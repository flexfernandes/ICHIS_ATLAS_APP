# Prompt — GF Atlas Web Page (Central Corporativa)

> Prompt para geração da Web Page dinâmica da Central Corporativa GREENFARMS no ERPNext/Frappe Cloud.

---

Criar uma Web Page dinâmica, moderna, responsiva e funcional dentro do ERPNext/Frappe Cloud, inspirada na tela de referência enviada.

A Web Page será uma página inicial corporativa para navegação de conteúdos, relatórios, documentos, cadastros, rotinas operacionais e links internos usados no dia a dia de uma indústria.

**IMPORTANTE — ENTREGA EM DUAS PARTES:**
Esta é a **Parte 1**: entregar estrutura completa da página + sidebar dinâmica + navegação hierárquica funcional.
A Parte 2 (separada) cobrirá dashboard com métricas e busca global avançada.

====================================================
OBJETIVO
====================================================

Transformar a tela de referência em uma Web Page dinâmica e nativa do ERPNext/Frappe Cloud.

A página deve funcionar como uma central de acesso corporativo, permitindo que o usuário navegue por grupos, subgrupos e itens finais, até chegar em relatórios, páginas, dashboards, cadastros, documentos ou links.

Nesta primeira etapa, NÃO implementar regras de acesso por usuário.

Utilizar apenas:
- GF Content Group
- GF Content Registry

O objetivo inicial é construir a navegação dinâmica, organizada e funcional.

====================================================
REFERÊNCIA VISUAL
====================================================

O código HTML da página de referência foi fornecido **apenas como referência estética e de layout**. Não copiar o conteúdo nem a estrutura de dados hardcoded. Usar apenas como inspiração visual para:

- menu lateral escuro
- logotipo ou identificação da empresa no topo
- campo de busca na lateral
- grupos de navegação organizados por seção
- badges com contadores
- área principal clara
- breadcrumb superior
- data e status no canto superior direito
- título principal
- indicadores numéricos
- cards de acesso rápido
- visual limpo, moderno, corporativo e profissional

**O menu lateral deve ser 100% dinâmico**, carregado via `frappe.call` a partir dos registros reais do DocType GF Content Group. Nenhum item de menu deve ser hardcoded.

====================================================
ACESSO E AUTENTICAÇÃO
====================================================

A página será **privada**, acessível apenas por usuários logados no ERPNext/Frappe Cloud.

Utilizar `frappe.session.user` e `frappe.session.user_fullname` para exibir o avatar e o nome do usuário logado na sidebar e na topbar.

====================================================
DIREÇÃO DO CONTEÚDO
====================================================

Não centralizar a tela em IA, prompts ou cloud.

A página deve ser pensada para o uso diário de uma empresa industrial, com foco em:

- gestão
- vendas
- compras
- estoque
- produção
- financeiro
- engenharia
- qualidade
- clientes
- fornecedores
- projetos
- documentos
- relatórios
- ERP
- operações internas

Tecnologia, IA, cloud e integrações podem aparecer, mas como seção secundária no final do menu ou em um card específico.

====================================================
DOCTYPES UTILIZADOS
====================================================

A página deve consumir dados dos seguintes Doctypes:

1. **GF Content Group**
Responsável pela estrutura hierárquica dos grupos e subgrupos.

2. **GF Content Registry**
Responsável pelo cadastro dos itens finais que serão abertos pelo usuário.

Não utilizar GF Access Group nesta primeira etapa.
Não implementar controle de permissão nesta etapa.

====================================================
GF CONTENT GROUP
====================================================

Campos disponíveis:

- internal_name
- display_name
- parent_group
- is_group
- description
- icon (nome do ícone Lucide Icons)
- color (hex)
- sort_order
- active

A página deve montar automaticamente a navegação a partir dos registros ativos (`active = 1`) de GF Content Group.

====================================================
GF CONTENT REGISTRY
====================================================

Campos disponíveis:

- title
- content_group
- item_type
- reference_doctype
- reference_name
- route_url
- description
- icon
- color
- tags
- responsible_user
- status
- sort_order
- show_on_home
- favorite
- active

Valores possíveis de item_type:
WEB_PAGE, REPORT, DASHBOARD, PDF, HTML, DOCUMENT, APPLICATION, WORKFLOW, EXTERNAL_LINK, API, SCRIPT, OTHER

====================================================
HIERARQUIA DE NAVEGAÇÃO
====================================================

O GF Content Group suporta até **3 níveis visíveis na sidebar**:

```
Nível 0 — Raiz (ex: "GREENFARMS Documentação Corporativa")
  Nível 1 — Grupo principal (ex: "01 Comercial", "02 Engenharia")
    Nível 2 — Subgrupo (ex: "Clientes", "Propostas Comerciais")
```

**Regras para renderização da sidebar:**
- Nível 0 (raiz) não aparece no menu — serve apenas como âncora da árvore
- Nível 1 aparece como seções principais expansíveis no menu
- Nível 2 aparece como subitens quando o grupo pai é expandido
- Itens do GF Content Registry são carregados na área principal ao clicar no grupo
- Não renderizar recursão infinita — limitar a 3 níveis no menu lateral

====================================================
COMPORTAMENTO DE NAVEGAÇÃO
====================================================

- O menu lateral mostra os grupos de nível 1
- Ao clicar em um grupo de nível 1, ele expande os subgrupos (nível 2)
- Ao clicar em um subgrupo, a área principal exibe os itens vinculados
- Os itens finais abrem a rota definida em `route_url`
- Se `route_url` estiver vazio, montar o link com `reference_doctype` e `reference_name`
- O menu deve ter contadores de itens por grupo
- O usuário pode recolher e expandir os grupos
- Evitar mostrar tudo aberto ao mesmo tempo

====================================================
REGRAS DE ABERTURA DOS LINKS
====================================================

Para cada item do GF Content Registry:

- Se `route_url` existir → abrir `route_url`
- Se `item_type = REPORT` → `/app/query-report/[reference_name]`
- Se `item_type = DOCTYPE` → `/app/[doctype-em-kebab-case]`
- Se `item_type = DASHBOARD` → abrir dashboard correspondente
- Se `item_type = EXTERNAL_LINK` → abrir em nova aba
- Se `item_type = WEB_PAGE` → abrir rota da Web Page
- Se nenhum destino configurado → mostrar aviso discreto "Destino ainda não configurado"

====================================================
LAYOUT PRINCIPAL
====================================================

**1. Topbar**
- Breadcrumb dinâmico
- Data atual
- Status do sistema (sempre "Online")
- Avatar e nome do usuário logado

**2. Hero institucional**
- Título claro
- Descrição curta
- Contadores simples (total de registros, grupos, relatórios)

**3. Acesso Rápido**
- Cards dinâmicos com itens onde `show_on_home = 1`

**4. Áreas Operacionais**
- Grid com os grupos de nível 1, com ícone, cor e contador

**5. Seção de Tecnologia**
- Card escuro (estilo dark) para os grupos de tecnologia/ERP

====================================================
MENU LATERAL — ESTRUTURA
====================================================

Topo:
- Identificador da empresa (GF mark + GREENFARMS)
- Subtítulo "Central Corporativa"
- Campo de busca

Bloco fixo:
- Início
- Favoritos
- Recentes

Bloco dinâmico (carregado via API):
- Grupos de nível 1 agrupados por seção operacional
- Cada item: ícone + nome + contador + seta de expansão (se tiver filhos)

Rodapé:
- Avatar + nome do usuário logado

====================================================
INTEGRAÇÃO COM FRAPPE
====================================================

Utilizar `frappe.call` com `frappe.client.get_list` para carregar:

- Todos os GF Content Group com `active = 1`, ordenados por `sort_order asc`
- Todos os GF Content Registry com `active = 1` e `status != ARCHIVED`, ordenados por `sort_order asc`

Carregar os dois em paralelo no carregamento da página.
Usar `frappe.ready()` como ponto de entrada da inicialização.

====================================================
DESIGN VISUAL
====================================================

- Sidebar escura (#0b0f14)
- Área principal clara (#f5f6f8)
- Cards com bordas suaves e sombras discretas
- Ícones Lucide Icons (carregar via CDN)
- Hover elegante com transições suaves
- Tipografia Inter
- Badges pequenos para tipo de item
- Skeleton loading enquanto carrega os dados

====================================================
RESPONSIVIDADE
====================================================

- Desktop: sidebar fixa, grid de 4 colunas
- Tablet: grid de 2 colunas
- Mobile: sidebar colapsável via botão hamburguer, grid de 1 coluna

====================================================
ESTRUTURA DO ARQUIVO ENTREGUE
====================================================

Entregar **dois arquivos**:

1. `gf_atlas.py` — controller Python para a Web Page www do Frappe:
```python
no_cache = 1
login_required = True
def get_context(context): ...
```

2. `gf_atlas.html` — template Frappe com `{% extends "templates/base.html" %}` contendo:
- `{% block head_include %}` — CSS completo + Lucide CDN
- `{% block content %}` — HTML da sidebar e área principal
- `{% block script %}` — JavaScript completo com toda a lógica

====================================================
RESULTADO ESPERADO
====================================================

Uma Web Page Frappe moderna, dinâmica e privada que transforma os dados do GF Content Group e GF Content Registry em uma central corporativa funcional — com sidebar dinâmica, navegação hierárquica em 3 níveis, abertura inteligente de links e visual inspirado na referência fornecida, adaptado para uma empresa industrial.
