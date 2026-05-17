import frappe


def after_install():
    create_roles()
    create_access_groups()
    create_content_groups()
    create_web_page_custom_fields()
    frappe.db.commit()
    print("GF Atlas App: instalação concluída com sucesso.")


# ─────────────────────────────────────────────────────────────────────────────
# ROLES
# ─────────────────────────────────────────────────────────────────────────────

def create_roles():
    for role_name in ["GF Manager", "GF Editor", "GF Viewer"]:
        if not frappe.db.exists("Role", role_name):
            frappe.get_doc({
                "doctype": "Role",
                "role_name": role_name,
                "desk_access": 1
            }).insert(ignore_permissions=True)
    print("GF Atlas App: roles criadas.")


# ─────────────────────────────────────────────────────────────────────────────
# GF ACCESS GROUPS
# (internal_name, display_name, is_internal, is_external, is_restricted,
#  sort_order, description)
# ─────────────────────────────────────────────────────────────────────────────

ACCESS_GROUPS = [
    # Externos
    ("publico",               "Público",                    0, 1, 0,  1,  "Acesso público geral"),
    ("visitante",             "Visitante",                  0, 1, 0,  2,  "Visitantes sem vínculo formal"),
    ("terceirizado",          "Terceirizado",               0, 1, 0,  3,  "Prestadores de serviço terceirizados"),
    ("consultoria",           "Consultoria",                0, 1, 0,  4,  "Consultores e assessores externos"),
    ("cliente",               "Cliente",                    0, 1, 0,  5,  "Clientes da GREENFARMS"),
    ("fornecedor",            "Fornecedor",                 0, 1, 0,  6,  "Fornecedores homologados"),
    # Operacional
    ("engenharia",            "Engenharia",                 1, 0, 0, 10,  "Equipe de engenharia"),
    ("automacao",             "Automação",                  1, 0, 0, 11,  "Equipe de automação e CLP"),
    ("producao",              "Produção",                   1, 0, 0, 12,  "Equipe de produção e fabricação"),
    ("qualidade",             "Qualidade",                  1, 0, 0, 13,  "Equipe de qualidade e inspeção"),
    ("manutencao",            "Manutenção",                 1, 0, 0, 14,  "Equipe de manutenção industrial"),
    ("suprimentos",           "Suprimentos",                1, 0, 0, 15,  "Compras e suprimentos"),
    ("logistica",             "Logística",                  1, 0, 0, 16,  "Logística e expedição"),
    # Administrativo
    ("financeiro",            "Financeiro",                 1, 0, 0, 20,  "Equipe financeira"),
    ("comercial",             "Comercial",                  1, 0, 0, 21,  "Equipe comercial e vendas"),
    ("rh",                    "Recursos Humanos",           1, 0, 0, 22,  "Gestão de pessoas"),
    ("marketing",             "Marketing",                  1, 0, 0, 23,  "Marketing e comunicação"),
    ("ti",                    "Tecnologia da Informação",   1, 0, 0, 24,  "TI e infraestrutura"),
    ("erpnext",               "ERPNext",                    1, 0, 0, 25,  "Gestores e usuários do ERPNext"),
    ("ia_e_automacoes",       "IA e Automações",            1, 0, 0, 26,  "Projetos de IA e automações digitais"),
    # Gestão
    ("gerencia",              "Gerência",                   1, 0, 0, 30,  "Nível gerencial"),
    ("diretoria",             "Diretoria",                  1, 0, 1, 31,  "Diretoria executiva — acesso restrito"),
    ("administrador",         "Administrador",              1, 0, 1, 32,  "Administrador do sistema — acesso restrito"),
    # Compliance e Jurídico
    ("juridico",              "Jurídico",                   1, 0, 1, 40,  "Equipe jurídica — acesso restrito"),
    ("controladoria",         "Controladoria",              1, 0, 1, 41,  "Controladoria — acesso restrito"),
    ("auditoria",             "Auditoria",                  1, 0, 1, 42,  "Auditoria interna e externa — acesso restrito"),
    ("seguranca_do_trabalho", "Segurança do Trabalho",      1, 0, 0, 43,  "Segurança do trabalho e CIPA"),
    # Técnico / P&D
    ("pesquisa_e_desenvolvimento", "Pesquisa e Desenvolvimento", 1, 0, 0, 50, "P&D e inovação"),
    ("laboratorio",           "Laboratório",                1, 0, 0, 51,  "Laboratório técnico"),
    ("processos_industriais", "Processos Industriais",      1, 0, 0, 52,  "Engenharia de processos"),
    # Digital
    ("integracoes",           "Integrações",                1, 0, 0, 60,  "APIs e integrações de sistemas"),
    ("dashboards",            "Dashboards",                 1, 0, 0, 61,  "Painéis e dashboards corporativos"),
    ("web_applications",      "Web Applications",           1, 0, 0, 62,  "Aplicações web internas"),
    ("documentacoes",         "Documentações",              1, 0, 0, 63,  "Acesso à base de documentação"),
    ("projetos_especiais",    "Projetos Especiais",         1, 0, 0, 64,  "Projetos especiais e confidenciais"),
    # Arquivo
    ("arquivo_morto",         "Arquivo Morto",              1, 0, 0, 90,  "Documentos arquivados"),
    ("obsoleto",              "Obsoleto",                   1, 0, 0, 91,  "Conteúdos obsoletos"),
]


def create_access_groups():
    for (internal_name, display_name, is_internal, is_external,
         is_restricted, sort_order, description) in ACCESS_GROUPS:
        if not frappe.db.exists("GF Access Group", internal_name):
            frappe.get_doc({
                "doctype": "GF Access Group",
                "internal_name": internal_name,
                "display_name": display_name,
                "is_internal": is_internal,
                "is_external": is_external,
                "is_restricted": is_restricted,
                "system_group": 1,
                "active": 1,
                "sort_order": sort_order,
                "description": description
            }).insert(ignore_permissions=True)
    print(f"GF Atlas App: {len(ACCESS_GROUPS)} grupos de acesso criados.")


# ─────────────────────────────────────────────────────────────────────────────
# GF CONTENT GROUPS
# (internal_name, display_name, parent_internal_name, is_group,
#  sort_order, icon, color)
#
# icon  → nome do ícone Lucide Icons (https://lucide.dev/icons)
#         Renderizado no Knowledge Hub via data-lucide="nome" + lucide.createIcons()
#         O frontend aplica a cor de fundo do grupo e renderiza o SVG em branco.
# color → hex (#rrggbb) — cor do card/badge no Knowledge Hub
# ─────────────────────────────────────────────────────────────────────────────

CONTENT_GROUPS = [
    # ── RAIZ
    ("greenfarms_corp", "GREENFARMS Documentação Corporativa", None,           1,  0, "building-2",   "#166534"),

    # ── NÍVEL 1 — grupos principais
    ("g00", "00 Governança e Administração", "greenfarms_corp", 1,  0, "landmark",      "#6366f1"),
    ("g01", "01 Comercial",                  "greenfarms_corp", 1,  1, "briefcase",     "#f59e0b"),
    ("g02", "02 Engenharia",                 "greenfarms_corp", 1,  2, "settings-2",    "#3b82f6"),
    ("g03", "03 Produtos e Equipamentos",    "greenfarms_corp", 1,  3, "package",        "#8b5cf6"),
    ("g04", "04 Produção e Fabricação",      "greenfarms_corp", 1,  4, "factory",        "#f97316"),
    ("g05", "05 Qualidade",                  "greenfarms_corp", 1,  5, "shield-check",   "#22c55e"),
    ("g06", "06 Compras e Suprimentos",      "greenfarms_corp", 1,  6, "shopping-cart",  "#06b6d4"),
    ("g07", "07 Financeiro",                 "greenfarms_corp", 1,  7, "banknote",       "#eab308"),
    ("g08", "08 Jurídico e Compliance",      "greenfarms_corp", 1,  8, "scale",          "#dc2626"),
    ("g09", "09 Recursos Humanos",           "greenfarms_corp", 1,  9, "users",          "#ec4899"),
    ("g10", "10 Marketing e Comunicação",    "greenfarms_corp", 1, 10, "megaphone",      "#a855f7"),
    ("g11", "11 Tecnologia e ERPNext",       "greenfarms_corp", 1, 11, "monitor",        "#0ea5e9"),
    ("g12", "12 Projetos Especiais",         "greenfarms_corp", 1, 12, "rocket",         "#f43f5e"),
    ("g13", "13 Clientes e Obras",           "greenfarms_corp", 1, 13, "hard-hat",       "#14b8a6"),
    ("g14", "14 Manuais Técnicos",           "greenfarms_corp", 1, 14, "book-open",      "#64748b"),
    ("g15", "15 Biblioteca Técnica",         "greenfarms_corp", 1, 15, "library",        "#78716c"),
    ("g80", "80 Informações Pessoa Física",  "greenfarms_corp", 1, 80, "user",           "#84cc16"),
    ("g99", "99 Arquivo Morto",              "greenfarms_corp", 1, 99, "archive",        "#6b7280"),

    # ── g00 Governança e Administração
    ("g00_contratos_sociais", "Contratos Sociais e Documentos da Empresa", "g00", 0, 0, "file-text",      ""),
    ("g00_procuracoes",       "Procurações e Autorizações",                "g00", 0, 1, "pen-line",       ""),
    ("g00_politicas",         "Políticas Internas",                        "g00", 0, 2, "scroll",         ""),
    ("g00_atas",              "Atas e Reuniões",                           "g00", 0, 3, "clipboard",      ""),
    ("g00_planejamento",      "Planejamento Estratégico",                  "g00", 0, 4, "target",         ""),

    # ── g01 Comercial
    ("g01_clientes",          "Clientes",                  "g01", 0, 0, "users",          ""),
    ("g01_propostas",         "Propostas Comerciais",      "g01", 0, 1, "file-plus",      ""),
    ("g01_tabelas_preco",     "Tabelas de Preço",          "g01", 0, 2, "tag",            ""),
    ("g01_apresentacoes",     "Apresentações Comerciais",  "g01", 0, 3, "monitor",        ""),
    ("g01_followups",         "Follow-ups e Negociações",  "g01", 0, 4, "phone-call",     ""),
    ("g01_contratos",         "Contratos Comerciais",      "g01", 0, 5, "file-check",     ""),

    # ── g02 Engenharia
    ("g02_proj_mecanicos",    "Projetos Mecânicos",        "g02", 0, 0, "wrench",         ""),
    ("g02_proj_eletricos",    "Projetos Elétricos",        "g02", 0, 1, "zap",            ""),
    ("g02_automacao",         "Automação e CLP",           "g02", 0, 2, "cpu",            ""),
    ("g02_layouts",           "Layouts Industriais",       "g02", 0, 3, "layout",         ""),
    ("g02_memoriais",         "Memoriais Descritivos",     "g02", 0, 4, "file-text",      ""),
    ("g02_calculos",          "Cálculos Técnicos",         "g02", 0, 5, "bar-chart-2",    ""),
    ("g02_revisoes",          "Revisões de Projeto",       "g02", 0, 6, "refresh-cw",     ""),

    # ── g03 Produtos e Equipamentos
    ("g03_biorreatores",      "Biorreatores",              "g03", 0, 0, "flask-conical",  ""),
    ("g03_cisalhadores",      "Cisalhadores",              "g03", 0, 1, "settings-2",     ""),
    ("g03_spray_heads",       "Spray Heads e CIP",         "g03", 0, 2, "droplets",       ""),
    ("g03_skids",             "Skids",                     "g03", 0, 3, "layers",         ""),
    ("g03_tanques",           "Tanques e Vasos de Pressão","g03", 0, 4, "database",       ""),
    ("g03_plantas_piloto",    "Plantas Piloto",            "g03", 0, 5, "leaf",           ""),
    ("g03_componentes",       "Componentes Sanitários",    "g03", 0, 6, "link",           ""),

    # ── g04 Produção e Fabricação
    ("g04_ordens",            "Ordens de Produção",        "g04", 0, 0, "clipboard-list", ""),
    ("g04_desenhos_fab",      "Desenhos para Fabricação",  "g04", 0, 1, "pen-tool",       ""),
    ("g04_usinagem",          "Usinagem",                  "g04", 0, 2, "settings",       ""),
    ("g04_soldagem",          "Soldagem",                  "g04", 0, 3, "zap",            ""),
    ("g04_polimento",         "Polimento e Acabamento",    "g04", 0, 4, "sparkles",       ""),
    ("g04_montagem",          "Montagem",                  "g04", 0, 5, "wrench",         ""),
    ("g04_inspecao",          "Inspeção Final",            "g04", 0, 6, "search",         ""),

    # ── g05 Qualidade
    ("g05_pop",               "Procedimentos Operacionais Padrão", "g05", 0, 0, "clipboard-list",  ""),
    ("g05_checklists",        "Checklists",                "g05", 0, 1, "check-square",   ""),
    ("g05_relatorios",        "Relatórios de Inspeção",    "g05", 0, 2, "bar-chart",      ""),
    ("g05_certificados",      "Certificados de Materiais", "g05", 0, 3, "award",          ""),
    ("g05_rastreabilidade",   "Rastreabilidade",           "g05", 0, 4, "search",         ""),
    ("g05_nao_conformidades", "Não Conformidades",         "g05", 0, 5, "alert-triangle", ""),
    ("g05_melhoria",          "Melhoria Contínua",         "g05", 0, 6, "trending-up",    ""),

    # ── g06 Compras e Suprimentos
    ("g06_solicitacoes",      "Solicitações de Compra",    "g06", 0, 0, "shopping-cart",  ""),
    ("g06_cotacoes",          "Cotações de Fornecedores",  "g06", 0, 1, "message-circle", ""),
    ("g06_pedidos",           "Pedidos de Compra",         "g06", 0, 2, "package",        ""),
    ("g06_fornecedores",      "Fornecedores Homologados",  "g06", 0, 3, "building",       ""),
    ("g06_materiais_criticos","Materiais Críticos",        "g06", 0, 4, "alert-triangle", ""),
    ("g06_notas",             "Notas e Comprovantes",      "g06", 0, 5, "receipt",        ""),

    # ── g07 Financeiro
    ("g07_contas_pagar",      "Contas a Pagar",            "g07", 0, 0, "trending-down",  ""),
    ("g07_contas_receber",    "Contas a Receber",          "g07", 0, 1, "trending-up",    ""),
    ("g07_fluxo_caixa",       "Fluxo de Caixa",            "g07", 0, 2, "activity",       ""),
    ("g07_custos_proj",       "Custos de Projetos",        "g07", 0, 3, "bar-chart-2",    ""),
    ("g07_investimentos",     "Investimentos",             "g07", 0, 4, "line-chart",     ""),
    ("g07_impostos",          "Impostos e Obrigações",     "g07", 0, 5, "landmark",       ""),
    ("g07_relatorios",        "Relatórios Financeiros",    "g07", 0, 6, "pie-chart",      ""),

    # ── g08 Jurídico e Compliance
    ("g08_contratos",         "Contratos",                 "g08", 0, 0, "file-text",      ""),
    ("g08_notificacoes",      "Notificações",              "g08", 0, 1, "bell",           ""),
    ("g08_propriedade",       "Propriedade Intelectual",   "g08", 0, 2, "lightbulb",      ""),
    ("g08_marcas",            "Marcas e Registros",        "g08", 0, 3, "badge",          ""),
    ("g08_nda",               "Termos de Confidencialidade","g08",0, 4, "lock",           ""),
    ("g08_docs_legais",       "Documentos Legais",         "g08", 0, 5, "scroll",         ""),

    # ── g09 Recursos Humanos
    ("g09_colaboradores",     "Colaboradores",             "g09", 0, 0, "user",           ""),
    ("g09_prestadores",       "Prestadores de Serviço",    "g09", 0, 1, "handshake",      ""),
    ("g09_treinamentos",      "Treinamentos",              "g09", 0, 2, "graduation-cap", ""),
    ("g09_funcoes",           "Funções e Responsabilidades","g09",0, 3, "clipboard",      ""),
    ("g09_sst",               "Segurança do Trabalho",     "g09", 0, 4, "shield",         ""),
    ("g09_conduta",           "Políticas de Conduta",      "g09", 0, 5, "scroll",         ""),

    # ── g10 Marketing e Comunicação
    ("g10_identidade",        "Identidade Visual",         "g10", 0, 0, "palette",        ""),
    ("g10_logotipos",         "Logotipos",                 "g10", 0, 1, "image",          ""),
    ("g10_fotos_prod",        "Fotos de Produtos",         "g10", 0, 2, "camera",         ""),
    ("g10_catalogos",         "Catálogos",                 "g10", 0, 3, "book",           ""),
    ("g10_site",              "Site e Conteúdos Web",      "g10", 0, 4, "globe",          ""),
    ("g10_redes_sociais",     "Redes Sociais",             "g10", 0, 5, "share-2",        ""),
    ("g10_apresentacoes",     "Apresentações Institucionais","g10",0, 6, "presentation",  ""),

    # ── g11 Tecnologia e ERPNext
    ("g11_erpnext",           "ERPNext",                   "g11", 0, 0, "layers",         ""),
    ("g11_frappe_cloud",      "Frappe Cloud",              "g11", 0, 1, "cloud",          ""),
    ("g11_ichis",             "Aplicativo ICHIS",          "g11", 0, 2, "smartphone",     ""),
    ("g11_relatorios",        "Relatórios Customizados",   "g11", 0, 3, "bar-chart",      ""),
    ("g11_scripts",           "Scripts e Customizações",   "g11", 0, 4, "terminal",       ""),
    ("g11_backups",           "Backups e Segurança",       "g11", 0, 5, "shield",         ""),
    ("g11_manuais_sis",       "Manuais Internos do Sistema","g11",0, 6, "book-open",      ""),

    # ── g12 Projetos Especiais
    ("g12_yellow",            "Projeto Yellow",            "g12", 0, 0, "sun",            ""),
    ("g12_alphablade",        "AlphaBlade",                "g12", 0, 1, "zap",            ""),
    ("g12_plantas_piloto",    "Plantas Piloto",            "g12", 0, 2, "leaf",           ""),
    ("g12_dev_produtos",      "Desenvolvimento de Produtos","g12",0, 3, "flask-conical",  ""),
    ("g12_pesquisa",          "Pesquisa e Inovação",       "g12", 0, 4, "microscope",     ""),
    ("g12_encerrados",        "Projetos Encerrados",       "g12", 0, 5, "check-circle",   ""),

    # ── g13 Clientes e Obras
    ("g13_clientes_ativos",   "Clientes Ativos",           "g13", 0, 0, "users",          ""),
    ("g13_historico_proj",    "Histórico de Projetos",     "g13", 0, 1, "clock",          ""),
    ("g13_instalacoes",       "Instalações em Campo",      "g13", 0, 2, "map-pin",        ""),
    ("g13_assistencia",       "Assistência Técnica",       "g13", 0, 3, "wrench",         ""),
    ("g13_entregas",          "Entregas Técnicas",         "g13", 0, 4, "package",        ""),
    ("g13_pos_venda",         "Pós-venda",                 "g13", 0, 5, "star",           ""),

    # ── g14 Manuais Técnicos
    ("g14_equipamentos",      "Manuais de Equipamentos",   "g14", 0, 0, "settings-2",     ""),
    ("g14_operacao",          "Manuais de Operação",       "g14", 0, 1, "play-circle",    ""),
    ("g14_manutencao",        "Manuais de Manutenção",     "g14", 0, 2, "wrench",         ""),
    ("g14_cip_sip",           "Manuais de CIP e SIP",      "g14", 0, 3, "droplets",       ""),
    ("g14_automacao",         "Manuais de Automação",      "g14", 0, 4, "cpu",            ""),
    ("g14_doc_clientes",      "Documentação para Clientes","g14", 0, 5, "file-text",      ""),

    # ── g15 Biblioteca Técnica
    ("g15_normas",            "Normas Técnicas",           "g15", 0, 0, "ruler",          ""),
    ("g15_artigos",           "Artigos e Estudos",         "g15", 0, 1, "newspaper",      ""),
    ("g15_catalogos_forn",    "Catálogos de Fornecedores", "g15", 0, 2, "book",           ""),
    ("g15_referencias",       "Materiais de Referência",   "g15", 0, 3, "link",           ""),
    ("g15_tabelas",           "Tabelas Técnicas",          "g15", 0, 4, "table",          ""),
    ("g15_treinamentos",      "Conteúdos de Treinamento",  "g15", 0, 5, "graduation-cap", ""),

    # ══ g80 Informações Pessoa Física ══════════════════════════════════════
    # Nível 2 — cada subcategoria tem ícone e cor próprios
    ("g80_00", "00 Documentos Pessoais",        "g80", 1,  0, "credit-card",    "#6366f1"),
    ("g80_01", "01 Família",                    "g80", 1,  1, "heart",          "#ec4899"),
    ("g80_02", "02 Imóveis e Patrimônio",       "g80", 1,  2, "home",           "#f59e0b"),
    ("g80_03", "03 Veículos",                   "g80", 1,  3, "car",            "#3b82f6"),
    ("g80_04", "04 Saúde e Medicina",           "g80", 1,  4, "heart-pulse",    "#dc2626"),
    ("g80_05", "05 Financeiro Pessoal",         "g80", 1,  5, "wallet",         "#eab308"),
    ("g80_06", "06 Seguros",                    "g80", 1,  6, "shield",         "#8b5cf6"),
    ("g80_07", "07 Jurídico Pessoal",           "g80", 1,  7, "scale",          "#f97316"),
    ("g80_08", "08 Fotos e Memórias",           "g80", 1,  8, "camera",         "#a855f7"),
    ("g80_09", "09 Viagens e Lazer",            "g80", 1,  9, "plane",          "#0ea5e9"),
    ("g80_10", "10 Educação e Formação",        "g80", 1, 10, "graduation-cap", "#22c55e"),
    ("g80_11", "11 Senhas e Acessos",           "g80", 1, 11, "lock",           "#64748b"),
    ("g80_12", "12 Projetos Pessoais",          "g80", 1, 12, "lightbulb",      "#f43f5e"),
    ("g80_13", "13 Espiritualidade e Vida Pessoal", "g80", 1, 13, "sun",        "#84cc16"),
    ("g80_14", "14 Arquivo Pessoal",            "g80", 1, 14, "archive",        "#6b7280"),

    # g80_00 Documentos Pessoais
    ("g80_00_rg_cpf_cnh",    "RG, CPF e CNH",             "g80_00", 0, 0, "credit-card",    ""),
    ("g80_00_certidoes",     "Certidões",                  "g80_00", 0, 1, "scroll",         ""),
    ("g80_00_passaporte",    "Passaporte e Vistos",        "g80_00", 0, 2, "stamp",          ""),
    ("g80_00_comprovantes",  "Comprovantes de Endereço",   "g80_00", 0, 3, "home",           ""),
    ("g80_00_titulos",       "Títulos e Registros",        "g80_00", 0, 4, "file-text",      ""),
    ("g80_00_digitalizados", "Documentos Digitalizados",   "g80_00", 0, 5, "scan",           ""),

    # g80_01 Família
    ("g80_01_esposa",        "Documentos da Esposa",       "g80_01", 0, 0, "heart",          ""),
    ("g80_01_filhos",        "Documentos dos Filhos",      "g80_01", 0, 1, "baby",           ""),
    ("g80_01_certidoes",     "Certidões da Família",       "g80_01", 0, 2, "scroll",         ""),
    ("g80_01_escola",        "Escola e Educação",          "g80_01", 0, 3, "school",         ""),
    ("g80_01_viagens",       "Viagens em Família",         "g80_01", 0, 4, "plane",          ""),
    ("g80_01_registros",     "Registros Importantes",      "g80_01", 0, 5, "star",           ""),

    # g80_02 Imóveis e Patrimônio
    ("g80_02_escrituras",    "Escrituras",                 "g80_02", 0, 0, "scroll",         ""),
    ("g80_02_contratos",     "Contratos de Compra e Venda","g80_02", 0, 1, "file-text",      ""),
    ("g80_02_iptu",          "IPTU",                       "g80_02", 0, 2, "landmark",       ""),
    ("g80_02_condominio",    "Condomínio",                 "g80_02", 0, 3, "building",       ""),
    ("g80_02_reformas",      "Reformas e Manutenções",     "g80_02", 0, 4, "hammer",         ""),
    ("g80_02_fotos",         "Fotos dos Imóveis",          "g80_02", 0, 5, "camera",         ""),
    ("g80_02_regularizacao", "Documentos de Regularização","g80_02", 0, 6, "file-check",     ""),

    # g80_03 Veículos
    ("g80_03_docs",          "Documentos dos Veículos",    "g80_03", 0, 0, "file-text",      ""),
    ("g80_03_seguro",        "Seguro",                     "g80_03", 0, 1, "shield",         ""),
    ("g80_03_ipva",          "IPVA",                       "g80_03", 0, 2, "landmark",       ""),
    ("g80_03_multas",        "Multas e Taxas",             "g80_03", 0, 3, "alert-triangle", ""),
    ("g80_03_manutencoes",   "Manutenções",                "g80_03", 0, 4, "wrench",         ""),
    ("g80_03_fotos",         "Fotos dos Veículos",         "g80_03", 0, 5, "camera",         ""),
    ("g80_03_compra_venda",  "Compra e Venda",             "g80_03", 0, 6, "handshake",      ""),

    # g80_04 Saúde e Medicina
    ("g80_04_exames",        "Exames Médicos",             "g80_04", 0, 0, "microscope",     ""),
    ("g80_04_consultas",     "Consultas Médicas",          "g80_04", 0, 1, "stethoscope",    ""),
    ("g80_04_receitas",      "Receitas e Prescrições",     "g80_04", 0, 2, "pill",           ""),
    ("g80_04_historico",     "Histórico de Saúde",         "g80_04", 0, 3, "clipboard-list", ""),
    ("g80_04_planos",        "Planos de Saúde",            "g80_04", 0, 4, "building-2",     ""),
    ("g80_04_odonto",        "Odontologia",                "g80_04", 0, 5, "smile",          ""),
    ("g80_04_vacinas",       "Vacinas",                    "g80_04", 0, 6, "syringe",        ""),
    ("g80_04_cirurgias",     "Cirurgias e Procedimentos",  "g80_04", 0, 7, "activity",       ""),
    ("g80_04_emergencias",   "Emergências",                "g80_04", 0, 8, "alert-circle",   ""),

    # g80_05 Financeiro Pessoal
    ("g80_05_bancos",        "Bancos",                     "g80_05", 0, 0, "landmark",       ""),
    ("g80_05_cartoes",       "Cartões",                    "g80_05", 0, 1, "credit-card",    ""),
    ("g80_05_investimentos", "Investimentos",              "g80_05", 0, 2, "trending-up",    ""),
    ("g80_05_emprestimos",   "Empréstimos e Financiamentos","g80_05",0, 3, "banknote",       ""),
    ("g80_05_ir",            "Imposto de Renda",           "g80_05", 0, 4, "file-text",      ""),
    ("g80_05_comprovantes",  "Comprovantes de Pagamento",  "g80_05", 0, 5, "receipt",        ""),
    ("g80_05_recibos",       "Recibos",                    "g80_05", 0, 6, "receipt",        ""),
    ("g80_05_planejamento",  "Planejamento Financeiro",    "g80_05", 0, 7, "pie-chart",      ""),

    # g80_06 Seguros
    ("g80_06_vida",          "Seguro de Vida",             "g80_06", 0, 0, "heart",          ""),
    ("g80_06_residencial",   "Seguro Residencial",         "g80_06", 0, 1, "home",           ""),
    ("g80_06_veiculos",      "Seguro de Veículos",         "g80_06", 0, 2, "car",            ""),
    ("g80_06_saude",         "Seguro Saúde",               "g80_06", 0, 3, "activity",       ""),
    ("g80_06_empresarial",   "Seguro Empresarial Pessoal", "g80_06", 0, 4, "building",       ""),
    ("g80_06_apolices",      "Apólices",                   "g80_06", 0, 5, "file-text",      ""),
    ("g80_06_sinistros",     "Sinistros",                  "g80_06", 0, 6, "alert-triangle", ""),

    # g80_07 Jurídico Pessoal
    ("g80_07_contratos",     "Contratos Pessoais",         "g80_07", 0, 0, "file-text",      ""),
    ("g80_07_procuracoes",   "Procurações",                "g80_07", 0, 1, "pen-line",       ""),
    ("g80_07_declaracoes",   "Declarações",                "g80_07", 0, 2, "file-check",     ""),
    ("g80_07_inventario",    "Inventário e Testamento",    "g80_07", 0, 3, "scroll",         ""),
    ("g80_07_processos",     "Processos",                  "g80_07", 0, 4, "scale",          ""),
    ("g80_07_notificacoes",  "Notificações",               "g80_07", 0, 5, "bell",           ""),
    ("g80_07_acordos",       "Acordos",                    "g80_07", 0, 6, "handshake",      ""),

    # g80_08 Fotos e Memórias
    ("g80_08_fotos_pessoais","Fotos Pessoais",             "g80_08", 0, 0, "camera",         ""),
    ("g80_08_fotos_familia", "Fotos da Família",           "g80_08", 0, 1, "users",          ""),
    ("g80_08_fotos_viagens", "Fotos de Viagens",           "g80_08", 0, 2, "map-pin",        ""),
    ("g80_08_eventos",       "Eventos e Comemorações",     "g80_08", 0, 3, "party-popper",   ""),
    ("g80_08_videos",        "Vídeos Pessoais",            "g80_08", 0, 4, "video",          ""),
    ("g80_08_docs_hist",     "Documentos Históricos",      "g80_08", 0, 5, "scroll",         ""),
    ("g80_08_memorias",      "Memórias da Vida",           "g80_08", 0, 6, "heart",          ""),

    # g80_09 Viagens e Lazer
    ("g80_09_reservas",      "Reservas",                   "g80_09", 0, 0, "calendar-check", ""),
    ("g80_09_passagens",     "Passagens",                  "g80_09", 0, 1, "ticket",         ""),
    ("g80_09_hospedagens",   "Hospedagens",                "g80_09", 0, 2, "bed",            ""),
    ("g80_09_roteiros",      "Roteiros",                   "g80_09", 0, 3, "map",            ""),
    ("g80_09_docs_viagem",   "Documentos de Viagem",       "g80_09", 0, 4, "folder",         ""),
    ("g80_09_fotos_viagens", "Fotos de Viagens",           "g80_09", 0, 5, "camera",         ""),
    ("g80_09_comprovantes",  "Comprovantes",               "g80_09", 0, 6, "receipt",        ""),

    # g80_10 Educação e Formação
    ("g80_10_cursos",        "Cursos",                     "g80_10", 0, 0, "book-open",      ""),
    ("g80_10_certificados",  "Certificados",               "g80_10", 0, 1, "award",          ""),
    ("g80_10_diplomas",      "Diplomas",                   "g80_10", 0, 2, "graduation-cap", ""),
    ("g80_10_treinamentos",  "Treinamentos",               "g80_10", 0, 3, "target",         ""),
    ("g80_10_palestras",     "Palestras",                  "g80_10", 0, 4, "mic",            ""),
    ("g80_10_materiais",     "Materiais de Estudo",        "g80_10", 0, 5, "library",        ""),

    # g80_11 Senhas e Acessos
    ("g80_11_contas",        "Contas Importantes",         "g80_11", 0, 0, "user",           ""),
    ("g80_11_bancarios",     "Acessos Bancários",          "g80_11", 0, 1, "landmark",       ""),
    ("g80_11_governamentais","Acessos Governamentais",     "g80_11", 0, 2, "building-2",     ""),
    ("g80_11_sistemas",      "Acessos de Sistemas",        "g80_11", 0, 3, "monitor",        ""),
    ("g80_11_recuperacao",   "Recuperação de Contas",      "g80_11", 0, 4, "key",            ""),
    ("g80_11_seguranca",     "Observações de Segurança",   "g80_11", 0, 5, "alert-triangle", ""),

    # g80_12 Projetos Pessoais
    ("g80_12_ideias",        "Ideias",                     "g80_12", 0, 0, "lightbulb",      ""),
    ("g80_12_planejamento",  "Planejamento",               "g80_12", 0, 1, "calendar",       ""),
    ("g80_12_documentos",    "Documentos",                 "g80_12", 0, 2, "file-text",      ""),
    ("g80_12_fotos",         "Fotos",                      "g80_12", 0, 3, "camera",         ""),
    ("g80_12_referencias",   "Referências",                "g80_12", 0, 4, "link",           ""),
    ("g80_12_historico",     "Histórico",                  "g80_12", 0, 5, "clock",          ""),

    # g80_13 Espiritualidade e Vida Pessoal
    ("g80_13_reflexoes",     "Reflexões",                  "g80_13", 0, 0, "brain",          ""),
    ("g80_13_mensagens",     "Mensagens",                  "g80_13", 0, 1, "message-circle", ""),
    ("g80_13_oracoes",       "Orações",                    "g80_13", 0, 2, "sun",            ""),
    ("g80_13_registros",     "Registros Especiais",        "g80_13", 0, 3, "star",           ""),
    ("g80_13_textos",        "Textos Pessoais",            "g80_13", 0, 4, "pen-line",       ""),

    # g80_14 Arquivo Pessoal
    ("g80_14_docs_antigos",     "Documentos Antigos",      "g80_14", 0, 0, "folder",         ""),
    ("g80_14_fotos_antigas",    "Fotos Antigas",           "g80_14", 0, 1, "image",          ""),
    ("g80_14_registros_antigos","Registros Antigos",       "g80_14", 0, 2, "file-text",      ""),
    ("g80_14_obsoletos",        "Arquivos Obsoletos",      "g80_14", 0, 3, "trash-2",        ""),
    ("g80_14_historico",        "Histórico Geral",         "g80_14", 0, 4, "clock",          ""),

    # ── g99 Arquivo Morto
    ("g99_docs_antigos",       "Documentos Antigos",       "g99", 0, 0, "folder",            ""),
    ("g99_proj_encerrados",    "Projetos Encerrados",      "g99", 0, 1, "check-circle",      ""),
    ("g99_versoes_obsoletas",  "Versões Obsoletas",        "g99", 0, 2, "refresh-cw",        ""),
    ("g99_propostas_perdidas", "Propostas Perdidas",       "g99", 0, 3, "trending-down",     ""),
    ("g99_historico",          "Histórico Geral",          "g99", 0, 4, "clock",             ""),
]


# ─────────────────────────────────────────────────────────────────────────────
# CUSTOM FIELDS — Web Page
# Dois blocos HTML auxiliares adicionados no final da tela de edição.
# Usados para conteúdo extra, blocos laterais, widgets, etc.
# ─────────────────────────────────────────────────────────────────────────────

def create_web_page_custom_fields():
    # Detecta o último campo existente na Web Page para inserir após ele
    meta_fields = frappe.get_meta("Web Page").fields
    last_fieldname = meta_fields[-1].fieldname if meta_fields else ""

    custom_fields = [
        {
            "fieldname": "gf_sb_auxiliary_blocks",
            "label": "Auxiliary Blocks",
            "fieldtype": "Section Break",
            "insert_after": last_fieldname,
        },
        {
            "fieldname": "auxiliary_block_1",
            "label": "Auxiliary Block 1",
            "fieldtype": "HTML Editor",
            "insert_after": "gf_sb_auxiliary_blocks",
        },
        {
            "fieldname": "auxiliary_block_2",
            "label": "Auxiliary Block 2",
            "fieldtype": "HTML Editor",
            "insert_after": "auxiliary_block_1",
        },
    ]

    for f in custom_fields:
        field_id = f"Web Page-{f['fieldname']}"
        if not frappe.db.exists("Custom Field", field_id):
            frappe.get_doc({
                "doctype": "Custom Field",
                "dt": "Web Page",
                **f
            }).insert(ignore_permissions=True)

    print("GF Atlas App: campos Auxiliary Block 1 e 2 criados em Web Page.")


def _insert_content_group(internal_name, display_name, parent_internal_name,
                           is_group, sort_order, icon, color):
    if frappe.db.exists("GF Content Group", internal_name):
        return
    frappe.get_doc({
        "doctype": "GF Content Group",
        "internal_name": internal_name,
        "display_name": display_name,
        "parent_group": parent_internal_name,
        "is_group": is_group,
        "active": 1,
        "sort_order": sort_order,
        "icon": icon,
        "color": color
    }).insert(ignore_permissions=True)


def create_content_groups():
    # Insere em 3 passagens com commit entre cada nível para garantir
    # que o nested set (lft/rgt) do pai exista antes de inserir filhos.

    # Nível 0 — raiz
    roots = [r for r in CONTENT_GROUPS if r[2] is None]
    for row in roots:
        _insert_content_group(*row)
    frappe.db.commit()

    # Nível 1 — filhos da raiz
    root_names = {r[0] for r in roots}
    level1 = [r for r in CONTENT_GROUPS if r[2] in root_names]
    for row in level1:
        _insert_content_group(*row)
    frappe.db.commit()

    # Níveis 2+ — todos os demais
    inserted = root_names | {r[0] for r in level1}
    remaining = [r for r in CONTENT_GROUPS if r[0] not in inserted]
    for row in remaining:
        _insert_content_group(*row)

    print(f"GF Atlas App: {len(CONTENT_GROUPS)} grupos de conteúdo criados.")
