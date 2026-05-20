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
    Salva os campos do DocType Single GF Integration Settings.

    Regra para campos Password:
    - Atualiza no banco APENAS se o valor recebido NÃO for None/null.
    - None indica que o usuário não alterou o campo (frontend enviou null
      intencionalmente) — o valor existente deve ser preservado.

    Parâmetros:
        data (str | dict): JSON com os valores do formulário.

    Retorno:
        dict: { "success": True } em caso de sucesso.
    """
    import json
    if isinstance(data, str):
        data = json.loads(data)

    doc = frappe.get_single("GF Integration Settings")

    for field, value in data.items():
        if field in PASSWORD_FIELDS and value is None:
            continue
        setattr(doc, field, value)

    doc.save(ignore_permissions=True)
    frappe.db.commit()
    return {"success": True}


@frappe.whitelist()
def test_connection(service):
    """
    Testa a conectividade com o serviço especificado.

    Parâmetros:
        service (str): 'google_drive' | 'gemini' | 'openai'

    Retorno:
        dict: {
            "status":  "connected" | "error",
            "message": str  — mensagem descritiva para exibição no frontend
        }

    Efeito colateral:
        Atualiza os campos <service>_status e <service>_last_tested no banco.
    """
    # TODO: implementar por serviço
    #
    # Exemplo de estrutura futura:
    #
    # from datetime import datetime
    # doc = frappe.get_single("GF Integration Settings")
    # now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #
    # if service == "gemini":
    #     result = _test_gemini(doc)
    # elif service == "openai":
    #     result = _test_openai(doc)
    # elif service == "google_drive":
    #     result = _test_google_drive(doc)
    # else:
    #     return {"status": "error", "message": f"Serviço '{service}' não reconhecido."}
    #
    # status_field     = f"{service}_status" if service != "google_drive" else "gd_status"
    # last_tested_field = f"{service}_last_tested" if service != "google_drive" else "gd_last_tested"
    # doc.set(status_field, result["status"])
    # doc.set(last_tested_field, now)
    # doc.save(ignore_permissions=True)
    # frappe.db.commit()
    # return result
    pass


@frappe.whitelist()
def initiate_google_oauth():
    """
    Inicia o fluxo OAuth 2.0 do Google Drive.
    Retorna a URL de autorização para o frontend redirecionar o usuário.
    """
    from urllib.parse import urlencode

    doc = frappe.get_single("GF Integration Settings")

    if not doc.gd_client_id:
        frappe.throw("Configure o Client ID antes de iniciar o OAuth.")

    state = frappe.generate_hash(length=32)
    frappe.cache().set_value(f"gd_oauth_state_{state}", True, expires_in_sec=600)

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
    from urllib.parse import urlencode

    redirect_base = f"{SITE_URL}/gf_integration_settings"

    if error:
        return frappe.redirect(f"{redirect_base}?oauth_error={error}")

    if not code or not state:
        return frappe.redirect(f"{redirect_base}?oauth_error=missing_params")

    # Valida state anti-CSRF
    cache_key = f"gd_oauth_state_{state}"
    if not frappe.cache().get_value(cache_key):
        return frappe.redirect(f"{redirect_base}?oauth_error=invalid_state")
    frappe.cache().delete_value(cache_key)

    doc = frappe.get_single("GF Integration Settings")

    # Troca code por access_token + refresh_token
    resp = requests.post(GOOGLE_TOKEN_URL, data={
        "code":          code,
        "client_id":     doc.gd_client_id,
        "client_secret": doc.get_password("gd_client_secret"),
        "redirect_uri":  REDIRECT_URI,
        "grant_type":    "authorization_code",
    }, timeout=15)

    if resp.status_code != 200:
        return frappe.redirect(f"{redirect_base}?oauth_error=token_exchange_failed")

    tokens = resp.json()
    doc.gd_access_token  = tokens.get("access_token", "")
    doc.gd_refresh_token = tokens.get("refresh_token", doc.get_password("gd_refresh_token") or "")
    doc.gd_status        = "connected"
    doc.save(ignore_permissions=True)
    frappe.db.commit()

    return frappe.redirect(f"{redirect_base}?oauth_success=1")
