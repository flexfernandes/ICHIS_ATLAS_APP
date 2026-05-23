import re
import unicodedata
import requests
import frappe
from frappe.model.document import Document


class GFContentRegistry(Document):

    def before_insert(self):
        if not self.version:
            self.version = "1.0.0"
        if not self.internal_name and self.title:
            ver_slug = (self.version or "1.0.0").replace(".", "_")
            self.internal_name = self._generate_internal_name(self.title) + "_v" + ver_slug

    def validate(self):
        # Campos obrigatórios são hidden no DocType, então a validação é manual aqui
        if not self.title:
            frappe.throw("O campo <b>Título</b> é obrigatório.")
        if not self.internal_name:
            frappe.throw("O campo <b>Internal Name</b> é obrigatório.")
        if not self.item_type:
            frappe.throw("O campo <b>Tipo do Item</b> é obrigatório.")
        if not self.content_group:
            frappe.throw("O campo <b>Grupo de Conteúdo</b> é obrigatório.")
        if not self.skill:
            frappe.throw("O campo <b>Skill</b> é obrigatório.")

        if self.content_group and not self.access_group:
            default_ag = frappe.db.get_value("GF Content Group", self.content_group, "default_access_group")
            if default_ag:
                self.access_group = default_ag

        if not self.access_group:
            frappe.throw("O campo <b>Grupo de Acesso</b> é obrigatório.")

    def before_save(self):
        if self.content_group:
            self._resolve_drive_path()

    def after_insert(self):
        self._ensure_ns_directories()
        self._ensure_gd_ns_folder()

    def on_update(self):
        self._ensure_ns_directories()
        self._ensure_gd_ns_folder()

    def _ensure_ns_directories(self):
        if not self.internal_name:
            return
        import os
        base = frappe.get_site_path('public', 'files', 'gf_atlas')
        # gf_atlas/ sempre existe
        os.makedirs(base, exist_ok=True)
        # gf_atlas/{route_url_parts...}/{internal_name}/
        path = base
        if self.route_url:
            for part in [p for p in self.route_url.split('/') if p]:
                path = os.path.join(path, part)
                os.makedirs(path, exist_ok=True)
        ns_path = os.path.join(path, self.internal_name)
        os.makedirs(ns_path, exist_ok=True)

    def _ensure_gd_ns_folder(self):
        """Cria/garante pasta {internal_name} dentro de route_url no Google Drive."""
        if not self.internal_name or not self.route_url:
            return
        try:
            settings = frappe.get_single("GF Integration Settings")
            try:
                token = settings.get_password("gd_access_token") or ""
            except Exception:
                token = ""
            if not token:
                return
            base_id = _resolve_path_to_id(token, self.route_url)
            if not base_id:
                return
            if not _find_folder(token, self.internal_name, base_id):
                _create_folder(token, self.internal_name, base_id)
        except Exception as e:
            frappe.log_error(f"NS GD folder creation failed for {self.internal_name}: {e}")

    def _resolve_drive_path(self):
        external_ref = frappe.db.get_value("GF Content Group", self.content_group, "external_reference")
        if not external_ref:
            frappe.throw(
                f"O Grupo de Conteúdo <b>{self.content_group}</b> não possui Referência Externa "
                "(Google Drive) configurada. Preencha o campo antes de salvar."
            )

        settings_doc = frappe.get_single("GF Integration Settings")
        try:
            access_token = settings_doc.get_password("gd_access_token") or ""
        except Exception:
            access_token = ""

        if not access_token:
            frappe.throw(
                "Google Drive não está conectado. Configure a integração em "
                "<b>GF Integration Settings</b> antes de salvar."
            )

        def _search(token):
            safe_ref = external_ref.replace("'", "\\'")
            return requests.get(
                "https://www.googleapis.com/drive/v3/files",
                params={
                    "q": f"name='{safe_ref}' and mimeType='application/vnd.google-apps.folder' and trashed=false",
                    "fields": "files(id,name,parents)",
                    "pageSize": 10,
                },
                headers={"Authorization": f"Bearer {token}"},
                timeout=15,
            )

        resp = _search(access_token)

        if resp.status_code == 401:
            from ichis_atlas_app.ichis_atlas_app.doctype.gf_integration_settings.gf_integration_settings import _refresh_google_token
            new_token = _refresh_google_token(settings_doc)
            if new_token:
                access_token = new_token
                resp = _search(access_token)
            else:
                frappe.throw(
                    "Token do Google Drive expirou e não foi possível renová-lo. "
                    "Reconecte em <b>GF Integration Settings</b>."
                )

        if resp.status_code != 200:
            frappe.throw(f"Erro ao consultar o Google Drive (HTTP {resp.status_code}).")

        files = resp.json().get("files", [])
        if not files:
            folder_id = _create_folder(access_token, external_ref, "root")
        else:
            folder_id = files[0]["id"]
        auth_headers = {"Authorization": f"Bearer {access_token}"}
        self.route_url = self._build_drive_path(folder_id, auth_headers)

    def _build_drive_path(self, folder_id, headers):
        parts = []
        current_id = folder_id
        visited = set()

        while current_id and current_id not in visited and len(parts) < 20:
            visited.add(current_id)
            resp = requests.get(
                f"https://www.googleapis.com/drive/v3/files/{current_id}",
                params={"fields": "id,name,parents"},
                headers=headers,
                timeout=10,
            )
            if resp.status_code != 200:
                break
            data = resp.json()
            parts.append(data.get("name", ""))
            parents = data.get("parents", [])
            current_id = parents[0] if parents else None

        parts.reverse()
        if parts and parts[0] in ("My Drive", "Meu Drive"):
            parts = parts[1:]
        return "/".join(parts)

    def _generate_internal_name(self, title):
        name = unicodedata.normalize("NFD", title.lower())
        name = "".join(c for c in name if unicodedata.category(c) != "Mn")
        name = re.sub(r"[^a-z0-9]+", "_", name)
        name = name.strip("_")
        return name[:64] if len(name) > 64 else name


# ── Helpers Drive ────────────────────────────────────────────────────────────

def _get_drive_token():
    """Retorna (settings_doc, access_token) renovando se necessário."""
    from ichis_atlas_app.ichis_atlas_app.doctype.gf_integration_settings.gf_integration_settings import _refresh_google_token

    settings = frappe.get_single("GF Integration Settings")
    try:
        token = settings.get_password("gd_access_token") or ""
    except Exception:
        token = ""

    if not token:
        frappe.throw("Google Drive não está conectado. Configure em <b>GF Integration Settings</b>.")

    return settings, token


def _drive_get(token, url, params=None, timeout=10):
    return requests.get(url, params=params, headers={"Authorization": f"Bearer {token}"}, timeout=timeout)


def _drive_post(token, url, json_body=None, timeout=10):
    return requests.post(url, json=json_body, headers={"Authorization": f"Bearer {token}"}, timeout=timeout)


def _find_folder(token, name, parent_id="root"):
    safe = name.replace("'", "\\'")
    r = _drive_get(token,
        "https://www.googleapis.com/drive/v3/files",
        params={
            "q": f"name='{safe}' and mimeType='application/vnd.google-apps.folder' and '{parent_id}' in parents and trashed=false",
            "fields": "files(id,name)",
            "pageSize": 1,
        },
    )
    if r.status_code == 200:
        files = r.json().get("files", [])
        return files[0]["id"] if files else None
    return None


def _create_folder(token, name, parent_id):
    r = requests.post(
        "https://www.googleapis.com/drive/v3/files",
        json={"name": name, "mimeType": "application/vnd.google-apps.folder", "parents": [parent_id]},
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        timeout=10,
    )
    if r.status_code in (200, 201):
        return r.json().get("id")
    frappe.throw(f"Erro ao criar pasta '{name}' no Google Drive (HTTP {r.status_code}).")


def _resolve_path_to_id(token, path):
    """Resolve um caminho 'A/B/C' para o ID da pasta folha. Retorna None se qualquer nível não existir."""
    parts = [p for p in path.split("/") if p]
    parent_id = "root"
    for part in parts:
        folder_id = _find_folder(token, part, parent_id)
        if not folder_id:
            return None
        parent_id = folder_id
    return parent_id


def _list_images(token, folder_id):
    IMAGE_MIME = (
        "image/jpeg,image/png,image/gif,image/webp,image/svg+xml,"
        "image/bmp,image/tiff,image/avif"
    )
    mime_filter = " or ".join(f"mimeType='{m}'" for m in IMAGE_MIME.split(","))
    r = _drive_get(token,
        "https://www.googleapis.com/drive/v3/files",
        params={
            "q": f"({mime_filter}) and '{folder_id}' in parents and trashed=false",
            "fields": "files(id,name,mimeType,size,thumbnailLink,webContentLink,createdTime)",
            "orderBy": "createdTime desc",
            "pageSize": 100,
        },
    )
    if r.status_code == 200:
        return r.json().get("files", [])
    return []


# ── Whitelisted API ──────────────────────────────────────────────────────────

@frappe.whitelist()
def ns_get_workspace(doc_name):
    """
    Retorna o folder_id do diretório NS e a lista de imagens.
    Cria a pasta internal_name dentro de route_url se não existir.
    """
    doc = frappe.get_doc("GF Content Registry", doc_name)
    if not doc.route_url or not doc.internal_name:
        frappe.throw("O registro precisa de URL/Rota e Internal Name preenchidos antes de usar o Natural Studio.")

    settings, token = _get_drive_token()

    # Resolve o caminho base (route_url)
    base_id = _resolve_path_to_id(token, doc.route_url)
    if not base_id:
        frappe.throw(f"Caminho base '{doc.route_url}' não encontrado no Google Drive.")

    # Verifica/cria a pasta do internal_name
    ns_folder_id = _find_folder(token, doc.internal_name, base_id)
    if not ns_folder_id:
        ns_folder_id = _create_folder(token, doc.internal_name, base_id)
        created = True
    else:
        created = False

    images = _list_images(token, ns_folder_id)

    return {
        "folder_id": ns_folder_id,
        "folder_path": f"{doc.route_url}/{doc.internal_name}",
        "created": created,
        "images": images,
    }


@frappe.whitelist()
def ns_upload_file(doc_name, filename, file_base64, mime_type="image/jpeg"):
    """Faz upload de uma imagem para a pasta NS do registro."""
    import base64

    doc = frappe.get_doc("GF Content Registry", doc_name)
    settings, token = _get_drive_token()

    base_id = _resolve_path_to_id(token, doc.route_url)
    if not base_id:
        frappe.throw(f"Caminho base '{doc.route_url}' não encontrado no Google Drive.")

    ns_folder_id = _find_folder(token, doc.internal_name, base_id)
    if not ns_folder_id:
        ns_folder_id = _create_folder(token, doc.internal_name, base_id)

    file_bytes = base64.b64decode(file_base64)

    metadata = {"name": filename, "parents": [ns_folder_id]}
    import json as _json

    boundary = "gf_ns_boundary_xyz"
    body = (
        f"--{boundary}\r\n"
        f"Content-Type: application/json; charset=UTF-8\r\n\r\n"
        f"{_json.dumps(metadata)}\r\n"
        f"--{boundary}\r\n"
        f"Content-Type: {mime_type}\r\n\r\n"
    ).encode("utf-8") + file_bytes + f"\r\n--{boundary}--".encode("utf-8")

    r = requests.post(
        "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
        data=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": f"multipart/related; boundary={boundary}",
        },
        timeout=60,
    )

    if r.status_code in (200, 201):
        return {"success": True, "file": r.json()}

    frappe.throw(f"Erro no upload para o Google Drive (HTTP {r.status_code}): {r.text[:200]}")


@frappe.whitelist()
def ns_delete_file(file_id):
    """Exclui um arquivo do Google Drive pelo file_id."""
    settings, token = _get_drive_token()

    r = requests.delete(
        f"https://www.googleapis.com/drive/v3/files/{file_id}",
        headers={"Authorization": f"Bearer {token}"},
        timeout=15,
    )

    if r.status_code == 204:
        return {"success": True}

    frappe.throw(f"Erro ao excluir arquivo do Google Drive (HTTP {r.status_code}).")


@frappe.whitelist()
def ns_append_timeline_entry(doc_name, entry_json):
    """Acrescenta uma entrada JSON à timeline usando db.set_value (sem hooks, sem conflito de versão)."""
    import json

    current = frappe.db.get_value("GF Content Registry", doc_name, "prompt_timeline") or "[]"
    try:
        timeline = json.loads(current)
        if not isinstance(timeline, list):
            timeline = []
    except Exception:
        timeline = []

    entry = json.loads(entry_json)
    timeline.append(entry)
    new_json = json.dumps(timeline, ensure_ascii=False)
    frappe.db.set_value("GF Content Registry", doc_name, "prompt_timeline", new_json, update_modified=False)
    frappe.db.commit()
    return timeline


@frappe.whitelist()
def ns_clear_timeline(doc_name):
    """Limpa toda a timeline do registro."""
    frappe.db.set_value("GF Content Registry", doc_name, "prompt_timeline", "[]", update_modified=False)
    frappe.db.commit()
    return []
