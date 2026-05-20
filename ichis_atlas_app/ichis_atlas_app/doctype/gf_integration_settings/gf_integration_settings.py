import frappe
from frappe.model.document import Document

SITE_URL        = "https://greenfarms.v.frappe.cloud"
CALLBACK_PATH   = "/api/method/ichis_atlas_app.ichis_atlas_app.doctype.gf_integration_settings.gf_integration_settings.google_oauth_callback"
REDIRECT_URI    = SITE_URL + CALLBACK_PATH
OAUTH_SCOPE     = "https://www.googleapis.com/auth/drive"
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL= "https://oauth2.googleapis.com/token"

# ── Campos sensíveis por integração ─────────────────────────────────────────
PASSWORD_FIELDS = [
    "gd_client_secret",
    "gd_access_token",
    "gd_refresh_token",
    "gemini_api_key",
    "oai_api_key",
]


class GFIntegrationSettings(Document):
    pass


@frappe.whitelist()
def get_settings():
    """
    Retorna os campos do DocType Single GF Integration Settings.

    Campos Password NUNCA são retornados com valor real:
    - Retorna True  se o campo possui valor configurado no banco.
    - Retorna False se o campo está vazio.

    Isso garante que chaves sensíveis nunca trafeguem para o frontend.
    O frontend usa esse booleano para exibir o placeholder "configurado".
    """
    doc = frappe.get_single("GF Integration Settings")

    # Garante que redirect_uri e oauth_scope estejam sempre preenchidos
    if doc.gd_redirect_uri != REDIRECT_URI or doc.gd_oauth_scope != OAUTH_SCOPE:
        doc.gd_redirect_uri = REDIRECT_URI
        doc.gd_oauth_scope  = OAUTH_SCOPE
        doc.save(ignore_permissions=True)
        frappe.db.commit()

    data = doc.as_dict()

    for field in PASSWORD_FIELDS:
        data[field] = bool(data.get(field))

    return data


@frappe.whitelist()
def save_settings(data):
    """
    Salva APENAS campos Password que o usuário alterou explicitamente.
    Campos normais são salvos pelo frontend via frappe.client.set_value (nativo).
    Só é chamado quando ao menos um campo sensível foi preenchido.
    """
    import json
    if isinstance(data, str):
        data = json.loads(data)

    doc = frappe.get_single("GF Integration Settings")

    for field, value in data.items():
        if field in PASSWORD_FIELDS and value:
            doc.set(field, value)

    doc.save(ignore_permissions=True)
    frappe.db.commit()
    return {"success": True}


@frappe.whitelist()
def test_connection(service):
    """
    Testa a conectividade com o serviço especificado.
    Retorna status e mensagem. Atualiza <service>_status e <service>_last_tested.
    """
    if service == "google_drive":
        return _test_google_drive()
    elif service == "gemini":
        return _test_gemini()
    elif service == "openai":
        return _test_openai()
    return {"status": "error", "message": f"Serviço '{service}' desconhecido."}


def _test_google_drive():
    import requests

    doc = frappe.get_single("GF Integration Settings")

    try:
        access_token = doc.get_password("gd_access_token") or ""
    except Exception:
        access_token = ""

    if not access_token:
        return {
            "status":  "error",
            "message": "Sem token de acesso. Clique em 'Conectar Google Drive' para autorizar.",
        }

    def _do_test(token):
        return requests.get(
            "https://www.googleapis.com/drive/v3/about",
            params={"fields": "user"},
            headers={"Authorization": f"Bearer {token}"},
            timeout=10,
        )

    resp = _do_test(access_token)

    # Token expirado → tenta renovar e repete
    if resp.status_code == 401:
        new_token = _refresh_google_token(doc)
        if new_token:
            resp = _do_test(new_token)

    def _save_status(status):
        doc.gd_status      = status
        doc.gd_last_tested = frappe.utils.now_datetime()
        doc.save(ignore_permissions=True)
        frappe.db.commit()

    if resp.status_code == 200:
        email = resp.json().get("user", {}).get("emailAddress", "")
        _save_status("connected")
        msg = f"Conectado como {email}" if email else "Conexão com Google Drive bem-sucedida."
        return {"status": "connected", "message": msg}

    _save_status("error")
    return {"status": "error", "message": f"Falha ao conectar ao Google Drive (HTTP {resp.status_code})."}


def _refresh_google_token(doc):
    """Tenta renovar o access_token usando o refresh_token. Retorna o novo token ou None."""
    import requests

    try:
        refresh_token = doc.get_password("gd_refresh_token") or ""
        client_secret = doc.get_password("gd_client_secret") or ""
    except Exception:
        return None

    if not refresh_token or not doc.gd_client_id or not client_secret:
        return None

    resp = requests.post(GOOGLE_TOKEN_URL, data={
        "grant_type":    "refresh_token",
        "refresh_token": refresh_token,
        "client_id":     doc.gd_client_id,
        "client_secret": client_secret,
    }, timeout=10)

    if resp.status_code == 200:
        new_token = resp.json().get("access_token", "")
        if new_token:
            doc.gd_access_token = new_token
            doc.save(ignore_permissions=True)
            frappe.db.commit()
            return new_token

    return None


def _test_gemini():
    import requests

    doc = frappe.get_single("GF Integration Settings")

    try:
        api_key = doc.get_password("gemini_api_key") or ""
    except Exception:
        api_key = ""

    if not api_key:
        return {"status": "error", "message": "API Key não configurada."}

    model = doc.gemini_default_model or "gemini-2.0-flash"
    url   = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"

    try:
        resp = requests.post(url, json={"contents": [{"parts": [{"text": "ping"}]}]}, timeout=10)
    except Exception as e:
        return {"status": "error", "message": f"Erro de rede: {e}"}

    if resp.status_code == 200:
        doc.gemini_status      = "connected"
        doc.gemini_last_tested = frappe.utils.now_datetime()
        doc.save(ignore_permissions=True)
        frappe.db.commit()
        return {"status": "connected", "message": f"Gemini ({model}) respondendo corretamente."}

    doc.gemini_status      = "error"
    doc.gemini_last_tested = frappe.utils.now_datetime()
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    return {"status": "error", "message": f"Erro Gemini API (HTTP {resp.status_code})."}


def _test_openai():
    import requests

    doc = frappe.get_single("GF Integration Settings")

    try:
        api_key = doc.get_password("oai_api_key") or ""
    except Exception:
        api_key = ""

    if not api_key:
        return {"status": "error", "message": "API Key não configurada."}

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    if doc.oai_org_id:
        headers["OpenAI-Organization"] = doc.oai_org_id
    if doc.oai_project_id:
        headers["OpenAI-Project"] = doc.oai_project_id

    try:
        resp = requests.get("https://api.openai.com/v1/models", headers=headers, timeout=10)
    except Exception as e:
        return {"status": "error", "message": f"Erro de rede: {e}"}

    if resp.status_code == 200:
        doc.oai_status      = "connected"
        doc.oai_last_tested = frappe.utils.now_datetime()
        doc.save(ignore_permissions=True)
        frappe.db.commit()
        return {"status": "connected", "message": "Conexão com OpenAI bem-sucedida."}

    doc.oai_status      = "error"
    doc.oai_last_tested = frappe.utils.now_datetime()
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    return {"status": "error", "message": f"Erro OpenAI API (HTTP {resp.status_code})."}


@frappe.whitelist()
def initiate_google_oauth():
    """
    Inicia o fluxo OAuth 2.0 do Google Drive.
    Retorna a URL de autorização para o frontend redirecionar o usuário.
    """
    from urllib.parse import urlencode

    doc = frappe.get_single("GF Integration Settings")

    if not doc.gd_client_id:
        return {"error": "Configure e salve o Client ID antes de iniciar o OAuth."}

    state = frappe.generate_hash(length=32)
    frappe.cache.set_value(f"gd_oauth_state_{state}", True, expires_in_sec=600)

    params = {
        "client_id":     doc.gd_client_id,
        "redirect_uri":  REDIRECT_URI,
        "response_type": "code",
        "scope":         OAUTH_SCOPE,
        "access_type":   "offline",
        "prompt":        "consent",
        "state":         state,
    }

    auth_url = GOOGLE_AUTH_URL + "?" + urlencode(params)
    return {"auth_url": auth_url}


@frappe.whitelist(allow_guest=True)
def google_oauth_callback(code=None, state=None, error=None):
    """
    Callback OAuth 2.0 do Google Drive.
    Recebe o code de autorização, troca por tokens e salva no DocType.
    """
    import requests

    redirect_base = f"{SITE_URL}/gf_integration_settings"

    def _redirect(url):
        frappe.local.response["type"] = "redirect"
        frappe.local.response["location"] = url

    try:
        if error:
            return _redirect(f"{redirect_base}?oauth_error={error}")

        if not code or not state:
            return _redirect(f"{redirect_base}?oauth_error=missing_params")

        # Valida state anti-CSRF
        cache_key = f"gd_oauth_state_{state}"
        try:
            cached = frappe.cache.get_value(cache_key)
        except Exception:
            cached = None

        if not cached:
            return _redirect(f"{redirect_base}?oauth_error=invalid_state")

        try:
            frappe.cache.delete_value(cache_key)
        except Exception:
            pass

        doc = frappe.get_single("GF Integration Settings")

        try:
            client_secret = doc.get_password("gd_client_secret") or ""
        except Exception:
            client_secret = ""

        if not doc.gd_client_id or not client_secret:
            frappe.log_error("Client ID ou Client Secret não configurados.", "OAuth Callback")
            return _redirect(f"{redirect_base}?oauth_error=missing_credentials")

        # Troca code por access_token + refresh_token
        resp = requests.post(GOOGLE_TOKEN_URL, data={
            "code":          code,
            "client_id":     doc.gd_client_id,
            "client_secret": client_secret,
            "redirect_uri":  REDIRECT_URI,
            "grant_type":    "authorization_code",
        }, timeout=15)

        if resp.status_code != 200:
            frappe.log_error(f"Token exchange falhou ({resp.status_code}): {resp.text}", "OAuth Callback")
            return _redirect(f"{redirect_base}?oauth_error=token_exchange_failed")

        tokens = resp.json()

        try:
            existing_refresh = doc.get_password("gd_refresh_token") or ""
        except Exception:
            existing_refresh = ""

        doc.gd_access_token  = tokens.get("access_token", "")
        doc.gd_refresh_token = tokens.get("refresh_token") or existing_refresh
        doc.gd_status        = "connected"
        doc.save(ignore_permissions=True)
        frappe.db.commit()

        return _redirect(f"{redirect_base}?oauth_success=1")

    except Exception:
        frappe.log_error(frappe.get_traceback(), "OAuth Callback Error")
        return _redirect(f"{redirect_base}?oauth_error=server_error")
