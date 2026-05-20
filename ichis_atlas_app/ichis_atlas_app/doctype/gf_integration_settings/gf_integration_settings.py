import frappe
from frappe.model.document import Document


class GFIntegrationSettings(Document):
    pass


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

    Retorno:
        dict: { "auth_url": str } — URL de autorização para redirect no frontend.

    TODO: implementar fluxo completo:

    1. Ler client_id e redirect_uri do DocType
    2. Gerar state token aleatório anti-CSRF:
           state = frappe.generate_hash(length=32)
           frappe.cache().set_value(f"gd_oauth_state_{state}", True, expires_in_sec=600)
    3. Montar authorization URL:
           https://accounts.google.com/o/oauth2/v2/auth?
             client_id=<client_id>
             &redirect_uri=<redirect_uri>
             &response_type=code
             &scope=https://www.googleapis.com/auth/drive
             &access_type=offline
             &prompt=consent
             &state=<state>
    4. Retornar {"auth_url": url} para o frontend redirecionar o usuário.

    ── BACKEND INTEGRATION POINT ──────────────────────────────────────────────
    Endpoint de callback a criar:
        /api/method/ichis_atlas_app.ichis_atlas_app.doctype
          .gf_integration_settings.gf_integration_settings.google_oauth_callback
    Parâmetros recebidos: code (str), state (str)
    Ação:
        - Validar state no cache do Frappe (anti-CSRF)
        - POST https://oauth2.googleapis.com/token com code + client_id + client_secret
        - Armazenar access_token e refresh_token nos campos gd_access_token / gd_refresh_token
        - Atualizar gd_status para "connected"
    ────────────────────────────────────────────────────────────────────────────
    """
    # TODO: implementar
    pass
