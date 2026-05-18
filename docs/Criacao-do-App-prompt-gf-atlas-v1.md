# PROMPT — GF ATLAS APP (v1)
## GREENFARMS Corporate Foundation

---

## CONTEXTO DO SISTEMA

App customizado para **ERPNext / Frappe Cloud** (`greenfarmsagro.frappe.cloud`),
desenvolvido como **Custom App Frappe** (Python + JSON, padrão `apps/`).

O app se chama **GF Atlas** e é a base estrutural do ecossistema digital da
GREENFARMS. Toda a gestão de conteúdo, acesso e organização corporativa parte
deste app.

**Regra de nomenclatura global:** Todos os Doctypes obrigatoriamente iniciam com `GF`.
`GREENFARMS` deve ser sempre escrito junto, sem espaço.

---

## OBJETIVO DO APP

O app deve permitir organizar dentro do ERPNext:

- relatórios e dashboards
- documentações técnicas e internas
- APIs e integrações
- workflows e automações
- scripts e aplicações hospedadas
- conteúdos HTML e PDFs
- links externos
- materiais internos e registros organizacionais
- biblioteca técnica
- projetos
- páginas e portais futuros

O objetivo é transformar o ERPNext em uma base corporativa organizada e escalável.

---

## ESCOPO DESTA VERSÃO

Focar **exclusivamente** em:

1. Estrutura de Doctypes
2. Estrutura de permissões
3. Estrutura organizacional
4. Cadastro central dos registros
5. Relacionamento entre grupos
6. Relacionamento com usuários reais do ERPNext
7. Popularização automática via hook `after_install`

**Popularização automática** significa: ao instalar o app, os grupos corporativos
padrão (GF Content Group e GF Access Group) são criados automaticamente via hook
`after_install`, sem intervenção manual. Nenhuma configuração manual deve ser
necessária após a instalação.

**Não duplicar registros:** o script de instalação deve verificar se o registro
já existe antes de criar. Deve permitir reinstalação sem erros e sem duplicações.

---

## NÃO IMPLEMENTAR NESTA VERSÃO

- Web Pages automáticas
- Homepage Wiki
- Qualquer frontend, portal ou interface visual
- Navegação visual ou árvore expandível
- Dashboards frontend
- Renderização dinâmica
- Menu automático
- Componentes gráficos

---

## ARQUITETURA CONCEITUAL

```
GF Content Group   = define ONDE o item aparece (organização hierárquica)
GF Access Group    = define QUEM pode acessar
GF Access Group User = vincula usuários reais do ERPNext aos grupos de acesso
GF Content Registry  = define O QUE é o item (registro central)
```

Fluxo conceitual:

```
Usuário faz login
↓
Sistema identifica o usuário ERPNext
↓
Sistema verifica os grupos do usuário (GF Access Group User)
↓
Sistema identifica os conteúdos permitidos (GF Content Registry)
↓
Sistema organiza pela estrutura hierárquica (GF Content Group)
↓
Sistema disponibiliza os registros autorizados
```

---

## PADRÃO DE NOMENCLATURA — REGRA GLOBAL

Todos os Doctypes que possuem campos de nome devem seguir este padrão duplo:

**`internal_name`**
- utilizado internamente no sistema, código, filtros e queries
- sem acentos, sem espaços, sem caracteres especiais
- lowercase, underscore permitido
- Exemplo: `projetos_especiais`

**`display_name`**
- utilizado visualmente na interface
- com acentos, com espaços, nomenclatura amigável
- aparência corporativa
- Exemplo: `Projetos Especiais`

---

## DOCTYPE 1 — GF Content Group

**Função:** Criar a árvore organizacional corporativa de conteúdo.
Semelhante a uma estrutura de pastas, plano de contas ou árvore de categorias.

### Campos

| # | fieldname | label | tipo | obrigatório | observação |
|---|-----------|-------|------|-------------|------------|
| 1 | `internal_name` | Nome Interno | Data | Sim | sem acentos, lowercase, underscore |
| 2 | `display_name` | Nome de Exibição | Data | Sim | com acentos, amigável |
| 3 | `parent_group` | Grupo Pai | Link → GF Content Group | Não | hierarquia |
| 4 | `is_group` | É Grupo | Check | — | nó pai ou folha |
| 5 | `default_access_group` | Grupo de Acesso Padrão | Link → GF Access Group | Não | pré-preenche o GF Content Registry |
| 6 | `description` | Descrição | Small Text | Não | |
| 7 | `sort_order` | Ordem | Int | Não | |
| 8 | `icon` | Ícone | Data | Não | |
| 9 | `color` | Cor | Data | Não | |
| 10 | `active` | Ativo | Check | — | Default: 1 |

**Observação sobre `default_access_group`:**
Ao criar um registro no GF Content Registry e selecionar um `content_group`,
o campo `access_group` do registro deve ser preenchido automaticamente com
o `default_access_group` definido neste grupo. O campo permanece editável
para permitir exceções por item.

---

## DOCTYPE 2 — GF Access Group

**Função:** Criar grupos de permissão corporativos.
Define quem pode visualizar, pesquisar, criar, alterar, deletar, exportar e imprimir.

### Campos

| # | fieldname | label | tipo | obrigatório | observação |
|---|-----------|-------|------|-------------|------------|
| 1 | `internal_name` | Nome Interno | Data | Sim | sem acentos, lowercase, underscore |
| 2 | `display_name` | Nome de Exibição | Data | Sim | com acentos, amigável |
| 3 | `description` | Descrição | Small Text | Não | |
| 4 | `is_internal` | Interno | Check | — | grupo de colaboradores |
| 5 | `is_external` | Externo | Check | — | clientes, fornecedores, terceiros |
| 6 | `is_restricted` | Restrito | Check | — | acesso sensível/confidencial |
| 7 | `system_group` | Grupo do Sistema | Check | — | criado pelo app |
| 8 | `default_landing_workspace` | Workspace Padrão | Data | Não | |
| 9 | `sort_order` | Ordem | Int | Não | |
| 10 | `active` | Ativo | Check | — | Default: 1 |

---

## DOCTYPE 3 — GF Access Group User

**Função:** Child DocType de GF Access Group. Vincula usuários reais do ERPNext
aos grupos de acesso com permissões granulares.

**Regra obrigatória:** O campo `user` deve ser do tipo `Link → User`, utilizando
diretamente o DocType nativo `User` do ERPNext/Frappe. O usuário nunca é digitado
manualmente.

O campo `full_name` deve usar `fetch_from: "user.full_name"` para preencher
automaticamente ao selecionar o usuário.

### Campos

| # | fieldname | label | tipo | obrigatório | observação |
|---|-----------|-------|------|-------------|------------|
| 1 | `user` | Usuário | Link → User | Sim | DocType nativo ERPNext |
| 2 | `full_name` | Nome Completo | Data | — | Read Only, fetch_from: user.full_name |
| 3 | `can_view` | Pode Visualizar | Check | — | Default: 1 |
| 4 | `can_search` | Pode Pesquisar | Check | — | Default: 1 |
| 5 | `can_create` | Pode Criar | Check | — | Default: 0 |
| 6 | `can_edit` | Pode Editar | Check | — | Default: 0 |
| 7 | `can_delete` | Pode Deletar | Check | — | Default: 0 |
| 8 | `can_export` | Pode Exportar | Check | — | Default: 0 |
| 9 | `can_print` | Pode Imprimir | Check | — | Default: 0 |
| 10 | `enabled` | Habilitado | Check | — | Default: 1 |

---

## DOCTYPE 4 — GF Content Registry

**Função:** Cadastro central de todos os registros organizacionais da GREENFARMS.
Agnóstico ao tipo de conteúdo — registra, organiza, relaciona e controla acesso.

Pode representar: relatório, dashboard, PDF, HTML, documento, workflow,
aplicação, script, API, link externo, conteúdo técnico, integração, automação, outros.

### Campos

| # | fieldname | label | tipo | obrigatório | observação |
|---|-----------|-------|------|-------------|------------|
| 1 | `title` | Título | Data | Sim | |
| 2 | `content_group` | Grupo de Conteúdo | Link → GF Content Group | Sim | |
| 3 | `access_group` | Grupo de Acesso | Link → GF Access Group | Sim | pré-preenchido via content_group.default_access_group, editável |
| 4 | `item_type` | Tipo do Item | Select | Sim | ver lista abaixo |
| 5 | `reference_doctype` | DocType de Referência | Data | Não | |
| 6 | `reference_name` | Nome de Referência | Data | Não | |
| 7 | `route_url` | URL / Rota | Data | Não | ex: /app/query-report/timesheet ou https://greenfarms.com.br |
| 8 | `description` | Descrição | Small Text | Não | |
| 9 | `icon` | Ícone | Data | Não | |
| 10 | `color` | Cor | Data | Não | |
| 11 | `tags` | Tags | Small Text | Não | |
| 12 | `responsible_user` | Responsável | Link → User | Não | auditoria e gestão |
| 13 | `status` | Status | Select | — | Default: ACTIVE |
| 14 | `sort_order` | Ordem | Int | Não | |
| 15 | `show_on_home` | Exibir na Home | Check | — | Default: 0 |
| 16 | `favorite` | Favorito | Check | — | Default: 0 |
| 17 | `active` | Ativo | Check | — | Default: 1 |

### Valores de `item_type`

```
WEB_PAGE
REPORT
DASHBOARD
PDF
HTML
DOCUMENT
APPLICATION
WORKFLOW
EXTERNAL_LINK
API
SCRIPT
OTHER
```

### Valores de `status`

```
DRAFT
ACTIVE
ARCHIVED
OBSOLETE
```

### Lógica de preenchimento automático — Client Script

Ao selecionar `content_group`, o sistema deve buscar o campo `default_access_group`
do GF Content Group selecionado e preencher automaticamente o campo `access_group`.
Implementar via `frappe.ui.form.on('GF Content Registry', { content_group: ... })`.
O campo `access_group` permanece editável para permitir exceções por item.

---

## PERMISSÕES — ROLES DO APP

As roles abaixo devem ser criadas pelo app:

| Role | Permissões |
|------|-----------|
| GF Manager | Criar, editar, excluir em todos os 4 Doctypes |
| GF Editor | Criar e editar GF Content Registry; leitura em GF Content Group e GF Access Group |
| GF Viewer | Somente leitura em GF Content Registry |

System Manager do ERPNext mantém acesso total.

---

## EXEMPLOS DE USO

**Exemplo 1 — Documento técnico restrito**
```
title:          Manual Projeto Yellow
content_group:  12 Projetos Especiais > Projeto Yellow
access_group:   ENGENHARIA
item_type:      DOCUMENT
```
Resultado: somente usuários do grupo ENGENHARIA visualizam.

**Exemplo 2 — Relatório confidencial**
```
title:          Fluxo de Caixa Estratégico
content_group:  07 Financeiro > Fluxo de Caixa
access_group:   DIRETORIA
item_type:      REPORT
```
Resultado: somente usuários do grupo DIRETORIA visualizam.

**Exemplo 3 — Link externo público**
```
title:          Website GREENFARMS
content_group:  10 Marketing e Comunicação > Site e Conteúdos Web
access_group:   PUBLICO
item_type:      EXTERNAL_LINK
route_url:      https://greenfarms.com.br
```
Resultado: todos os usuários do grupo PUBLICO acessam.

---

## POPULARIZAÇÃO AUTOMÁTICA — GF Access Group

Criar automaticamente na instalação. Regras:
- `internal_name`: sem acentos, lowercase, underscore
- `display_name`: com acentos, amigável
- `system_group = 1`
- `active = 1`
- `is_restricted = 1` para: DIRETORIA, JURIDICO, CONTROLADORIA, AUDITORIA, ADMINISTRADOR
- `is_external = 1` para: PUBLICO, VISITANTE, TERCEIRIZADO, CONSULTORIA, CLIENTE, FORNECEDOR
- `is_internal = 1` para todos os demais

| internal_name | display_name |
|---|---|
| publico | Público |
| visitante | Visitante |
| terceirizado | Terceirizado |
| consultoria | Consultoria |
| cliente | Cliente |
| fornecedor | Fornecedor |
| engenharia | Engenharia |
| automacao | Automação |
| producao | Produção |
| qualidade | Qualidade |
| manutencao | Manutenção |
| suprimentos | Suprimentos |
| logistica | Logística |
| financeiro | Financeiro |
| comercial | Comercial |
| rh | Recursos Humanos |
| marketing | Marketing |
| ti | Tecnologia da Informação |
| erpnext | ERPNext |
| ia_e_automacoes | IA e Automações |
| gerencia | Gerência |
| diretoria | Diretoria |
| administrador | Administrador |
| juridico | Jurídico |
| controladoria | Controladoria |
| auditoria | Auditoria |
| seguranca_do_trabalho | Segurança do Trabalho |
| pesquisa_e_desenvolvimento | Pesquisa e Desenvolvimento |
| laboratorio | Laboratório |
| processos_industriais | Processos Industriais |
| integracoes | Integrações |
| dashboards | Dashboards |
| web_applications | Web Applications |
| documentacoes | Documentações |
| projetos_especiais | Projetos Especiais |
| arquivo_morto | Arquivo Morto |
| obsoleto | Obsoleto |

---

## POPULARIZAÇÃO AUTOMÁTICA — GF Content Group

Criar automaticamente na instalação a estrutura hierárquica oficial corporativa.
Regras de nomenclatura: `internal_name` sem acentos/underscore; `display_name` amigável.

```
GREENFARMS DOCUMENTAÇÃO CORPORATIVA  (raiz)

00 Governança e Administração
  ├── Contratos Sociais e Documentos da Empresa
  ├── Procurações e Autorizações
  ├── Políticas Internas
  ├── Atas e Reuniões
  └── Planejamento Estratégico

01 Comercial
  ├── Clientes
  ├── Propostas Comerciais
  ├── Tabelas de Preço
  ├── Apresentações Comerciais
  ├── Follow-ups e Negociações
  └── Contratos Comerciais

02 Engenharia
  ├── Projetos Mecânicos
  ├── Projetos Elétricos
  ├── Automação e CLP
  ├── Layouts Industriais
  ├── Memoriais Descritivos
  ├── Cálculos Técnicos
  └── Revisões de Projeto

03 Produtos e Equipamentos
  ├── Biorreatores
  ├── Cisalhadores
  ├── Spray Heads e CIP
  ├── Skids
  ├── Tanques e Vasos de Pressão
  ├── Plantas Piloto
  └── Componentes Sanitários

04 Produção e Fabricação
  ├── Ordens de Produção
  ├── Desenhos para Fabricação
  ├── Usinagem
  ├── Soldagem
  ├── Polimento e Acabamento
  ├── Montagem
  └── Inspeção Final

05 Qualidade
  ├── Procedimentos Operacionais Padrão
  ├── Checklists
  ├── Relatórios de Inspeção
  ├── Certificados de Materiais
  ├── Rastreabilidade
  ├── Não Conformidades
  └── Melhoria Contínua

06 Compras e Suprimentos
  ├── Solicitações de Compra
  ├── Cotações de Fornecedores
  ├── Pedidos de Compra
  ├── Fornecedores Homologados
  ├── Materiais Críticos
  └── Notas e Comprovantes

07 Financeiro
  ├── Contas a Pagar
  ├── Contas a Receber
  ├── Fluxo de Caixa
  ├── Custos de Projetos
  ├── Investimentos
  ├── Impostos e Obrigações
  └── Relatórios Financeiros

08 Jurídico e Compliance
  ├── Contratos
  ├── Notificações
  ├── Propriedade Intelectual
  ├── Marcas e Registros
  ├── Termos de Confidencialidade
  └── Documentos Legais

09 Recursos Humanos
  ├── Colaboradores
  ├── Prestadores de Serviço
  ├── Treinamentos
  ├── Funções e Responsabilidades
  ├── Segurança do Trabalho
  └── Políticas de Conduta

10 Marketing e Comunicação
  ├── Identidade Visual
  ├── Logotipos
  ├── Fotos de Produtos
  ├── Catálogos
  ├── Site e Conteúdos Web
  ├── Redes Sociais
  └── Apresentações Institucionais

11 Tecnologia e ERPNext
  ├── ERPNext
  ├── Frappe Cloud
  ├── Aplicativo ICHIS
  ├── Relatórios Customizados
  ├── Scripts e Customizações
  ├── Backups e Segurança
  └── Manuais Internos do Sistema

12 Projetos Especiais
  ├── Projeto Yellow
  ├── AlphaBlade
  ├── Plantas Piloto
  ├── Desenvolvimento de Produtos
  ├── Pesquisa e Inovação
  └── Projetos Encerrados

13 Clientes e Obras
  ├── Clientes Ativos
  ├── Histórico de Projetos
  ├── Instalações em Campo
  ├── Assistência Técnica
  ├── Entregas Técnicas
  └── Pós-venda

14 Manuais Técnicos
  ├── Manuais de Equipamentos
  ├── Manuais de Operação
  ├── Manuais de Manutenção
  ├── Manuais de CIP e SIP
  ├── Manuais de Automação
  └── Documentação para Clientes

15 Biblioteca Técnica
  ├── Normas Técnicas
  ├── Artigos e Estudos
  ├── Catálogos de Fornecedores
  ├── Materiais de Referência
  ├── Tabelas Técnicas
  └── Conteúdos de Treinamento

80 Informações Pessoa Física
  ├── 00 Documentos Pessoais
  │     ├── RG, CPF e CNH
  │     ├── Certidões
  │     ├── Passaporte e Vistos
  │     ├── Comprovantes de Endereço
  │     ├── Títulos e Registros
  │     └── Documentos Digitalizados
  ├── 01 Família
  │     ├── Documentos da Esposa
  │     ├── Documentos dos Filhos
  │     ├── Certidões da Família
  │     ├── Escola e Educação
  │     ├── Viagens em Família
  │     └── Registros Importantes
  ├── 02 Imóveis e Patrimônio
  │     ├── Escrituras
  │     ├── Contratos de Compra e Venda
  │     ├── IPTU
  │     ├── Condomínio
  │     ├── Reformas e Manutenções
  │     ├── Fotos dos Imóveis
  │     └── Documentos de Regularização
  ├── 03 Veículos
  │     ├── Documentos dos Veículos
  │     ├── Seguro
  │     ├── IPVA
  │     ├── Multas e Taxas
  │     ├── Manutenções
  │     ├── Fotos dos Veículos
  │     └── Compra e Venda
  ├── 04 Saúde e Medicina
  │     ├── Exames Médicos
  │     ├── Consultas Médicas
  │     ├── Receitas e Prescrições
  │     ├── Histórico de Saúde
  │     ├── Planos de Saúde
  │     ├── Odontologia
  │     ├── Vacinas
  │     ├── Cirurgias e Procedimentos
  │     └── Emergências
  ├── 05 Financeiro Pessoal
  │     ├── Bancos
  │     ├── Cartões
  │     ├── Investimentos
  │     ├── Empréstimos e Financiamentos
  │     ├── Imposto de Renda
  │     ├── Comprovantes de Pagamento
  │     ├── Recibos
  │     └── Planejamento Financeiro
  ├── 06 Seguros
  │     ├── Seguro de Vida
  │     ├── Seguro Residencial
  │     ├── Seguro de Veículos
  │     ├── Seguro Saúde
  │     ├── Seguro Empresarial Pessoal
  │     ├── Apólices
  │     └── Sinistros
  ├── 07 Jurídico Pessoal
  │     ├── Contratos Pessoais
  │     ├── Procurações
  │     ├── Declarações
  │     ├── Inventário e Testamento
  │     ├── Processos
  │     ├── Notificações
  │     └── Acordos
  ├── 08 Fotos e Memórias
  │     ├── Fotos Pessoais
  │     ├── Fotos da Família
  │     ├── Fotos de Viagens
  │     ├── Eventos e Comemorações
  │     ├── Vídeos Pessoais
  │     ├── Documentos Históricos
  │     └── Memórias da Vida
  ├── 09 Viagens e Lazer
  │     ├── Reservas
  │     ├── Passagens
  │     ├── Hospedagens
  │     ├── Roteiros
  │     ├── Documentos de Viagem
  │     ├── Fotos de Viagens
  │     └── Comprovantes
  ├── 10 Educação e Formação
  │     ├── Cursos
  │     ├── Certificados
  │     ├── Diplomas
  │     ├── Treinamentos
  │     ├── Palestras
  │     └── Materiais de Estudo
  ├── 11 Senhas e Acessos
  │     ├── Contas Importantes
  │     ├── Acessos Bancários
  │     ├── Acessos Governamentais
  │     ├── Acessos de Sistemas
  │     ├── Recuperação de Contas
  │     └── Observações de Segurança
  ├── 12 Projetos Pessoais
  │     ├── Ideias
  │     ├── Planejamento
  │     ├── Documentos
  │     ├── Fotos
  │     ├── Referências
  │     └── Histórico
  ├── 13 Espiritualidade e Vida Pessoal
  │     ├── Reflexões
  │     ├── Mensagens
  │     ├── Orações
  │     ├── Registros Especiais
  │     └── Textos Pessoais
  └── 14 Arquivo Pessoal
        ├── Documentos Antigos
        ├── Fotos Antigas
        ├── Registros Antigos
        ├── Arquivos Obsoletos
        └── Histórico Geral

99 Arquivo Morto
  ├── Documentos Antigos
  ├── Projetos Encerrados
  ├── Versões Obsoletas
  ├── Propostas Perdidas
  └── Histórico Geral
```

---

## REGRAS TÉCNICAS

- Compatível com ERPNext/Frappe Cloud
- Seguir boas práticas do Frappe Framework
- Nomes limpos e estáveis (sem renomeações futuras)
- Hooks e patches de instalação via `after_install`
- Não duplicar registros na reinstalação
- Não sobrescrever registros existentes
- Usar `Link → User` obrigatoriamente (nunca campo texto livre para usuário)
- Arquitetura preparada para expansão futura (frontend, Wiki, portal)

---

## RESULTADO ESPERADO

Ao finalizar esta versão o app deve entregar:

1. Estrutura completa do app compatível com Frappe Cloud
2. 4 Doctypes funcionais com todos os campos e relacionamentos
3. Padrão `internal_name` / `display_name` em GF Content Group e GF Access Group
4. `default_access_group` no GF Content Group para pré-preenchimento no Registry
5. `access_group` no GF Content Registry pré-preenchido via client script, editável
6. `responsible_user` no GF Content Registry para auditoria
7. 3 roles corporativas criadas (GF Manager, GF Editor, GF Viewer)
8. Permissões configuradas por role
9. 37 Access Groups populados automaticamente no install
10. Estrutura hierárquica completa de Content Groups populada no install (17 grupos raiz + subcategorias, incluindo 80 Informações Pessoa Física com 15 subcategorias e seus itens)
11. Código organizado, sem configuração manual após instalação
12. Base sólida e escalável para as próximas fases (frontend, Wiki, portal)
