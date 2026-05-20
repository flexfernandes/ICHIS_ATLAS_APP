# Prompt — GF Integration Settings

## Objetivo

Implementar a tela de configuração centralizada de integrações externas da GREENFARMS chamada **"GF Integration Settings"**, seguindo exatamente o mesmo padrão arquitetural do `GF Content Registry` já existente no projeto `ichis_atlas_app`.

---

## Decisão Arquitetural

**DocType Single como backend de dados + Página HTML customizada como interface.**

- O **DocType Single** (`GF Integration Settings`) armazena os dados via Frappe ORM.
- A **página HTML** (`/www/gf_integration_settings.html`) é a interface visual, seguindo o padrão do `gf_content_registry.html`. A navegação é feita exclusivamente por ela.
- O form padrão do Frappe para este DocType **não será utilizado** como interface.
- Carregamento e salvamento de dados ocorrem via `frappe.call` a métodos Python `@frappe.whitelist()`.

---

## Arquivos a Criar

```
ichis_atlas_app/
├── doctype/
│   └── gf_integration_settings/
│       ├── gf_integration_settings.json
│       └── gf_integration_settings.py
└── www/
    └── gf_integration_settings.html
```

---

## 1. DocType — `gf_integration_settings.json`

**Metadados**
- `issingle: 1`
- `module: "Ichis Atlas App"`
- `track_changes: 1`
- Permissões: `System Manager` (leitura + escrita), `GF Manager` (leitura + escrita)

**Campos — Google Drive**

| fieldname | fieldtype | label | observações |
|---|---|---|---|
| `gd_section` | Section Break | Google Drive | — |
| `gd_enabled` | Check | Enable Google Drive | default: 0 |
| `gd_client_id` | Data | Client ID | — |
| `gd_client_secret` | Password | Client Secret | — |
| `gd_redirect_uri` | Data | Redirect URI | `read_only: 1` — gerado pelo backend |
| `gd_root_folder_id` | Data | Root Folder ID | — |
| `gd_read_folder_id` | Data | Default Read Folder ID | — |
| `gd_write_folder_id` | Data | Default Write Folder ID | — |
| `gd_oauth_scope` | Small Text | OAuth Scope | `read_only: 1` — valor fixo definido pelo backend |
| `gd_access_token` | Password | Access Token | `read_only: 1` — gerenciado exclusivamente pelo backend OAuth |
| `gd_refresh_token` | Password | Refresh Token | `read_only: 1` — gerenciado exclusivamente pelo backend OAuth |
| `gd_status` | Data | Connection Status | `read_only: 1` |
| `gd_last_tested` | Datetime | Last Connection Test | `read_only: 1` |

**Campos — Gemini**

| fieldname | fieldtype | label | observações |
|---|---|---|---|
| `gemini_section` | Section Break | Gemini API | — |
| `gemini_enabled` | Check | Enable Gemini | default: 0 |
| `gemini_api_key` | Password | API Key | — |
| `gemini_default_model` | Select | Default Model | options: `gemini-2.0-flash\ngemini-1.5-pro\ngemini-1.5-flash` |
| `gemini_temperature` | Float | Temperature | default: 0.7 |
| `gemini_max_tokens` | Int | Max Output Tokens | default: 2048 |
| `gemini_system_instruction` | Text | System Instruction | — |
| `gemini_status` | Data | Connection Status | `read_only: 1` |
| `gemini_last_tested` | Datetime | Last Connection Test | `read_only: 1` |

**Campos — OpenAI ChatGPT**

| fieldname | fieldtype | label | observações |
|---|---|---|---|
| `oai_section` | Section Break | OpenAI ChatGPT | — |
| `oai_enabled` | Check | Enable OpenAI | default: 0 |
| `oai_api_key` | Password | API Key | — |
| `oai_org_id` | Data | Organization ID | opcional |
| `oai_project_id` | Data | Project ID | opcional |
| `oai_default_model` | Select | Default Model | options: `gpt-4o\ngpt-4o-mini\ngpt-4-turbo\ngpt-3.5-turbo` |
| `oai_temperature` | Float | Temperature | default: 0.7 |
| `oai_max_tokens` | Int | Max Tokens | default: 2048 |
| `oai_system_prompt` | Text | System Prompt | — |
| `oai_status` | Data | Connection Status | `read_only: 1` |
| `oai_last_tested` | Datetime | Last Connection Test | `read_only: 1` |

---

## 2. Python — `gf_integration_settings.py`

Criar a classe `GFIntegrationSettings(Document)` com os seguintes métodos stub — **sem implementação real neste momento**, apenas assinatura, docstring e `# TODO`.

```python
class GFIntegrationSettings(Document):
    pass


@frappe.whitelist()
def get_settings():
    """
    Retorna os campos do DocType Single.
    Campos Password NUNCA são retornados com valor real —
    retornar True se configurado, False se vazio.
    Isso impede que chaves sensíveis trafeguem para o frontend.
    """
    # TODO: implementar


@frappe.whitelist()
def save_settings(data):
    """
    Recebe dict com os valores do form.
    Regra para campos Password: atualizar no banco APENAS se o
    valor recebido não for None. None indica que o usuário não
    alterou o campo (frontend enviou null intencionalmente).
    """
    # TODO: implementar


@frappe.whitelist()
def test_connection(service):
    """
    Testa a conectividade com o serviço informado.
    Parâmetro service: 'google_drive' | 'gemini' | 'openai'
    Retorno esperado: {'status': 'connected' | 'error', 'message': str}
    Atualiza os campos <service>_status e <service>_last_tested no banco.
    """
    # TODO: implementar


@frappe.whitelist()
def initiate_google_oauth():
    """
    Inicia o fluxo OAuth 2.0 do Google Drive.
    Retorna a URL de autorização para redirect.

    TODO: implementar fluxo completo:
    - Gerar state token anti-CSRF
    - Montar authorization URL com client_id, scope, redirect_uri
    - Registrar state no cache do Frappe
    - Criar endpoint de callback:
      /api/method/ichis_atlas_app.gf_integration_settings.google_oauth_callback
    - Callback: trocar code por access_token + refresh_token
    - Salvar tokens criptografados nos campos gd_access_token e gd_refresh_token
    """
    # TODO: implementar
```

---

## 3. HTML — `gf_integration_settings.html`

### Padrão visual obrigatório

- Usar **exatamente** as variáveis CSS já definidas no projeto:
  `--primary`, `--accent`, `--accent-pale`, `--bg`, `--surface`, `--border`, `--text`, `--text-m`, `--text-l`, `--mono`, `--radius`, `--font`
- Usar **Lucide Icons** via `/assets/ichis_atlas_app/js/lucide.min.js` — mesmo padrão do `gf_content_registry.html`
- Header idêntico ao padrão GF Atlas: logo "GF", título "GF Integration Settings", subtítulo, separador, link "Wiki Hub", avatar do usuário
- **Nenhum framework externo** (sem Bootstrap, Tailwind, Material UI)
- CSS escrito inline no `<style>` dentro de `{% block head_include %}`

### Layout

```
[Header GF Atlas]
─────────────────────────────────────────────────────────────
[Abas: ⚡ Google Drive | ✦ Gemini | ◯ OpenAI ChatGPT]
─────────────────────────────────────────────────────────────
[Conteúdo da aba ativa]
  [Banner de status: Not Connected | Connected | Error]
  [Descrição curta da integração]
  [Formulário com campos e descrições]
  [Rodapé com botões de ação]
```

### Tratamento de campos sensíveis no frontend (regra obrigatória)

- Campos Password **nunca** são pré-preenchidos com o valor real do banco
- Se o backend retornar `true` para o campo (valor existe), exibir:
  `placeholder="••••••••  (configurado — deixe em branco para manter)"`
- Se o backend retornar `false` (não configurado), exibir placeholder normal de exemplo
- Ao focar o campo, limpar o placeholder para que o usuário possa digitar novo valor
- Ao salvar: se o campo estiver vazio, enviar `null` — backend **não sobrescreve** o valor salvo

### Indicadores de status

| Estado | Cor | Ícone Lucide |
|---|---|---|
| `not-connected` | `--text-l` (cinza) | `wifi-off` |
| `connected` | `--accent` (verde) | `check-circle` |
| `error` | `#dc2626` (vermelho) | `alert-circle` |

### Conteúdo de cada aba

**Aba Google Drive**
- Toggle enable/disable
- Campos: `gd_client_id`, `gd_client_secret` (password, `autocomplete="off"`)
- Campos somente leitura: `gd_redirect_uri` com botão "Copiar", `gd_oauth_scope`
- Campos: `gd_root_folder_id`, `gd_read_folder_id`, `gd_write_folder_id`
- Status (`gd_status`) e data do último teste (`gd_last_tested`) — somente leitura
- Botões: **Conectar Google Drive** (OAuth), **Testar Conexão**, **Salvar**
- Descrição abaixo de cada campo explicando sua finalidade em linguagem simples

**Aba Gemini**
- Toggle enable/disable
- Campos: `gemini_api_key` (password), `gemini_default_model` (select), `gemini_temperature` (number, step 0.1, min 0, max 2), `gemini_max_tokens` (number), `gemini_system_instruction` (textarea)
- Status e data do último teste — somente leitura
- Botões: **Testar Conexão**, **Salvar**
- Descrição abaixo de cada campo

**Aba OpenAI ChatGPT**
- Toggle enable/disable
- Campos: `oai_api_key` (password), `oai_org_id`, `oai_project_id`, `oai_default_model` (select), `oai_temperature` (number), `oai_max_tokens` (number), `oai_system_prompt` (textarea)
- Status e data do último teste — somente leitura
- Botões: **Testar Conexão**, **Salvar**
- Descrição abaixo de cada campo

### JavaScript — comportamentos obrigatórios

```javascript
// INIT ──────────────────────────────────────────────
// 1. Chamar get_settings via frappe.call
// 2. Para cada campo não-Password: preencher com valor retornado
// 3. Para cada campo Password: se backend retornou true → aplicar
//    placeholder "configurado"; se false → placeholder vazio
// 4. Renderizar indicadores de status para cada integração
// 5. Inicializar lucide.createIcons()

// SAVE ──────────────────────────────────────────────
// 1. Serializar todos os campos do form ativo
// 2. Para campos Password: verificar se o usuário digitou valor novo
//    (campo não vazio e diferente do estado placeholder)
//    Se não digitou → enviar null no payload
// 3. frappe.call('...save_settings', { data: payload })
// 4. Toast de sucesso ou erro

// TEST CONNECTION ───────────────────────────────────
// 1. Botão entra em estado loading (spinner, disabled)
// 2. frappe.call('...test_connection', { service: 'gemini' })
// 3. Atualizar indicador de status com resultado retornado
// 4. Exibir toast com mensagem do backend
// 5. Restaurar botão

// GOOGLE OAUTH ──────────────────────────────────────
// 1. frappe.call('...initiate_google_oauth')
// 2. Redirecionar para URL retornada
// /* ── BACKEND INTEGRATION POINT ─────────────────
//    Endpoint de callback a criar:
//    /api/method/ichis_atlas_app.gf_integration_settings
//      .google_oauth_callback
//    Parâmetros: code (str), state (str)
//    Ação: trocar code por tokens, salvar no DocType
//    ─────────────────────────────────────────────── */
```

### Comentários de integração futura

Marcar **todos** os pontos onde o backend deverá ser conectado com o bloco padrão:

```javascript
// ── BACKEND INTEGRATION POINT ──────────────────────
// Método: ichis_atlas_app.gf_integration_settings.<nome>
// Parâmetros: { ... }
// Retorno esperado: { ... }
// ───────────────────────────────────────────────────
```

---

## Resultado Esperado

Três arquivos funcionais e sem erros:

1. **`gf_integration_settings.json`** — DocType Single, campos todos tipados corretamente, nomes em `snake_case` com prefixo por integração (`gd_`, `gemini_`, `oai_`), permissões definidas, módulo `Ichis Atlas App`

2. **`gf_integration_settings.py`** — Classe com 4 métodos stub, whitelisted, com docstrings detalhando o comportamento esperado e os `# TODO` de implementação futura, incluindo a estrutura do fluxo OAuth documentada em comentários

3. **`gf_integration_settings.html`** — Interface visual completa no padrão GF Atlas, com carregamento e salvamento real via `frappe.call`, tratamento correto de campos sensíveis (sem expor valores no frontend), indicadores de status funcionais, abas com toggle por integração e todos os pontos de integração futura marcados com comentários padronizados
