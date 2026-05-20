import frappe


def after_install():
    create_roles()
    create_access_groups()
    create_content_groups()
    create_web_page_custom_fields()
    create_sample_skills()
    create_sample_content_registry()
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
#  system_group, sort_order, description)
# ─────────────────────────────────────────────────────────────────────────────

ACCESS_GROUPS = [
    # Externos
    ("publico",                   "Público",                    0, 1, 0, 0,  10,  "Acesso público geral"),
    ("visitante",                 "Visitante",                  0, 1, 0, 0,  20,  "Visitantes sem vínculo formal"),
    ("terceirizado",              "Terceirizado",               0, 1, 0, 0,  30,  "Prestadores de serviço terceirizados"),
    ("consultoria",               "Consultoria",                0, 1, 0, 0,  40,  "Consultores e assessores externos"),
    ("cliente",                   "Cliente",                    0, 1, 0, 0,  50,  "Clientes da empresa"),
    ("fornecedor",                "Fornecedor",                 0, 1, 0, 0,  60,  "Fornecedores homologados"),
    # Operacional
    ("engenharia",                "Engenharia",                 1, 0, 0, 0,  70,  "Equipe de engenharia"),
    ("engenharia_mecanica",       "Engenharia Mecânica",        1, 0, 0, 0,  80,  "Equipe de engenharia mecânica"),
    ("engenharia_eletrica",       "Engenharia Elétrica",        1, 0, 0, 0,  90,  "Equipe de engenharia elétrica"),
    ("automacao",                 "Automação",                  1, 0, 0, 0, 100,  "Equipe de automação e CLP"),
    ("producao",                  "Produção",                   1, 0, 0, 0, 110,  "Equipe de produção e fabricação"),
    ("qualidade",                 "Qualidade",                  1, 0, 0, 0, 120,  "Equipe de qualidade e inspeção"),
    ("manutencao",                "Manutenção",                 1, 0, 0, 0, 130,  "Equipe de manutenção industrial"),
    ("pcp",                       "PCP",                        1, 0, 0, 0, 140,  "Planejamento e controle da produção"),
    ("suprimentos",               "Suprimentos",                1, 0, 0, 0, 150,  "Compras e suprimentos"),
    ("comprador",                 "Comprador",                  1, 0, 0, 0, 160,  "Compradores"),
    ("logistica",                 "Logística",                  1, 0, 0, 0, 170,  "Logística e expedição"),
    ("expedicao",                 "Expedição",                  1, 0, 0, 0, 180,  "Equipe de expedição"),
    ("almoxarifado",              "Almoxarifado",               1, 0, 0, 0, 190,  "Equipe do almoxarifado"),
    ("assistencia_tecnica",       "Assistência Técnica",        1, 0, 0, 0, 200,  "Equipe de assistência técnica"),
    ("pos_venda",                 "Pós-Venda",                  1, 0, 0, 0, 210,  "Equipe de pós-venda"),
    ("processos_industriais",     "Processos Industriais",      1, 0, 0, 0, 220,  "Engenharia de processos industriais"),
    ("laboratorio",               "Laboratório",                1, 0, 0, 0, 230,  "Laboratório técnico"),
    ("pesquisa_e_desenvolvimento","Pesquisa e Desenvolvimento", 1, 0, 0, 0, 240,  "P&D e inovação"),
    # Administrativo
    ("financeiro",                "Financeiro",                 1, 0, 0, 0, 250,  "Equipe financeira"),
    ("comercial",                 "Comercial",                  1, 0, 0, 0, 260,  "Equipe comercial e vendas"),
    ("recursos_humanos",          "Recursos Humanos",           1, 0, 0, 0, 270,  "Gestão de pessoas"),
    ("marketing",                 "Marketing",                  1, 0, 0, 0, 280,  "Marketing e comunicação"),
    ("tecnologia_da_informacao",  "Tecnologia da Informação",   1, 0, 0, 0, 290,  "TI e infraestrutura"),
    # Sistema / Técnico
    ("infraestrutura",            "Infraestrutura",             1, 0, 0, 1, 300,  "Infraestrutura de TI"),
    ("devops",                    "DevOps",                     1, 0, 0, 1, 310,  "Equipe de DevOps"),
    ("cloud",                     "Cloud",                      1, 0, 0, 1, 320,  "Cloud e hospedagem"),
    ("erpnext",                   "ERPNext",                    1, 0, 0, 1, 330,  "Gestores e usuários do ERPNext"),
    ("ia_e_automacoes",           "IA e Automações",            1, 0, 0, 1, 340,  "Projetos de IA e automações digitais"),
    ("integracoes",               "Integrações",                1, 0, 0, 1, 350,  "APIs e integrações de sistemas"),
    # Digital / Conteúdo
    ("dashboards",                "Dashboards",                 1, 0, 0, 0, 360,  "Painéis e dashboards corporativos"),
    ("web_applications",          "Web Applications",           1, 0, 0, 1, 370,  "Aplicações web internas"),
    ("documentacoes",             "Documentações",              1, 0, 0, 0, 380,  "Acesso à base de documentação"),
    # Projetos / Gestão
    ("gestao_de_projetos",        "Gestão de Projetos",         1, 0, 0, 0, 390,  "Gestão de projetos"),
    ("pmo",                       "PMO",                        1, 0, 0, 0, 400,  "Project Management Office"),
    ("projetos_especiais",        "Projetos Especiais",         1, 0, 1, 0, 410,  "Projetos especiais — acesso restrito"),
    # Restritos / Gerência e Diretoria
    ("gerencia",                  "Gerência",                   1, 0, 1, 0, 420,  "Nível gerencial — acesso restrito"),
    ("diretoria",                 "Diretoria",                  1, 0, 1, 0, 430,  "Diretoria executiva — acesso restrito"),
    ("diretoria_financeira",      "Diretoria Financeira",       1, 0, 1, 0, 440,  "Diretoria financeira — acesso restrito"),
    ("diretoria_industrial",      "Diretoria Industrial",       1, 0, 1, 0, 450,  "Diretoria industrial — acesso restrito"),
    ("diretoria_comercial",       "Diretoria Comercial",        1, 0, 1, 0, 460,  "Diretoria comercial — acesso restrito"),
    ("diretoria_tecnica",         "Diretoria Técnica",          1, 0, 1, 0, 470,  "Diretoria técnica — acesso restrito"),
    ("diretoria_de_operacoes",    "Diretoria de Operações",     1, 0, 1, 0, 480,  "Diretoria de operações — acesso restrito"),
    # Sistema admin
    ("administrador",             "Administrador",              1, 0, 1, 1, 490,  "Administrador do sistema — acesso restrito"),
    ("administrador_do_hub",      "Administrador do HUB",       1, 0, 1, 1, 500,  "Administrador do HUB — acesso restrito"),
    ("curadoria",                 "Curadoria",                  1, 0, 0, 1, 510,  "Curadoria de conteúdo"),
    ("gestao_documental",         "Gestão Documental",          1, 0, 0, 1, 520,  "Gestão documental"),
    # Visualizador
    ("visualizador",              "Visualizador",               1, 0, 0, 0, 530,  "Acesso somente visualização"),
    # Compliance / Jurídico
    ("juridico",                  "Jurídico",                   1, 0, 1, 0, 540,  "Equipe jurídica — acesso restrito"),
    ("controladoria",             "Controladoria",              1, 0, 1, 0, 550,  "Controladoria — acesso restrito"),
    ("auditoria",                 "Auditoria",                  1, 0, 1, 0, 560,  "Auditoria interna e externa — acesso restrito"),
    ("seguranca_do_trabalho",     "Segurança do Trabalho",      1, 0, 0, 0, 570,  "Segurança do trabalho e CIPA"),
    ("confidencial",              "Confidencial",               1, 0, 1, 0, 580,  "Conteúdo confidencial — acesso restrito"),
    ("alta_confidencialidade",    "Alta Confidencialidade",     1, 0, 1, 0, 590,  "Alta confidencialidade — acesso restrito"),
    # Arquivo
    ("arquivo_morto",             "Arquivo Morto",              1, 0, 0, 0, 600,  "Documentos arquivados"),
    ("obsoleto",                  "Obsoleto",                   1, 0, 0, 0, 610,  "Conteúdos obsoletos"),
]


def create_access_groups():
    for (internal_name, display_name, is_internal, is_external,
         is_restricted, system_group, sort_order, description) in ACCESS_GROUPS:
        if not frappe.db.exists("GF Access Group", internal_name):
            frappe.get_doc({
                "doctype": "GF Access Group",
                "internal_name": internal_name,
                "display_name": display_name,
                "is_internal": is_internal,
                "is_external": is_external,
                "is_restricted": is_restricted,
                "system_group": system_group,
                "active": 1,
                "sort_order": sort_order,
                "description": description
            }).insert(ignore_permissions=True)
    print(f"GF Atlas App: {len(ACCESS_GROUPS)} grupos de acesso criados.")


# ─────────────────────────────────────────────────────────────────────────────
# GF CONTENT GROUPS
# (sort_order, display_name, external_reference, is_group, icon)
#
# sort_order  → string hierárquico (ex: "1", "1_0010", "1_0010_010")
# internal_name = external_reference (autoname = field:internal_name)
# parent_group → derivado removendo o último segmento do sort_order
# icon         → nome do ícone Lucide Icons (https://lucide.dev/icons)
# ─────────────────────────────────────────────────────────────────────────────

CONTENT_GROUPS = [
    # ── RAIZ
    ("1",                "HUB",                                  "1_hub",                                          1, "layout-dashboard"),

    # ── NÍVEL 1 — grupos principais
    ("1_0010",           "Financeiro",                           "1_0010_financeiro",                              1, "banknote"),
    ("1_0010_010",       "Contas a Pagar",                       "1_0010_010_contas_a_pagar",                      0, "arrow-down"),
    ("1_0010_020",       "Contas a Receber",                     "1_0010_020_contas_a_receber",                    0, "arrow-up"),
    ("1_0010_030",       "Fluxo de Caixa",                       "1_0010_030_fluxo_de_caixa",                      0, "trending-up"),
    ("1_0010_040",       "Custos de Projetos",                   "1_0010_040_custos_de_projetos",                  0, "calculator"),
    ("1_0010_050",       "Investimentos",                        "1_0010_050_investimentos",                       0, "trending-up"),
    ("1_0010_060",       "Impostos e Obrigações",                "1_0010_060_impostos_e_obrigacoes",               0, "receipt"),
    ("1_0010_070",       "Relatórios Financeiros",               "1_0010_070_relatorios_financeiros",              0, "bar-chart-2"),
    ("1_0010_080",       "Conciliações",                         "1_0010_080_conciliacoes",                        0, "check-circle"),
    ("1_0010_090",       "Fluxos Bancários",                     "1_0010_090_fluxos_bancarios",                    0, "landmark"),
    ("1_0010_100",       "Orçamentos",                           "1_0010_100_orcamentos",                          0, "file-text"),
    ("1_0010_110",       "DRE e Balanços",                       "1_0010_110_dre_e_balancos",                      0, "pie-chart"),
    ("1_0010_120",       "Outros Financeiro",                    "1_0010_120_outros_financeiro",                   0, "folder"),

    ("1_0020",           "Comercial",                            "1_0020_comercial",                               1, "briefcase"),
    ("1_0020_010",       "Clientes",                             "1_0020_010_clientes",                            0, "users"),
    ("1_0020_020",       "Propostas Comerciais",                 "1_0020_020_propostas_comerciais",                0, "file-plus"),
    ("1_0020_030",       "Tabelas de Preço",                     "1_0020_030_tabelas_de_preco",                    0, "tag"),
    ("1_0020_040",       "Apresentações Comerciais",             "1_0020_040_apresentacoes_comerciais",            0, "monitor"),
    ("1_0020_050",       "Followups e Negociações",              "1_0020_050_followups_e_negociacoes",             0, "phone-call"),
    ("1_0020_060",       "Contratos Comerciais",                 "1_0020_060_contratos_comerciais",                0, "file-check"),
    ("1_0020_070",       "CRM",                                  "1_0020_070_crm",                                 0, "share-2"),
    ("1_0020_080",       "Leads e Prospecção",                   "1_0020_080_leads_e_prospeccao",                  0, "search"),
    ("1_0020_090",       "Histórico de Negociações",             "1_0020_090_historico_de_negociacoes",            0, "clock"),
    ("1_0020_100",       "Outros Comercial",                     "1_0020_100_outros_comercial",                    0, "folder"),

    ("1_0030",           "Compras e Suprimentos",                "1_0030_compras_e_suprimentos",                   1, "shopping-cart"),
    ("1_0030_010",       "Solicitações de Compra",               "1_0030_010_solicitacoes_de_compra",              0, "clipboard-list"),
    ("1_0030_020",       "Cotações de Fornecedores",             "1_0030_020_cotacoes_de_fornecedores",            0, "file-text"),
    ("1_0030_030",       "Pedidos de Compra",                    "1_0030_030_pedidos_de_compra",                   0, "package"),
    ("1_0030_040",       "Fornecedores Homologados",             "1_0030_040_fornecedores_homologados",            0, "users"),
    ("1_0030_050",       "Materiais Críticos",                   "1_0030_050_materiais_criticos",                  0, "box"),
    ("1_0030_060",       "Notas e Comprovantes",                 "1_0030_060_notas_e_comprovantes",                0, "receipt"),
    ("1_0030_070",       "Histórico de Compras",                 "1_0030_070_historico_de_compras",                0, "clock"),
    ("1_0030_080",       "Contratos de Fornecimento",            "1_0030_080_contratos_de_fornecimento",           0, "file-check"),
    ("1_0030_090",       "Controle de Entregas",                 "1_0030_090_controle_de_entregas",                0, "truck"),
    ("1_0030_100",       "Outros Compras e Suprimentos",         "1_0030_100_outros_compras_e_suprimentos",        0, "folder"),

    ("1_0040",           "Produção e Fabricação",                "1_0040_producao_e_fabricacao",                   1, "factory"),
    ("1_0040_010",       "Ordens de Produção",                   "1_0040_010_ordens_de_producao",                  0, "clipboard"),
    ("1_0040_020",       "Desenhos para Fabricação",             "1_0040_020_desenhos_para_fabricacao",            0, "file-text"),
    ("1_0040_030",       "Usinagem",                             "1_0040_030_usinagem",                            0, "wrench"),
    ("1_0040_040",       "Soldagem",                             "1_0040_040_soldagem",                            0, "zap"),
    ("1_0040_050",       "Polimento e Acabamento",               "1_0040_050_polimento_e_acabamento",              0, "star"),
    ("1_0040_060",       "Montagem",                             "1_0040_060_montagem",                            0, "layers"),
    ("1_0040_070",       "Inspeção Final",                       "1_0040_070_inspecao_final",                      0, "shield-check"),
    ("1_0040_080",       "Planejamento Industrial",              "1_0040_080_planejamento_industrial",             0, "calendar"),
    ("1_0040_090",       "Tempos e Processos",                   "1_0040_090_tempos_e_processos",                  0, "clock"),
    ("1_0040_100",       "Controle de Produção",                 "1_0040_100_controle_de_producao",                0, "gauge"),
    ("1_0040_110",       "Outros Produção e Fabricação",         "1_0040_110_outros_producao_e_fabricacao",        0, "folder"),

    ("1_0050",           "Estoque e Logística",                  "1_0050_estoque_e_logistica",                     1, "package"),
    ("1_0050_010",       "Estoque",                              "1_0050_010_estoque",                             0, "package"),
    ("1_0050_020",       "Almoxarifado",                         "1_0050_020_almoxarifado",                        0, "inbox"),
    ("1_0050_030",       "Movimentações",                        "1_0050_030_movimentacoes",                       0, "move"),
    ("1_0050_040",       "Ajustes de Estoque",                   "1_0050_040_ajustes_de_estoque",                  0, "sliders"),
    ("1_0050_050",       "Inventários",                          "1_0050_050_inventarios",                         0, "clipboard-list"),
    ("1_0050_060",       "Expedição",                            "1_0050_060_expedicao",                           0, "truck"),
    ("1_0050_070",       "Recebimento",                          "1_0050_070_recebimento",                         0, "download"),
    ("1_0050_080",       "Separação",                            "1_0050_080_separacao",                           0, "filter"),
    ("1_0050_090",       "Logística Interna",                    "1_0050_090_logistica_interna",                   0, "route"),
    ("1_0050_100",       "Transporte",                           "1_0050_100_transporte",                          0, "truck"),
    ("1_0050_110",       "Outros Estoque e Logística",           "1_0050_110_outros_estoque_e_logistica",          0, "folder"),

    ("1_0060",           "Engenharia",                           "1_0060_engenharia",                              1, "wrench"),
    ("1_0060_010",       "Projetos Mecânicos",                   "1_0060_010_projetos_mecanicos",                  0, "wrench"),
    ("1_0060_020",       "Projetos Elétricos",                   "1_0060_020_projetos_eletricos",                  0, "zap"),
    ("1_0060_030",       "Automação e CLP",                      "1_0060_030_automacao_e_clp",                     0, "cpu"),
    ("1_0060_040",       "Layouts Industriais",                  "1_0060_040_layouts_industriais",                 0, "layout"),
    ("1_0060_050",       "Memoriais Descritivos",                "1_0060_050_memoriais_descritivos",               0, "file-text"),
    ("1_0060_060",       "Cálculos Técnicos",                    "1_0060_060_calculos_tecnicos",                   0, "calculator"),
    ("1_0060_070",       "Revisões de Projeto",                  "1_0060_070_revisoes_de_projeto",                 0, "refresh-cw"),
    ("1_0060_080",       "Padrões de Projetos",                  "1_0060_080_padroes_de_projetos",                 0, "bookmark"),
    ("1_0060_090",       "Bibliotecas CAD",                      "1_0060_090_bibliotecas_cad",                     0, "grid"),
    ("1_0060_100",       "Especificações Técnicas",              "1_0060_100_especificacoes_tecnicas",             0, "file-check"),
    ("1_0060_110",       "Normas de Projeto",                    "1_0060_110_normas_de_projeto",                   0, "scroll"),
    ("1_0060_120",       "Outros Engenharia",                    "1_0060_120_outros_engenharia",                   0, "folder"),

    ("1_0070",           "Qualidade",                            "1_0070_qualidade",                               1, "shield-check"),
    ("1_0070_010",       "Procedimentos Operacionais Padrão",    "1_0070_010_procedimentos_operacionais_padrao",   0, "scroll"),
    ("1_0070_020",       "Checklists",                           "1_0070_020_checklists",                          0, "check-square"),
    ("1_0070_030",       "Relatórios de Inspeção",               "1_0070_030_relatorios_de_inspecao",              0, "search"),
    ("1_0070_040",       "Certificados de Materiais",            "1_0070_040_certificados_de_materiais",           0, "award"),
    ("1_0070_050",       "Rastreabilidade",                      "1_0070_050_rastreabilidade",                     0, "route"),
    ("1_0070_060",       "Não Conformidades",                    "1_0070_060_nao_conformidades",                   0, "alert-circle"),
    ("1_0070_070",       "Melhoria Contínua",                    "1_0070_070_melhoria_continua",                   0, "trending-up"),
    ("1_0070_080",       "Auditorias",                           "1_0070_080_auditorias",                          0, "clipboard-check"),
    ("1_0070_090",       "Indicadores da Qualidade",             "1_0070_090_indicadores_da_qualidade",            0, "bar-chart"),
    ("1_0070_100",       "Ações Corretivas e Preventivas",       "1_0070_100_acoes_corretivas_e_preventivas",      0, "settings"),
    ("1_0070_110",       "Outros Qualidade",                     "1_0070_110_outros_qualidade",                    0, "folder"),

    ("1_0080",           "Recursos Humanos",                     "1_0080_recursos_humanos",                        1, "users"),
    ("1_0080_010",       "Colaboradores",                        "1_0080_010_colaboradores",                       0, "user"),
    ("1_0080_020",       "Prestadores de Serviço",               "1_0080_020_prestadores_de_servico",              0, "user-check"),
    ("1_0080_030",       "Treinamentos",                         "1_0080_030_treinamentos",                        0, "graduation-cap"),
    ("1_0080_040",       "Funções e Responsabilidades",          "1_0080_040_funcoes_e_responsabilidades",         0, "briefcase"),
    ("1_0080_050",       "Segurança do Trabalho",                "1_0080_050_seguranca_do_trabalho",               0, "shield"),
    ("1_0080_060",       "Políticas de Conduta",                 "1_0080_060_politicas_de_conduta",                0, "scroll"),
    ("1_0080_070",       "Folha de Pagamento",                   "1_0080_070_folha_de_pagamento",                  0, "banknote"),
    ("1_0080_080",       "Benefícios",                           "1_0080_080_beneficios",                          0, "heart"),
    ("1_0080_090",       "Recrutamento e Seleção",               "1_0080_090_recrutamento_e_selecao",              0, "user-plus"),
    ("1_0080_100",       "Avaliações de Desempenho",             "1_0080_100_avaliacoes_de_desempenho",            0, "star"),
    ("1_0080_110",       "Outros Recursos Humanos",              "1_0080_110_outros_recursos_humanos",             0, "folder"),

    ("1_0090",           "Clientes e Obras",                     "1_0090_clientes_e_obras",                        1, "hard-hat"),
    ("1_0090_010",       "Clientes Ativos",                      "1_0090_010_clientes_ativos",                     0, "users"),
    ("1_0090_020",       "Histórico de Projetos",                "1_0090_020_historico_de_projetos",               0, "clock"),
    ("1_0090_030",       "Instalações em Campo",                 "1_0090_030_instalacoes_em_campo",                0, "map-pin"),
    ("1_0090_040",       "Assistência Técnica",                  "1_0090_040_assistencia_tecnica",                 0, "tool"),
    ("1_0090_050",       "Entregas Técnicas",                    "1_0090_050_entregas_tecnicas",                   0, "package"),
    ("1_0090_060",       "Pós Venda",                            "1_0090_060_pos_venda",                           0, "handshake"),
    ("1_0090_070",       "Garantias",                            "1_0090_070_garantias",                           0, "shield-check"),
    ("1_0090_080",       "Histórico de Atendimento",             "1_0090_080_historico_de_atendimento",            0, "message-square"),
    ("1_0090_090",       "Documentação de Campo",                "1_0090_090_documentacao_de_campo",               0, "file"),
    ("1_0090_100",       "Outros Clientes e Obras",              "1_0090_100_outros_clientes_e_obras",             0, "folder"),

    ("1_0100",           "Produtos e Equipamentos",              "1_0100_produtos_e_equipamentos",                 1, "box"),
    ("1_0100_010",       "Biorreatores",                         "1_0100_010_biorreatores",                        0, "flask-conical"),
    ("1_0100_020",       "Cisalhadores",                         "1_0100_020_cisalhadores",                        0, "cpu"),
    ("1_0100_030",       "Spray Heads e CIP",                    "1_0100_030_spray_heads_e_cip",                   0, "droplets"),
    ("1_0100_040",       "Skids",                                "1_0100_040_skids",                               0, "layers"),
    ("1_0100_050",       "Tanques e Vasos de Pressão",           "1_0100_050_tanques_e_vasos_de_pressao",          0, "database"),
    ("1_0100_060",       "Plantas Piloto",                       "1_0100_060_plantas_piloto",                      0, "microscope"),
    ("1_0100_070",       "Componentes Sanitários",               "1_0100_070_componentes_sanitarios",              0, "box"),
    ("1_0100_080",       "Catálogos Técnicos",                   "1_0100_080_catalogos_tecnicos",                  0, "book"),
    ("1_0100_090",       "Lista de Componentes",                 "1_0100_090_lista_de_componentes",                0, "clipboard-list"),
    ("1_0100_100",       "Estrutura de Produtos",                "1_0100_100_estrutura_de_produtos",               0, "git-branch"),
    ("1_0100_110",       "Outros Produtos e Equipamentos",       "1_0100_110_outros_produtos_e_equipamentos",      0, "folder"),

    ("1_0110",           "Projetos Especiais",                   "1_0110_projetos_especiais",                      1, "sparkles"),
    ("1_0110_010",       "Projeto Yellow",                       "1_0110_010_projeto_yellow",                      0, "star"),
    ("1_0110_020",       "AlphaBlade",                           "1_0110_020_alphablade",                          0, "zap"),
    ("1_0110_030",       "Plantas Piloto",                       "1_0110_030_plantas_piloto",                      0, "microscope"),
    ("1_0110_040",       "Desenvolvimento de Produtos",          "1_0110_040_desenvolvimento_de_produtos",         0, "code"),
    ("1_0110_050",       "Pesquisa e Inovação",                  "1_0110_050_pesquisa_e_inovacao",                 0, "search"),
    ("1_0110_060",       "Projetos Encerrados",                  "1_0110_060_projetos_encerrados",                 0, "archive"),
    ("1_0110_070",       "Pesquisa Industrial",                  "1_0110_070_pesquisa_industrial",                 0, "factory"),
    ("1_0110_080",       "Inovações",                            "1_0110_080_inovacoes",                           0, "sparkles"),
    ("1_0110_090",       "Estudos de Viabilidade",               "1_0110_090_estudos_de_viabilidade",              0, "bar-chart"),
    ("1_0110_100",       "Outros Projetos Especiais",            "1_0110_100_outros_projetos_especiais",           0, "folder"),

    ("1_0120",           "Processos e Operações",                "1_0120_processos_e_operacoes",                   1, "git-branch"),
    ("1_0120_010",       "BPM e Fluxos",                         "1_0120_010_bpm_e_fluxos",                        0, "git-branch"),
    ("1_0120_020",       "Fluxos Operacionais",                  "1_0120_020_fluxos_operacionais",                 0, "arrow-right"),
    ("1_0120_030",       "Mapeamento de Processos",              "1_0120_030_mapeamento_de_processos",             0, "map"),
    ("1_0120_040",       "Indicadores Operacionais",             "1_0120_040_indicadores_operacionais",            0, "bar-chart"),
    ("1_0120_050",       "Procedimentos Internos",               "1_0120_050_procedimentos_internos",              0, "scroll"),
    ("1_0120_060",       "SLA e Tempos",                         "1_0120_060_sla_e_tempos",                        0, "clock"),
    ("1_0120_070",       "Padronização",                         "1_0120_070_padronizacao",                        0, "bookmark"),
    ("1_0120_080",       "Automações Operacionais",              "1_0120_080_automacoes_operacionais",             0, "zap"),
    ("1_0120_090",       "Outros Processos e Operações",         "1_0120_090_outros_processos_e_operacoes",        0, "folder"),

    ("1_0130",           "Governança e Administração",           "1_0130_governanca_e_administracao",              1, "landmark"),
    ("1_0130_010",       "Contratos Sociais e Documentos da Empresa", "1_0130_010_contratos_sociais_e_documentos_da_empresa", 0, "file-text"),
    ("1_0130_020",       "Procurações e Autorizações",           "1_0130_020_procuracoes_e_autorizacoes",          0, "pen-line"),
    ("1_0130_030",       "Políticas Internas",                   "1_0130_030_politicas_internas",                  0, "scroll"),
    ("1_0130_040",       "Atas e Reuniões",                      "1_0130_040_atas_e_reunioes",                     0, "clipboard"),
    ("1_0130_050",       "Planejamento Estratégico",             "1_0130_050_planejamento_estrategico",            0, "target"),
    ("1_0130_060",       "Compliance e Auditoria",               "1_0130_060_compliance_e_auditoria",              0, "shield"),
    ("1_0130_070",       "Estrutura Organizacional",             "1_0130_070_estrutura_organizacional",            0, "building-2"),
    ("1_0130_080",       "Indicadores e Métricas",               "1_0130_080_indicadores_e_metricas",              0, "bar-chart"),
    ("1_0130_090",       "Outros Governança e Administração",    "1_0130_090_outros_governanca_e_administracao",   0, "folder"),

    ("1_0140",           "Jurídico e Compliance",                "1_0140_juridico_e_compliance",                   1, "shield"),
    ("1_0140_010",       "Contratos",                            "1_0140_010_contratos",                           0, "file-check"),
    ("1_0140_020",       "Notificações",                         "1_0140_020_notificacoes",                        0, "bell"),
    ("1_0140_030",       "Propriedade Intelectual",              "1_0140_030_propriedade_intelectual",             0, "bookmark"),
    ("1_0140_040",       "Marcas e Registros",                   "1_0140_040_marcas_e_registros",                  0, "tag"),
    ("1_0140_050",       "Termos de Confidencialidade",          "1_0140_050_termos_de_confidencialidade",         0, "lock"),
    ("1_0140_060",       "Documentos Legais",                    "1_0140_060_documentos_legais",                   0, "file-text"),
    ("1_0140_070",       "LGPD e Privacidade",                   "1_0140_070_lgpd_e_privacidade",                  0, "eye-off"),
    ("1_0140_080",       "Contratos Internacionais",             "1_0140_080_contratos_internacionais",            0, "globe"),
    ("1_0140_090",       "Compliance Regulatório",               "1_0140_090_compliance_regulatorio",              0, "shield-check"),
    ("1_0140_100",       "Outros Jurídico e Compliance",         "1_0140_100_outros_juridico_e_compliance",        0, "folder"),

    ("1_0150",           "Estratégia e Diretoria",               "1_0150_estrategia_e_diretoria",                  1, "target"),
    ("1_0150_010",       "Indicadores Estratégicos",             "1_0150_010_indicadores_estrategicos",            0, "bar-chart-2"),
    ("1_0150_020",       "Planejamento Corporativo",             "1_0150_020_planejamento_corporativo",            0, "map"),
    ("1_0150_030",       "Expansão e Mercado",                   "1_0150_030_expansao_e_mercado",                  0, "trending-up"),
    ("1_0150_040",       "Fusões e Parcerias",                   "1_0150_040_fusoes_e_parcerias",                  0, "git-merge"),
    ("1_0150_050",       "Estudos Confidenciais",                "1_0150_050_estudos_confidenciais",               0, "file-text"),
    ("1_0150_060",       "Outros Estratégia e Diretoria",        "1_0150_060_outros_estrategia_e_diretoria",       0, "folder"),

    ("1_0160",           "Executivo e Estratégia",               "1_0160_executivo_e_estrategia",                  1, "award"),
    ("1_0160_010",       "Planejamento Estratégico",             "1_0160_010_planejamento_estrategico",            0, "target"),
    ("1_0160_020",       "Indicadores Executivos",               "1_0160_020_indicadores_executivos",              0, "bar-chart"),
    ("1_0160_030",       "Conselho",                             "1_0160_030_conselho",                            0, "users"),
    ("1_0160_040",       "Reuniões Estrategicas",                "1_0160_040_reunioes_estrategicas",               0, "calendar"),
    ("1_0160_050",       "Expansão",                             "1_0160_050_expansao",                            0, "trending-up"),
    ("1_0160_060",       "Novos Negócios",                       "1_0160_060_novos_negocios",                      0, "briefcase"),
    ("1_0160_070",       "Inteligência de Mercado",              "1_0160_070_inteligencia_de_mercado",             0, "brain"),
    ("1_0160_080",       "Estudos Confidenciais",                "1_0160_080_estudos_confidenciais",               0, "lock"),
    ("1_0160_090",       "Relatórios Executivos",                "1_0160_090_relatorios_executivos",               0, "file-text"),
    ("1_0160_100",       "Outros Executivo e Estratégia",        "1_0160_100_outros_executivo_e_estrategia",       0, "folder"),

    ("1_0170",           "Holding e Unidades",                   "1_0170_holding_e_unidades",                      1, "building-2"),
    ("1_0170_010",       "Empresas do Grupo",                    "1_0170_010_empresas_do_grupo",                   0, "building"),
    ("1_0170_020",       "Filiais",                              "1_0170_020_filiais",                             0, "building-2"),
    ("1_0170_030",       "Estrutura Societária",                 "1_0170_030_estrutura_societaria",                0, "file-text"),
    ("1_0170_040",       "Governança Corporativa",               "1_0170_040_governanca_corporativa",              0, "landmark"),
    ("1_0170_050",       "Participações",                        "1_0170_050_participacoes",                       0, "pie-chart"),
    ("1_0170_060",       "Organograma Global",                   "1_0170_060_organograma_global",                  0, "git-branch"),
    ("1_0170_070",       "Expansão Corporativa",                 "1_0170_070_expansao_corporativa",                0, "trending-up"),
    ("1_0170_080",       "Joint Ventures",                       "1_0170_080_joint_ventures",                      0, "handshake"),
    ("1_0170_090",       "Fusões e Aquisições",                  "1_0170_090_fusoes_e_aquisicoes",                 0, "git-merge"),
    ("1_0170_100",       "Outros Holding e Unidades",            "1_0170_100_outros_holding_e_unidades",           0, "folder"),

    ("1_0180",           "Inteligência e Dados",                 "1_0180_inteligencia_e_dados",                    1, "bar-chart-2"),
    ("1_0180_010",       "Dashboards",                           "1_0180_010_dashboards",                          0, "layout-dashboard"),
    ("1_0180_020",       "BI e Analytics",                       "1_0180_020_bi_e_analytics",                      0, "pie-chart"),
    ("1_0180_030",       "Indicadores",                          "1_0180_030_indicadores",                         0, "bar-chart"),
    ("1_0180_040",       "Relatórios Estratégicos",              "1_0180_040_relatorios_estrategicos",             0, "file-text"),
    ("1_0180_050",       "Dados Consolidados",                   "1_0180_050_dados_consolidados",                  0, "database"),
    ("1_0180_060",       "Outros Inteligência e Dados",          "1_0180_060_outros_inteligencia_e_dados",         0, "folder"),

    ("1_0190",           "Governança de Dados",                  "1_0190_governanca_de_dados",                     1, "database"),
    ("1_0190_010",       "Estrutura de Dados",                   "1_0190_010_estrutura_de_dados",                  0, "layers"),
    ("1_0190_020",       "Integrações",                          "1_0190_020_integracoes",                         0, "share-2"),
    ("1_0190_030",       "APIs",                                 "1_0190_030_apis",                                0, "code"),
    ("1_0190_040",       "Data Lake",                            "1_0190_040_data_lake",                           0, "database"),
    ("1_0190_050",       "BI e Analytics",                       "1_0190_050_bi_e_analytics",                      0, "pie-chart"),
    ("1_0190_060",       "Indicadores",                          "1_0190_060_indicadores",                         0, "bar-chart"),
    ("1_0190_070",       "Master Data",                          "1_0190_070_master_data",                         0, "star"),
    ("1_0190_080",       "LGPD e Privacidade",                   "1_0190_080_lgpd_e_privacidade",                  0, "eye-off"),
    ("1_0190_090",       "Políticas de Dados",                   "1_0190_090_politicas_de_dados",                  0, "scroll"),
    ("1_0190_100",       "Outros Governança de Dados",           "1_0190_100_outros_governanca_de_dados",          0, "folder"),

    ("1_0200",           "Tecnologia e ERPNext",                 "1_0200_tecnologia_e_erpnext",                    1, "cpu"),
    ("1_0200_010",       "ERPNext",                              "1_0200_010_erpnext",                             0, "monitor"),
    ("1_0200_020",       "Frappe Cloud",                         "1_0200_020_frappe_cloud",                        0, "cloud"),
    ("1_0200_030",       "Aplicativo ICHIS",                     "1_0200_030_aplicativo_ichis",                    0, "box"),
    ("1_0200_040",       "Relatórios Customizados",              "1_0200_040_relatorios_customizados",             0, "bar-chart"),
    ("1_0200_050",       "Scripts e Customizações",              "1_0200_050_scripts_e_customizacoes",             0, "code-2"),
    ("1_0200_060",       "Backups e Segurança",                  "1_0200_060_backups_e_seguranca",                 0, "archive"),
    ("1_0200_070",       "Manuais Internos do Sistema",          "1_0200_070_manuais_internos_do_sistema",         0, "book"),
    ("1_0200_080",       "APIs e Integrações",                   "1_0200_080_apis_e_integracoes",                  0, "share-2"),
    ("1_0200_090",       "Infraestrutura",                       "1_0200_090_infraestrutura",                      0, "server"),
    ("1_0200_100",       "Cloud e Hospedagem",                   "1_0200_100_cloud_e_hospedagem",                  0, "cloud"),
    ("1_0200_110",       "Inteligência Artificial",              "1_0200_110_inteligencia_artificial",             0, "brain"),
    ("1_0200_120",       "GitHub e Repositórios",                "1_0200_120_github_e_repositorios",               0, "git-branch"),
    ("1_0200_130",       "Websites e Aplicações",                "1_0200_130_websites_e_aplicacoes",               0, "globe"),
    ("1_0200_140",       "Outros Tecnologia e ERPNext",          "1_0200_140_outros_tecnologia_e_erpnext",         0, "folder"),

    ("1_0210",           "Websites e Aplicações",                "1_0210_websites_e_aplicacoes",                   1, "globe"),
    ("1_0210_010",       "Websites",                             "1_0210_010_websites",                            0, "globe"),
    ("1_0210_020",       "Landing Pages",                        "1_0210_020_landing_pages",                       0, "monitor"),
    ("1_0210_030",       "Aplicações Web",                       "1_0210_030_aplicacoes_web",                      0, "layout"),
    ("1_0210_040",       "APIs",                                 "1_0210_040_apis",                                0, "code"),
    ("1_0210_050",       "Cloudflare",                           "1_0210_050_cloudflare",                          0, "shield"),
    ("1_0210_060",       "GitHub",                               "1_0210_060_github",                              0, "git-branch"),
    ("1_0210_070",       "Automações",                           "1_0210_070_automacoes",                          0, "zap"),
    ("1_0210_080",       "Outros Websites e Aplicações",         "1_0210_080_outros_websites_e_aplicacoes",        0, "folder"),

    ("1_0220",           "IA e Automações",                      "1_0220_ia_e_automacoes",                         1, "brain"),
    ("1_0220_010",       "Prompts",                              "1_0220_010_prompts",                             0, "message-square"),
    ("1_0220_020",       "Agentes IA",                           "1_0220_020_agentes_ia",                          0, "cpu"),
    ("1_0220_030",       "MCPs",                                 "1_0220_030_mcps",                                0, "settings-2"),
    ("1_0220_040",       "Workflows",                            "1_0220_040_workflows",                           0, "git-branch"),
    ("1_0220_050",       "Automações",                           "1_0220_050_automacoes",                          0, "zap"),
    ("1_0220_060",       "Integrações IA",                       "1_0220_060_integracoes_ia",                      0, "share-2"),
    ("1_0220_070",       "Outros IA e Automações",               "1_0220_070_outros_ia_e_automacoes",              0, "folder"),

    ("1_0230",           "Inovação e Pesquisa",                  "1_0230_inovacao_e_pesquisa",                     1, "flask-conical"),
    ("1_0230_010",       "Pesquisa e Desenvolvimento",           "1_0230_010_pesquisa_e_desenvolvimento",          0, "microscope"),
    ("1_0230_020",       "Patentes",                             "1_0230_020_patentes",                            0, "bookmark"),
    ("1_0230_030",       "Estudos",                              "1_0230_030_estudos",                             0, "file-text"),
    ("1_0230_040",       "Protótipos",                           "1_0230_040_prototipos",                          0, "box"),
    ("1_0230_050",       "Laboratório",                          "1_0230_050_laboratorio",                         0, "flask-conical"),
    ("1_0230_060",       "Roadmap de Produtos",                  "1_0230_060_roadmap_de_produtos",                 0, "route"),
    ("1_0230_070",       "Testes Industriais",                   "1_0230_070_testes_industriais",                  0, "check-circle"),
    ("1_0230_080",       "Validações",                           "1_0230_080_validacoes",                          0, "shield-check"),
    ("1_0230_090",       "Inovações",                            "1_0230_090_inovacoes",                           0, "sparkles"),
    ("1_0230_100",       "Outros Inovação e Pesquisa",           "1_0230_100_outros_inovacao_e_pesquisa",          0, "folder"),

    ("1_0240",           "Marketing e Comunicação",              "1_0240_marketing_e_comunicacao",                 1, "share-2"),
    ("1_0240_010",       "Identidade Visual",                    "1_0240_010_identidade_visual",                   0, "star"),
    ("1_0240_020",       "Logotipos",                            "1_0240_020_logotipos",                           0, "image"),
    ("1_0240_030",       "Fotos de Produtos",                    "1_0240_030_fotos_de_produtos",                   0, "camera"),
    ("1_0240_040",       "Catálogos",                            "1_0240_040_catalogos",                           0, "book"),
    ("1_0240_050",       "Site e Conteúdos Web",                 "1_0240_050_site_e_conteudos_web",                0, "globe"),
    ("1_0240_060",       "Redes Sociais",                        "1_0240_060_redes_sociais",                       0, "share-2"),
    ("1_0240_070",       "Apresentações Institucionais",         "1_0240_070_apresentacoes_institucionais",        0, "monitor"),
    ("1_0240_080",       "Campanhas",                            "1_0240_080_campanhas",                           0, "target"),
    ("1_0240_090",       "Mídia e Publicidade",                  "1_0240_090_midia_e_publicidade",                 0, "tv"),
    ("1_0240_100",       "Conteúdo Institucional",               "1_0240_100_conteudo_institucional",              0, "file-text"),
    ("1_0240_110",       "Branding",                             "1_0240_110_branding",                            0, "award"),
    ("1_0240_120",       "Outros Marketing e Comunicação",       "1_0240_120_outros_marketing_e_comunicacao",      0, "folder"),

    ("1_0250",           "Manuais Técnicos",                     "1_0250_manuais_tecnicos",                        1, "book-open"),
    ("1_0250_010",       "Manuais de Equipamentos",              "1_0250_010_manuais_de_equipamentos",             0, "wrench"),
    ("1_0250_020",       "Manuais de Operação",                  "1_0250_020_manuais_de_operacao",                 0, "play-circle"),
    ("1_0250_030",       "Manuais de Manutenção",                "1_0250_030_manuais_de_manutencao",               0, "tool"),
    ("1_0250_040",       "Manuais de CIP e SIP",                 "1_0250_040_manuais_de_cip_e_sip",                0, "droplets"),
    ("1_0250_050",       "Manuais de Automação",                 "1_0250_050_manuais_de_automacao",                0, "cpu"),
    ("1_0250_060",       "Documentação para Clientes",           "1_0250_060_documentacao_para_clientes",          0, "users"),
    ("1_0250_070",       "Procedimentos",                        "1_0250_070_procedimentos",                       0, "scroll"),
    ("1_0250_080",       "Troubleshooting",                      "1_0250_080_troubleshooting",                     0, "alert-circle"),
    ("1_0250_090",       "Guias Rápidos",                        "1_0250_090_guias_rapidos",                       0, "book"),
    ("1_0250_100",       "Outros Manuais Técnicos",              "1_0250_100_outros_manuais_tecnicos",             0, "folder"),

    ("1_0260",           "Biblioteca Técnica",                   "1_0260_biblioteca_tecnica",                      1, "library"),
    ("1_0260_010",       "Normas Técnicas",                      "1_0260_010_normas_tecnicas",                     0, "scroll"),
    ("1_0260_020",       "Artigos e Estudos",                    "1_0260_020_artigos_e_estudos",                   0, "file-text"),
    ("1_0260_030",       "Catálogos de Fornecedores",            "1_0260_030_catalogos_de_fornecedores",           0, "book"),
    ("1_0260_040",       "Materiais de Referência",              "1_0260_040_materiais_de_referencia",             0, "layers"),
    ("1_0260_050",       "Tabelas Técnicas",                     "1_0260_050_tabelas_tecnicas",                    0, "table"),
    ("1_0260_060",       "Conteúdos de Treinamento",             "1_0260_060_conteudos_de_treinamento",            0, "graduation-cap"),
    ("1_0260_070",       "Livros e Apostilas",                   "1_0260_070_livros_e_apostilas",                  0, "book-open"),
    ("1_0260_080",       "Pesquisas e Referências",              "1_0260_080_pesquisas_e_referencias",             0, "search"),
    ("1_0260_090",       "Materiais Científicos",                "1_0260_090_materiais_cientificos",               0, "microscope"),
    ("1_0260_100",       "Outros Biblioteca Técnica",            "1_0260_100_outros_biblioteca_tecnica",           0, "folder"),

    # ── Informações Pessoa Física
    ("1_0270",                    "Informações Pessoa Física",                      "1_0270_informacoes_pessoa_fisica",                            1, "user"),

    ("1_0270_010",                "Documentos Pessoais",                            "1_0270_010_documentos_pessoais",                              1, "file-text"),
    ("1_0270_010_010",            "RG CPF CNH",                                     "1_0270_010_010_rg_cpf_cnh",                                   0, "user"),
    ("1_0270_010_020",            "Certidões",                                      "1_0270_010_020_certidoes",                                    0, "award"),
    ("1_0270_010_030",            "Passaporte e Vistos",                            "1_0270_010_030_passaporte_e_vistos",                          0, "globe"),
    ("1_0270_010_040",            "Comprovantes de Endereço",                       "1_0270_010_040_comprovantes_de_endereco",                     0, "file"),
    ("1_0270_010_050",            "Títulos e Registros",                            "1_0270_010_050_titulos_e_registros",                          0, "bookmark"),
    ("1_0270_010_060",            "Documentos Digitalizados",                       "1_0270_010_060_documentos_digitalizados",                     0, "copy"),
    ("1_0270_010_070",            "Outros Documentos Pessoais",                     "1_0270_010_070_outros_documentos_pessoais",                   0, "folder"),

    ("1_0270_020",                "Família",                                        "1_0270_020_familia",                                          1, "heart"),
    ("1_0270_020_010",            "Documentos da Esposa",                           "1_0270_020_010_documentos_da_esposa",                         0, "user"),
    ("1_0270_020_020",            "Documentos dos Filhos",                          "1_0270_020_020_documentos_dos_filhos",                        0, "users"),
    ("1_0270_020_030",            "Certidões da Família",                           "1_0270_020_030_certidoes_da_familia",                         0, "award"),
    ("1_0270_020_040",            "Escola e Educação",                              "1_0270_020_040_escola_e_educacao",                            0, "graduation-cap"),
    ("1_0270_020_050",            "Viagens em Família",                             "1_0270_020_050_viagens_em_familia",                           0, "plane"),
    ("1_0270_020_060",            "Registros Importantes",                          "1_0270_020_060_registros_importantes",                        0, "bookmark"),
    ("1_0270_020_070",            "Outros Família",                                 "1_0270_020_070_outros_familia",                               0, "folder"),

    ("1_0270_030",                "Imóveis e Patrimônio",                           "1_0270_030_imoveis_e_patrimonio",                             1, "home"),
    ("1_0270_030_010",            "Escrituras",                                     "1_0270_030_010_escrituras",                                   0, "file-text"),
    ("1_0270_030_020",            "Contratos de Compra e Venda",                    "1_0270_030_020_contratos_de_compra_e_venda",                  0, "file-check"),
    ("1_0270_030_030",            "IPTU",                                           "1_0270_030_030_iptu",                                         0, "receipt"),
    ("1_0270_030_040",            "Condomínio",                                     "1_0270_030_040_condominio",                                   0, "building"),
    ("1_0270_030_050",            "Reformas e Manutenções",                         "1_0270_030_050_reformas_e_manutencoes",                       0, "tool"),
    ("1_0270_030_060",            "Fotos dos Imóveis",                              "1_0270_030_060_fotos_dos_imoveis",                            0, "camera"),
    ("1_0270_030_070",            "Documentos de Regularização",                    "1_0270_030_070_documentos_de_regularizacao",                  0, "shield"),
    ("1_0270_030_080",            "Aluguéis",                                       "1_0270_030_080_alugueis",                                     0, "banknote"),
    ("1_0270_030_090",            "Regularização",                                  "1_0270_030_090_regularizacao",                                0, "shield"),
    ("1_0270_030_100",            "Outros Imóveis e Patrimônio",                    "1_0270_030_100_outros_imoveis_e_patrimonio",                  0, "folder"),

    ("1_0270_040",                "Veículos",                                       "1_0270_040_veiculos",                                         1, "car"),
    ("1_0270_040_010",            "Documentos dos Veículos",                        "1_0270_040_010_documentos_dos_veiculos",                      0, "file-text"),
    ("1_0270_040_020",            "Seguro",                                         "1_0270_040_020_seguro",                                       0, "shield"),
    ("1_0270_040_030",            "IPVA",                                           "1_0270_040_030_ipva",                                         0, "receipt"),
    ("1_0270_040_040",            "Multas e Taxas",                                 "1_0270_040_040_multas_e_taxas",                               0, "alert-circle"),
    ("1_0270_040_050",            "Manutenções",                                    "1_0270_040_050_manutencoes",                                  0, "tool"),
    ("1_0270_040_060",            "Fotos dos Veículos",                             "1_0270_040_060_fotos_dos_veiculos",                           0, "camera"),
    ("1_0270_040_070",            "Compra e Venda",                                 "1_0270_040_070_compra_e_venda",                               0, "trending-up"),
    ("1_0270_040_080",            "Licenciamentos",                                 "1_0270_040_080_licenciamentos",                               0, "key"),
    ("1_0270_040_090",            "Histórico de Manutenção",                        "1_0270_040_090_historico_de_manutencao",                      0, "clock"),
    ("1_0270_040_100",            "Outros Veículos",                                "1_0270_040_100_outros_veiculos",                              0, "folder"),

    ("1_0270_050",                "Saúde e Medicina",                               "1_0270_050_saude_e_medicina",                                 1, "heart-pulse"),
    ("1_0270_050_010",            "Exames Médicos",                                 "1_0270_050_010_exames_medicos",                               0, "clipboard-list"),
    ("1_0270_050_020",            "Consultas Médicas",                              "1_0270_050_020_consultas_medicas",                            0, "stethoscope"),
    ("1_0270_050_030",            "Receitas e Prescrições",                         "1_0270_050_030_receitas_e_prescricoes",                       0, "pill"),
    ("1_0270_050_040",            "Histórico de Saúde",                             "1_0270_050_040_historico_de_saude",                           0, "clock"),
    ("1_0270_050_050",            "Planos de Saúde",                                "1_0270_050_050_planos_de_saude",                              0, "shield"),
    ("1_0270_050_060",            "Odontologia",                                    "1_0270_050_060_odontologia",                                  0, "smile"),
    ("1_0270_050_070",            "Vacinas",                                        "1_0270_050_070_vacinas",                                      0, "syringe"),
    ("1_0270_050_080",            "Cirurgias e Procedimentos",                      "1_0270_050_080_cirurgias_e_procedimentos",                    0, "activity"),
    ("1_0270_050_090",            "Emergências",                                    "1_0270_050_090_emergencias",                                  0, "alert-circle"),
    ("1_0270_050_100",            "Exames Laboratoriais",                           "1_0270_050_100_exames_laboratoriais",                         0, "microscope"),
    ("1_0270_050_110",            "Histórico Familiar",                             "1_0270_050_110_historico_familiar",                           0, "users"),
    ("1_0270_050_120",            "Outros Saúde e Medicina",                        "1_0270_050_120_outros_saude_e_medicina",                      0, "folder"),

    ("1_0270_060",                "Financeiro Pessoal",                             "1_0270_060_financeiro_pessoal",                               1, "banknote"),
    ("1_0270_060_010",            "Bancos",                                         "1_0270_060_010_bancos",                                       0, "landmark"),
    ("1_0270_060_020",            "Cartões",                                        "1_0270_060_020_cartoes",                                      0, "credit-card"),
    ("1_0270_060_030",            "Investimentos",                                  "1_0270_060_030_investimentos",                                0, "trending-up"),
    ("1_0270_060_040",            "Empréstimos e Financiamentos",                   "1_0270_060_040_emprestimos_e_financiamentos",                 0, "dollar-sign"),
    ("1_0270_060_050",            "Imposto de Renda",                               "1_0270_060_050_imposto_de_renda",                             0, "receipt"),
    ("1_0270_060_060",            "Comprovantes de Pagamento",                      "1_0270_060_060_comprovantes_de_pagamento",                    0, "file-check"),
    ("1_0270_060_070",            "Recibos",                                        "1_0270_060_070_recibos",                                      0, "file-text"),
    ("1_0270_060_080",            "Planejamento Financeiro",                        "1_0270_060_080_planejamento_financeiro",                      0, "target"),
    ("1_0270_060_090",            "Planejamento Patrimonial",                       "1_0270_060_090_planejamento_patrimonial",                     0, "building-2"),
    ("1_0270_060_100",            "Reserva Financeira",                             "1_0270_060_100_reserva_financeira",                           0, "archive"),
    ("1_0270_060_110",            "Outros Financeiro Pessoal",                      "1_0270_060_110_outros_financeiro_pessoal",                    0, "folder"),

    ("1_0270_070",                "Seguros",                                        "1_0270_070_seguros",                                          1, "shield"),
    ("1_0270_070_010",            "Seguro de Vida",                                 "1_0270_070_010_seguro_de_vida",                               0, "heart"),
    ("1_0270_070_020",            "Seguro Residencial",                             "1_0270_070_020_seguro_residencial",                           0, "home"),
    ("1_0270_070_030",            "Seguro de Veículos",                             "1_0270_070_030_seguro_de_veiculos",                           0, "car"),
    ("1_0270_070_040",            "Seguro Saúde",                                   "1_0270_070_040_seguro_saude",                                 0, "heart-pulse"),
    ("1_0270_070_050",            "Seguro Empresarial Pessoal",                     "1_0270_070_050_seguro_empresarial_pessoal",                   0, "building"),
    ("1_0270_070_060",            "Apólices",                                       "1_0270_070_060_apolices",                                     0, "file-text"),
    ("1_0270_070_070",            "Sinistros",                                      "1_0270_070_070_sinistros",                                    0, "alert-circle"),
    ("1_0270_070_080",            "Renovações",                                     "1_0270_070_080_renovacoes",                                   0, "refresh-cw"),
    ("1_0270_070_090",            "Outros Seguros",                                 "1_0270_070_090_outros_seguros",                               0, "folder"),

    ("1_0270_080",                "Jurídico Pessoal",                               "1_0270_080_juridico_pessoal",                                 1, "shield"),
    ("1_0270_080_010",            "Contratos Pessoais",                             "1_0270_080_010_contratos_pessoais",                           0, "file-check"),
    ("1_0270_080_020",            "Procurações",                                    "1_0270_080_020_procuracoes",                                  0, "pen-line"),
    ("1_0270_080_030",            "Declarações",                                    "1_0270_080_030_declaracoes",                                  0, "file-text"),
    ("1_0270_080_040",            "Inventário e Testamento",                        "1_0270_080_040_inventario_e_testamento",                      0, "archive"),
    ("1_0270_080_050",            "Processos",                                      "1_0270_080_050_processos",                                    0, "landmark"),
    ("1_0270_080_060",            "Notificações",                                   "1_0270_080_060_notificacoes",                                 0, "bell"),
    ("1_0270_080_070",            "Acordos",                                        "1_0270_080_070_acordos",                                      0, "handshake"),
    ("1_0270_080_080",            "Consultorias",                                   "1_0270_080_080_consultorias",                                 0, "briefcase"),
    ("1_0270_080_090",            "Outros Jurídico Pessoal",                        "1_0270_080_090_outros_juridico_pessoal",                      0, "folder"),

    ("1_0270_090",                "Fotos e Memórias",                               "1_0270_090_fotos_e_memorias",                                 1, "camera"),
    ("1_0270_090_010",            "Fotos Pessoais",                                 "1_0270_090_010_fotos_pessoais",                               0, "user"),
    ("1_0270_090_020",            "Fotos da Família",                               "1_0270_090_020_fotos_da_familia",                             0, "heart"),
    ("1_0270_090_030",            "Fotos de Viagens",                               "1_0270_090_030_fotos_de_viagens",                             0, "plane"),
    ("1_0270_090_040",            "Eventos e Comemorações",                         "1_0270_090_040_eventos_e_comemoracoes",                       0, "calendar"),
    ("1_0270_090_050",            "Vídeos Pessoais",                                "1_0270_090_050_videos_pessoais",                              0, "video"),
    ("1_0270_090_060",            "Documentos Históricos",                          "1_0270_090_060_documentos_historicos",                        0, "clock"),
    ("1_0270_090_070",            "Memórias da Vida",                               "1_0270_090_070_memorias_da_vida",                             0, "heart"),
    ("1_0270_090_080",            "Restaurações",                                   "1_0270_090_080_restauracoes",                                 0, "refresh-cw"),
    ("1_0270_090_090",            "Arquivos Familiares",                            "1_0270_090_090_arquivos_familiares",                          0, "folder"),
    ("1_0270_090_100",            "Outros Fotos e Memórias",                        "1_0270_090_100_outros_fotos_e_memorias",                      0, "folder"),

    ("1_0270_100",                "Viagens e Lazer",                                "1_0270_100_viagens_e_lazer",                                  1, "plane"),
    ("1_0270_100_010",            "Reservas",                                       "1_0270_100_010_reservas",                                     0, "calendar"),
    ("1_0270_100_020",            "Passagens",                                      "1_0270_100_020_passagens",                                    0, "plane"),
    ("1_0270_100_030",            "Hospedagens",                                    "1_0270_100_030_hospedagens",                                  0, "hotel"),
    ("1_0270_100_040",            "Roteiros",                                       "1_0270_100_040_roteiros",                                     0, "map"),
    ("1_0270_100_050",            "Documentos de Viagem",                           "1_0270_100_050_documentos_de_viagem",                         0, "file-text"),
    ("1_0270_100_060",            "Fotos de Viagens",                               "1_0270_100_060_fotos_de_viagens",                             0, "camera"),
    ("1_0270_100_070",            "Comprovantes",                                   "1_0270_100_070_comprovantes",                                 0, "receipt"),
    ("1_0270_100_080",            "Mapas e Roteiros",                               "1_0270_100_080_mapas_e_roteiros",                             0, "map-pin"),
    ("1_0270_100_090",            "Outros Viagens e Lazer",                         "1_0270_100_090_outros_viagens_e_lazer",                       0, "folder"),

    ("1_0270_110",                "Educação e Formação",                            "1_0270_110_educacao_e_formacao",                              1, "graduation-cap"),
    ("1_0270_110_010",            "Cursos",                                         "1_0270_110_010_cursos",                                       0, "book"),
    ("1_0270_110_020",            "Certificados",                                   "1_0270_110_020_certificados",                                 0, "award"),
    ("1_0270_110_030",            "Diplomas",                                       "1_0270_110_030_diplomas",                                     0, "star"),
    ("1_0270_110_040",            "Treinamentos",                                   "1_0270_110_040_treinamentos",                                 0, "users"),
    ("1_0270_110_050",            "Palestras",                                      "1_0270_110_050_palestras",                                    0, "mic"),
    ("1_0270_110_060",            "Materiais de Estudo",                            "1_0270_110_060_materiais_de_estudo",                          0, "book-open"),
    ("1_0270_110_070",            "Especializações",                                "1_0270_110_070_especializacoes",                              0, "target"),
    ("1_0270_110_080",            "Idiomas",                                        "1_0270_110_080_idiomas",                                      0, "globe"),
    ("1_0270_110_090",            "Outros Educação e Formação",                     "1_0270_110_090_outros_educacao_e_formacao",                   0, "folder"),

    ("1_0270_120",                "Senhas e Acessos",                               "1_0270_120_senhas_e_acessos",                                 1, "lock"),
    ("1_0270_120_010",            "Contas Importantes",                             "1_0270_120_010_contas_importantes",                           0, "user"),
    ("1_0270_120_020",            "Acessos Bancários",                              "1_0270_120_020_acessos_bancarios",                            0, "landmark"),
    ("1_0270_120_030",            "Acessos Governamentais",                         "1_0270_120_030_acessos_governamentais",                       0, "building"),
    ("1_0270_120_040",            "Acessos de Sistemas",                            "1_0270_120_040_acessos_de_sistemas",                          0, "monitor"),
    ("1_0270_120_050",            "Recuperação de Contas",                          "1_0270_120_050_recuperacao_de_contas",                        0, "key"),
    ("1_0270_120_060",            "Observações de Segurança",                       "1_0270_120_060_observacoes_de_seguranca",                     0, "shield"),
    ("1_0270_120_070",            "Tokens e 2FA",                                   "1_0270_120_070_tokens_e_2fa",                                 0, "cpu"),
    ("1_0270_120_080",            "Chaves de Recuperação",                          "1_0270_120_080_chaves_de_recuperacao",                        0, "key"),
    ("1_0270_120_090",            "Outros Senhas e Acessos",                        "1_0270_120_090_outros_senhas_e_acessos",                      0, "folder"),

    ("1_0270_130",                "Projetos Pessoais",                              "1_0270_130_projetos_pessoais",                                1, "star"),
    ("1_0270_130_010",            "Ideias",                                         "1_0270_130_010_ideias",                                       0, "sparkles"),
    ("1_0270_130_020",            "Planejamento",                                   "1_0270_130_020_planejamento",                                 0, "target"),
    ("1_0270_130_030",            "Documentos",                                     "1_0270_130_030_documentos",                                   0, "file-text"),
    ("1_0270_130_040",            "Fotos",                                          "1_0270_130_040_fotos",                                        0, "camera"),
    ("1_0270_130_050",            "Referências",                                    "1_0270_130_050_referencias",                                  0, "bookmark"),
    ("1_0270_130_060",            "Histórico",                                      "1_0270_130_060_historico",                                    0, "clock"),
    ("1_0270_130_070",            "Estudos",                                        "1_0270_130_070_estudos",                                      0, "book"),
    ("1_0270_130_080",            "Desenvolvimento",                                "1_0270_130_080_desenvolvimento",                              0, "code-2"),
    ("1_0270_130_090",            "Outros Projetos Pessoais",                       "1_0270_130_090_outros_projetos_pessoais",                     0, "folder"),

    ("1_0270_140",                "Espiritualidade e Vida Pessoal",                 "1_0270_140_espiritualidade_e_vida_pessoal",                   1, "heart"),
    ("1_0270_140_010",            "Reflexões",                                      "1_0270_140_010_reflexoes",                                    0, "message-square"),
    ("1_0270_140_020",            "Mensagens",                                      "1_0270_140_020_mensagens",                                    0, "mail"),
    ("1_0270_140_030",            "Orações",                                        "1_0270_140_030_oracoes",                                      0, "star"),
    ("1_0270_140_040",            "Registros Especiais",                            "1_0270_140_040_registros_especiais",                          0, "bookmark"),
    ("1_0270_140_050",            "Textos Pessoais",                                "1_0270_140_050_textos_pessoais",                              0, "file-text"),
    ("1_0270_140_060",            "Aprendizados",                                   "1_0270_140_060_aprendizados",                                 0, "book-open"),
    ("1_0270_140_070",            "Reflexões de Vida",                              "1_0270_140_070_reflexoes_de_vida",                            0, "moon"),
    ("1_0270_140_080",            "Outros Espiritualidade e Vida Pessoal",          "1_0270_140_080_outros_espiritualidade_e_vida_pessoal",        0, "folder"),

    ("1_0270_150",                "Arquivo Pessoal",                                "1_0270_150_arquivo_pessoal",                                  1, "archive"),
    ("1_0270_150_010",            "Documentos Antigos",                             "1_0270_150_010_documentos_antigos",                           0, "file-text"),
    ("1_0270_150_020",            "Fotos Antigas",                                  "1_0270_150_020_fotos_antigas",                                0, "camera"),
    ("1_0270_150_030",            "Registros Antigos",                              "1_0270_150_030_registros_antigos",                            0, "clock"),
    ("1_0270_150_040",            "Arquivos Obsoletos",                             "1_0270_150_040_arquivos_obsoletos",                           0, "trash-2"),
    ("1_0270_150_050",            "Histórico Geral",                                "1_0270_150_050_historico_geral",                              0, "folder"),
    ("1_0270_150_060",            "Backups Antigos",                                "1_0270_150_060_backups_antigos",                              0, "archive"),
    ("1_0270_150_070",            "Outros Arquivo Pessoal",                         "1_0270_150_070_outros_arquivo_pessoal",                       0, "folder"),

    # ── Backups e Históricos
    ("1_0280",           "Backups e Históricos",                 "1_0280_backups_e_historicos",                    1, "archive"),
    ("1_0280_010",       "Backups ERPNext",                      "1_0280_010_backups_erpnext",                     0, "database"),
    ("1_0280_020",       "Exportações",                          "1_0280_020_exportacoes",                         0, "download"),
    ("1_0280_030",       "Snapshots",                            "1_0280_030_snapshots",                           0, "copy"),
    ("1_0280_040",       "Históricos de Sistema",                "1_0280_040_historicos_de_sistema",               0, "clock"),
    ("1_0280_050",       "Arquivos de Recuperação",              "1_0280_050_arquivos_de_recuperacao",             0, "refresh-cw"),
    ("1_0280_060",       "Logs Antigos",                         "1_0280_060_logs_antigos",                        0, "file-text"),
    ("1_0280_070",       "Outros Backups e Históricos",          "1_0280_070_outros_backups_e_historicos",         0, "folder"),

    # ── Arquivo Morto
    ("1_0290",           "Arquivo Morto",                        "1_0290_arquivo_morto",                           1, "trash-2"),
    ("1_0290_010",       "Documentos Antigos",                   "1_0290_010_documentos_antigos",                  0, "file-text"),
    ("1_0290_020",       "Projetos Encerrados",                  "1_0290_020_projetos_encerrados",                 0, "archive"),
    ("1_0290_030",       "Versões Obsoletas",                    "1_0290_030_versoes_obsoletas",                   0, "trash-2"),
    ("1_0290_040",       "Propostas Perdidas",                   "1_0290_040_propostas_perdidas",                  0, "x-circle"),
    ("1_0290_050",       "Histórico Geral",                      "1_0290_050_historico_geral",                     0, "clock"),
    ("1_0290_060",       "Outros Arquivo Morto",                 "1_0290_060_outros_arquivo_morto",                0, "folder"),
]


def create_content_groups():
    sort_to_name = {g[0]: g[2] for g in CONTENT_GROUPS}

    def get_parent(sort_order):
        if '_' not in sort_order:
            return None
        parent_sort = sort_order.rsplit('_', 1)[0]
        return sort_to_name.get(parent_sort)

    for (sort_order, display_name, external_reference, is_group, icon) in CONTENT_GROUPS:
        if not frappe.db.exists("GF Content Group", external_reference):
            frappe.get_doc({
                "doctype": "GF Content Group",
                "internal_name": external_reference,
                "display_name": display_name,
                "external_reference": external_reference,
                "sort_order": sort_order,
                "is_group": is_group,
                "icon": icon,
                "parent_group": get_parent(sort_order),
                "active": 1
            }).insert(ignore_permissions=True)
    print(f"GF Atlas App: {len(CONTENT_GROUPS)} grupos de conteúdo criados.")


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


# ─────────────────────────────────────────────────────────────────────────────
# SAMPLE SKILLS
# ─────────────────────────────────────────────────────────────────────────────
def create_sample_skills():
    admin = "Administrator"

    skills = [
        # ── 1. Documentação de Contratos ─────────────────────────────────────
        {
            "doctype": "GF Skill",
            "internal_name": "gf_skill_juridico_contratos",
            "skill_name": "Documentação de Contratos",
            "short_description": "Estrutura e redige cláusulas contratuais com linguagem jurídica precisa, cobertura de riscos e conformidade com a legislação brasileira.",
            "category": "Jurídico",
            "status": "Ativo",
            "active": 1,
            "version": "1.0.0",
            "version_notes": "Versão inicial — cobre contratos comerciais, de serviço e de fornecimento.",
            "skill_owner": admin,
            "tags": "contrato, jurídico, cláusulas, legislação, conformidade",
            "output_type": "Documentação",
            "default_language": "Português (BR)",
            "skill_priority": "Alta",
            "allow_export": 1,
            "allow_api_usage": 0,
            "is_system_skill": 0,
            "purpose": (
                "Estruturar, redigir e revisar documentos contratuais com linguagem jurídica precisa "
                "e em conformidade com o Código Civil Brasileiro, CLT e legislação setorial aplicável. "
                "O Skill garante que cada contrato contenha todas as cláusulas obrigatórias, cubra os "
                "principais cenários de risco e use terminologia consistente com a jurisprudência nacional."
            ),
            "when_to_use": (
                "- Elaboração de novos contratos comerciais, de prestação de serviço ou de fornecimento\n"
                "- Revisão e atualização de minutas contratuais existentes\n"
                "- Adaptação de templates padrão para situações específicas\n"
                "- Geração de adendos e termos aditivos"
            ),
            "when_not_to_use": (
                "- Contratos que exijam assinatura de advogado habilitado (petições, contratos judiciais)\n"
                "- Documentos sujeitos a registro em cartório sem revisão humana prévia\n"
                "- Situações envolvendo direito internacional ou legislação estrangeira"
            ),
            "main_instructions": (
                "1. Identificar as partes: razão social, CNPJ/CPF, endereço completo e representantes legais.\n"
                "2. Definir o objeto do contrato com precisão — evitar termos vagos como 'serviços gerais'.\n"
                "3. Estabelecer prazo, forma de pagamento, reajuste (IPCA/INPC) e condições de rescisão.\n"
                "4. Incluir cláusulas de: confidencialidade, propriedade intelectual, limitação de responsabilidade e foro.\n"
                "5. Verificar conformidade com a legislação aplicável ao setor (ex.: LGPD para dados pessoais).\n"
                "6. Usar numeração sequencial de cláusulas e parágrafos (ex.: Cláusula 1ª, §1º, §2º).\n"
                "7. Finalizar com espaço para assinatura, data, local e testemunhas."
            ),
            "mandatory_rules": (
                "- Toda menção a valor monetário deve incluir o valor por extenso entre parênteses.\n"
                "- Foro de eleição obrigatório ao final do documento.\n"
                "- Nunca omitir cláusula de rescisão — deve cobrir rescisão unilateral e por inadimplemento.\n"
                "- Referências legais devem citar artigo e lei específicos (ex.: Art. 421, Código Civil/2002)."
            ),
            "forbidden_actions": (
                "- Não usar linguagem coloquial ou abreviações informais.\n"
                "- Não omitir CNPJ/CPF das partes.\n"
                "- Não incluir cláusulas que violem direitos trabalhistas ou do consumidor.\n"
                "- Não referenciar leis revogadas."
            ),
            "validation_checklist": (
                "[ ] Todas as partes identificadas com razão social, CNPJ e representante legal\n"
                "[ ] Objeto do contrato definido com precisão\n"
                "[ ] Valor por extenso em todas as menções financeiras\n"
                "[ ] Prazo, reajuste e condições de pagamento presentes\n"
                "[ ] Cláusula de rescisão (unilateral e por inadimplemento)\n"
                "[ ] Cláusula de confidencialidade\n"
                "[ ] Foro de eleição definido\n"
                "[ ] Referências legais corretas e vigentes"
            ),
            "writing_style": "Jurídico-formal, preciso, impessoal. Frases completas sem ambiguidade. Voz ativa preferida.",
            "visual_style": "Documento estruturado com numeração de cláusulas e parágrafos. Sem tabelas decorativas.",
            "tone_of_voice": "Formal, neutro, institucional. Nenhuma expressão coloquial.",
            "formatting_rules": (
                "- Título centralizado em maiúsculas\n"
                "- Cláusulas numeradas: Cláusula 1ª, Cláusula 2ª…\n"
                "- Parágrafos: §1º, §2º…\n"
                "- Incisos: I —, II —, III —\n"
                "- Assinaturas ao final com linha, nome, cargo e data"
            ),
            "version_history": "v1.0.0 → criação inicial em 2026-05-18",
        },

        # ── 2. Documentação Técnica de Peças ─────────────────────────────────
        {
            "doctype": "GF Skill",
            "internal_name": "gf_skill_eng_pecas_tecnicas",
            "skill_name": "Documentação Técnica de Peças",
            "short_description": "Gera fichas técnicas completas de peças industriais com especificações, materiais, tolerâncias e instruções de manutenção.",
            "category": "Engenharia",
            "status": "Ativo",
            "active": 1,
            "version": "1.0.0",
            "version_notes": "Versão inicial — cobre peças mecânicas, eletromecânicas e de reposição.",
            "skill_owner": admin,
            "tags": "peças, engenharia, ficha técnica, industrial, manutenção, tolerâncias",
            "output_type": "Documentação",
            "default_language": "Português (BR)",
            "skill_priority": "Normal",
            "allow_export": 1,
            "allow_api_usage": 0,
            "is_system_skill": 0,
            "purpose": (
                "Produzir fichas técnicas padronizadas para peças industriais, contendo todas as informações "
                "necessárias para fabricação, inspeção, manutenção e reposição. O Skill garante rastreabilidade, "
                "consistência de formato e conformidade com normas técnicas (ABNT, ISO) aplicáveis."
            ),
            "when_to_use": (
                "- Criação de ficha técnica para peça nova no catálogo\n"
                "- Atualização de especificações após revisão de engenharia\n"
                "- Geração de documentação para peças de reposição críticas\n"
                "- Padronização de fichas existentes em formatos diversos"
            ),
            "when_not_to_use": (
                "- Projetos que exijam cálculos estruturais ou simulação FEA\n"
                "- Documentação de software embarcado ou firmware\n"
                "- Desenhos técnicos CAD (use ferramentas específicas)"
            ),
            "main_instructions": (
                "1. Registrar código da peça, descrição, família e equipamento de aplicação.\n"
                "2. Listar materiais com norma técnica (ex.: AISI 1045, NBR 6656).\n"
                "3. Especificar dimensões nominais com tolerâncias (ex.: Ø 50 ±0,02 mm).\n"
                "4. Indicar tratamento superficial, dureza e acabamento quando aplicável.\n"
                "5. Definir vida útil esperada, intervalo de manutenção e critério de descarte.\n"
                "6. Incluir fornecedores homologados e código de pedido.\n"
                "7. Registrar histórico de revisões com data, responsável e motivo."
            ),
            "mandatory_rules": (
                "- Todas as dimensões devem estar em milímetros (mm) salvo indicação explícita.\n"
                "- Materiais devem referenciar norma técnica aplicável.\n"
                "- Revisão deve ser registrada no cabeçalho (Rev. 00, Rev. 01…).\n"
                "- Código da peça deve seguir o padrão corporativo definido."
            ),
            "forbidden_actions": (
                "- Não usar denominações genéricas como 'parafuso comum' sem especificação.\n"
                "- Não omitir tolerâncias em dimensões funcionais críticas.\n"
                "- Não referenciar fornecedores não homologados como única opção."
            ),
            "validation_checklist": (
                "[ ] Código e descrição da peça preenchidos\n"
                "[ ] Material com norma técnica\n"
                "[ ] Dimensões com tolerâncias\n"
                "[ ] Tratamento superficial informado (ou 'N/A' justificado)\n"
                "[ ] Vida útil e intervalo de manutenção\n"
                "[ ] Fornecedor homologado\n"
                "[ ] Revisão registrada no cabeçalho"
            ),
            "writing_style": "Técnico, objetivo, sem ambiguidade. Substantivos precisos. Evitar adjetivos subjetivos.",
            "visual_style": "Tabela estruturada com seções claramente delimitadas. Cabeçalho com código, revisão e data.",
            "tone_of_voice": "Técnico, neutro, informativo.",
            "formatting_rules": (
                "- Cabeçalho: Código | Descrição | Revisão | Data | Responsável\n"
                "- Seções: Identificação, Material, Dimensões, Acabamento, Manutenção, Fornecedores, Histórico\n"
                "- Unidades sempre explícitas (mm, kg, HRC, °C)\n"
                "- Tolerâncias no formato ±X,XX"
            ),
            "version_history": "v1.0.0 → criação inicial em 2026-05-18",
        },

        # ── 3. Relatórios ERPNext ─────────────────────────────────────────────
        {
            "doctype": "GF Skill",
            "internal_name": "gf_skill_erpnext_relatorios",
            "skill_name": "Relatórios ERPNext",
            "short_description": "Gera relatórios HTML responsivos para ERPNext com tabelas de dados, KPIs, gráficos e seção de análise gerencial.",
            "category": "ERPNext",
            "status": "Ativo",
            "active": 1,
            "version": "1.0.0",
            "version_notes": "Versão inicial — cobre relatórios gerenciais, operacionais e de auditoria.",
            "skill_owner": admin,
            "tags": "erpnext, relatório, html, dashboard, kpi, gerencial",
            "output_type": "HTML",
            "default_language": "Português (BR)",
            "skill_priority": "Alta",
            "allow_export": 1,
            "allow_api_usage": 1,
            "is_system_skill": 0,
            "purpose": (
                "Produzir relatórios HTML completos e responsivos compatíveis com o ambiente ERPNext/Frappe, "
                "contendo cabeçalho corporativo, seção de KPIs, tabelas de dados formatadas, gráficos descritivos "
                "e análise gerencial. O output deve ser renderizável diretamente no campo HTML do ERPNext."
            ),
            "when_to_use": (
                "- Geração de relatórios gerenciais periódicos (mensal, trimestral, anual)\n"
                "- Relatórios de auditoria e conformidade\n"
                "- Dashboards estáticos para apresentação executiva\n"
                "- Exportação de dados operacionais com contexto analítico"
            ),
            "when_not_to_use": (
                "- Relatórios que exijam dados em tempo real via WebSocket\n"
                "- Integrações que precisem de saída JSON pura sem formatação\n"
                "- Análises estatísticas complexas (use Python/pandas)"
            ),
            "main_instructions": (
                "1. Iniciar com cabeçalho contendo logo, título do relatório, período e data de geração.\n"
                "2. Exibir bloco de KPIs com cards destacados para métricas principais.\n"
                "3. Apresentar tabela de dados com cabeçalho fixo, linhas alternadas e totalizadores.\n"
                "4. Incluir seção de análise textual com destaques positivos, pontos de atenção e recomendações.\n"
                "5. Finalizar com rodapé: gerado por, sistema, data/hora e versão do relatório.\n"
                "6. Garantir que todo o HTML seja inline (sem dependências externas) e responsivo."
            ),
            "mandatory_rules": (
                "- Todo CSS deve ser inline ou em <style> no próprio documento.\n"
                "- Nenhuma dependência de CDN externo — o relatório deve funcionar offline.\n"
                "- Tabelas devem sempre ter cabeçalho <thead> e rodapé <tfoot> com totais.\n"
                "- KPIs com variação devem indicar tendência (↑ verde / ↓ vermelho)."
            ),
            "forbidden_actions": (
                "- Não usar frameworks externos (Bootstrap CDN, jQuery CDN).\n"
                "- Não omitir período de referência dos dados.\n"
                "- Não misturar moedas sem conversão explícita."
            ),
            "validation_checklist": (
                "[ ] Cabeçalho com título, período e data de geração\n"
                "[ ] KPIs com valores e variação de tendência\n"
                "[ ] Tabela com thead, tbody e tfoot\n"
                "[ ] CSS 100% inline/interno\n"
                "[ ] Análise textual com destaques e recomendações\n"
                "[ ] Rodapé com metadados do relatório\n"
                "[ ] Testado em modo de impressão"
            ),
            "writing_style": "Gerencial, objetivo, analítico. Bullet points para destaques. Sem jargão técnico desnecessário.",
            "visual_style": "Clean, corporativo. Paleta neutra (branco/cinza) com destaques em verde/vermelho para variações.",
            "tone_of_voice": "Profissional, informativo, orientado a decisões.",
            "formatting_rules": (
                "- Largura máxima: 1200px centralizado\n"
                "- Cards KPI: grid de 4 colunas, borda esquerda colorida\n"
                "- Tabelas: linhas zebradas, cabeçalho escuro\n"
                "- Fonte: system-ui ou Arial, 14px base\n"
                "- Sem bordas externas pesadas — usar sombra sutil"
            ),
            "version_history": "v1.0.0 → criação inicial em 2026-05-18",
        },

        # ── 4. Prompt de Automação Industrial — CLP/Altus ────────────────────
        {
            "doctype": "GF Skill",
            "internal_name": "gf_skill_industrial_clp_altus",
            "skill_name": "Automação Industrial — CLP/Altus",
            "short_description": "Gera lógica ladder, ST e documentação técnica para CLPs Altus série Nexto, com foco em segurança, rastreabilidade e boas práticas IEC 61131-3.",
            "category": "Industrial",
            "status": "Ativo",
            "active": 1,
            "version": "1.0.0",
            "version_notes": "Versão inicial — cobre programação Nexto MX e NX, comunicação MODBUS e documentação de blocos funcionais.",
            "skill_owner": admin,
            "tags": "clp, altus, nexto, ladder, ST, IEC61131, automação, industrial",
            "output_type": "Documentação",
            "default_language": "Português (BR)",
            "skill_priority": "Alta",
            "allow_export": 1,
            "allow_api_usage": 0,
            "is_system_skill": 0,
            "purpose": (
                "Auxiliar engenheiros de automação na criação, documentação e revisão de programas para CLPs "
                "Altus série Nexto, seguindo a norma IEC 61131-3. O Skill cobre lógica ladder, texto estruturado (ST), "
                "mapeamento de tags, configuração de comunicação MODBUS/TCP e documentação de blocos funcionais (FB)."
            ),
            "when_to_use": (
                "- Criação de lógica ladder ou ST para automação de processos industriais\n"
                "- Documentação de programas existentes para manutenção e auditoria\n"
                "- Mapeamento de endereços MODBUS e tags do processo\n"
                "- Geração de blocos funcionais reutilizáveis (FB)\n"
                "- Revisão de segurança de programas (fail-safe, interlocks)"
            ),
            "when_not_to_use": (
                "- CLPs de outros fabricantes sem confirmação de compatibilidade sintática\n"
                "- Programação de sistemas de segurança SIL sem validação por engenheiro certificado\n"
                "- Simulações em tempo real sem ambiente de teste configurado"
            ),
            "main_instructions": (
                "1. Sempre iniciar com a declaração de variáveis (VAR, VAR_INPUT, VAR_OUTPUT, VAR_GLOBAL).\n"
                "2. Nomear tags seguindo o padrão: [ÁREA]_[INSTRUMENTO]_[NÚMERO] (ex.: FORNO1_TC_001).\n"
                "3. Comentar cada rung/bloco com propósito, condição de ativação e saída esperada.\n"
                "4. Implementar interlocks de segurança antes de ações de acionamento.\n"
                "5. Incluir lógica de alarme (AL_) para cada condição crítica.\n"
                "6. Documentar endereço MODBUS de cada variável mapeada externamente.\n"
                "7. Finalizar com tabela de tags: Nome | Tipo | Endereço | Descrição | Unidade."
            ),
            "mandatory_rules": (
                "- Interlocks de segurança devem preceder SEMPRE qualquer acionamento de atuador.\n"
                "- Variáveis globais devem ser declaradas em GVL separada.\n"
                "- Toda FB deve ter bloco de documentação com: Autor, Data, Versão, Descrição.\n"
                "- Endereços MODBUS devem ser registrados na tabela de mapeamento."
            ),
            "forbidden_actions": (
                "- Não usar endereços de memória absolutos sem declaração de tag associada.\n"
                "- Não omitir condição de reset em lógicas set/reset.\n"
                "- Não implementar acionamento direto sem interlock de segurança.\n"
                "- Não deixar entradas analógicas sem tratamento de valor fora de faixa."
            ),
            "validation_checklist": (
                "[ ] Declaração completa de variáveis (VAR / GVL)\n"
                "[ ] Tags nomeadas no padrão [ÁREA]_[INSTRUMENTO]_[NÚM]\n"
                "[ ] Todos os rungs/blocos comentados\n"
                "[ ] Interlocks de segurança implementados\n"
                "[ ] Lógica de alarme para condições críticas\n"
                "[ ] Tabela de mapeamento de tags com endereço MODBUS\n"
                "[ ] FB documentadas com autor, data e versão"
            ),
            "writing_style": "Técnico, preciso, estruturado. Comentários concisos no código. Documentação em prosa técnica.",
            "visual_style": "Código formatado com indentação consistente. Tabelas de mapeamento com bordas claras.",
            "tone_of_voice": "Técnico, direto, orientado à segurança operacional.",
            "formatting_rules": (
                "- Código ST: indentação 4 espaços, palavras-chave em MAIÚSCULAS\n"
                "- Comentários de rung: (* Propósito: ... | Condição: ... | Saída: ... *)\n"
                "- Tabela de tags: Nome | Tipo | Endereço | Descrição | Unidade\n"
                "- Blocos FB: cabeçalho padronizado com 5 campos obrigatórios"
            ),
            "version_history": "v1.0.0 → criação inicial em 2026-05-18",
        },

        # ── 5. Documentação HTML Corporativa GF Atlas ─────────────────────────
        {
            "doctype": "GF Skill",
            "internal_name": "gf_skill_html_corporativo_gf",
            "skill_name": "Documentação HTML Corporativa GF Atlas",
            "short_description": "Gera documentação HTML inline completa no padrão visual GF Atlas: cabeçalho, metadados, cards de seção, blocos de código, alertas e rodapé corporativo.",
            "category": "HTML",
            "status": "Ativo",
            "active": 1,
            "version": "1.0.0",
            "version_notes": "Versão inicial — padrão oficial GF Atlas para documentação interna no ERPNext.",
            "skill_owner": admin,
            "tags": "html, documentação, gf atlas, corporativo, erpnext, inline",
            "output_type": "HTML",
            "default_language": "Português (BR)",
            "skill_priority": "Crítica",
            "allow_export": 1,
            "allow_api_usage": 1,
            "is_system_skill": 1,
            "purpose": (
                "Gerar documentação técnica e operacional em HTML inline, compatível com o campo de texto rico "
                "do ERPNext/Frappe, seguindo o padrão visual GF Atlas. O output deve ser auto-contido, "
                "responsivo e renderizável sem dependências externas, mantendo identidade visual corporativa "
                "consistente em todos os documentos do sistema."
            ),
            "when_to_use": (
                "- Criação de documentação técnica para DocTypes, módulos e processos\n"
                "- Manuais de uso interno para usuários do ERPNext\n"
                "- Documentação de APIs e integrações no padrão corporativo\n"
                "- Relatórios e guias de onboarding"
            ),
            "when_not_to_use": (
                "- Documentação destinada a publicação externa (use formato diferente)\n"
                "- Conteúdo que precise de interatividade JavaScript avançada\n"
                "- Documentos com imagens pesadas que não possam ser base64"
            ),
            "main_instructions": (
                "1. Abrir com <div class='gf-doc'> contendo todo o CSS inline em <style> dedicada.\n"
                "2. Cabeçalho: faixa escura (#1e293b) com título, subtítulo e metadados (versão, data, responsável).\n"
                "3. Cada seção principal deve ser um card com título em faixa destacada e conteúdo em área branca.\n"
                "4. Blocos de código: fundo #0f172a, fonte monospace, syntax highlight manual com <span>.\n"
                "5. Alertas: 4 tipos — info (azul), sucesso (verde), aviso (amarelo), perigo (vermelho).\n"
                "6. Tabelas: cabeçalho #1e293b branco, linhas zebradas #f8fafc/#ffffff.\n"
                "7. Rodapé: faixa cinza com sistema, versão, data de geração e gerado por."
            ),
            "mandatory_rules": (
                "- Todo CSS deve ser inline no documento — absolutamente nenhuma dependência externa.\n"
                "- Paleta principal: #1e293b (primário), #059669 (acento), #f8fafc (fundo).\n"
                "- Fonte: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif.\n"
                "- Largura máxima do documento: 960px, centralizado.\n"
                "- Versão do documento sempre visível no cabeçalho."
            ),
            "forbidden_actions": (
                "- Não usar links para CSS externos (Bootstrap CDN, Google Fonts etc.).\n"
                "- Não usar JavaScript no documento.\n"
                "- Não usar cores fora da paleta corporativa sem justificativa.\n"
                "- Não omitir seção de rodapé."
            ),
            "validation_checklist": (
                "[ ] CSS 100% inline — zero dependências externas\n"
                "[ ] Cabeçalho com título, versão e metadados\n"
                "[ ] Todas as seções em cards padronizados\n"
                "[ ] Blocos de código com fundo escuro e monospace\n"
                "[ ] Alertas nos 4 tipos quando aplicável\n"
                "[ ] Tabelas com cabeçalho escuro e linhas zebradas\n"
                "[ ] Rodapé corporativo presente\n"
                "[ ] Paleta de cores em conformidade com padrão GF Atlas"
            ),
            "writing_style": "Técnico, claro, didático. Parágrafos curtos. Bullet points para listas operacionais.",
            "visual_style": "Enterprise clean. Paleta slate/verde. Cards com sombra sutil. Tipografia system-ui.",
            "tone_of_voice": "Profissional, técnico, confiável.",
            "formatting_rules": (
                "- Largura máx.: 960px, margin: 0 auto\n"
                "- Cards: border-radius 8px, box-shadow 0 1px 3px rgba(0,0,0,.08)\n"
                "- Cabeçalho card: background #1e293b, color #f8fafc, padding 14px 20px\n"
                "- Corpo card: background #fff, padding 20px\n"
                "- Alertas: border-left 4px solid [cor-tipo], background [cor-tipo-pale]"
            ),
            "version_history": "v1.0.0 → criação inicial em 2026-05-18",
        },

        # ── 6. Gestão de Knowledge Hub ────────────────────────────────────────
        {
            "doctype": "GF Skill",
            "internal_name": "gf_skill_ia_knowledge_hub",
            "skill_name": "Gestão de Knowledge Hub",
            "short_description": "Estrutura, organiza e mantém bases de conhecimento corporativo para uso por agentes de IA, incluindo indexação, metadados e políticas de atualização.",
            "category": "IA e Agentes",
            "status": "Ativo",
            "active": 1,
            "version": "1.0.0",
            "version_notes": "Versão inicial — cobre estruturação de KB para RAG, agentes e automação corporativa.",
            "skill_owner": admin,
            "tags": "knowledge hub, IA, RAG, agentes, base de conhecimento, indexação, corporativo",
            "output_type": "Documentação",
            "default_language": "Português (BR)",
            "skill_priority": "Alta",
            "allow_export": 1,
            "allow_api_usage": 1,
            "is_system_skill": 0,
            "purpose": (
                "Estruturar e manter bases de conhecimento corporativo otimizadas para recuperação por agentes de IA "
                "(RAG — Retrieval-Augmented Generation), garantindo que cada documento contenha metadados adequados, "
                "seja redigido para maximizar relevância semântica e siga políticas de revisão e versionamento "
                "que mantenham a base atualizada e confiável."
            ),
            "when_to_use": (
                "- Criação de novos documentos para a base de conhecimento corporativo\n"
                "- Revisão e atualização de documentos existentes no Knowledge Hub\n"
                "- Estruturação de metadados para indexação em sistemas RAG\n"
                "- Definição de políticas de atualização e descarte de conhecimento obsoleto\n"
                "- Onboarding de novos domínios de conhecimento ao sistema de IA"
            ),
            "when_not_to_use": (
                "- Documentos confidenciais que não devem ser acessados por agentes\n"
                "- Conhecimento altamente volátil sem processo de atualização definido\n"
                "- Dados estruturados que pertencem a banco de dados (use queries, não KB)"
            ),
            "main_instructions": (
                "1. Definir metadados obrigatórios: título, domínio, palavras-chave, versão, data de revisão e owner.\n"
                "2. Estruturar o documento em chunks semânticos de 200-500 palavras para otimizar recuperação.\n"
                "3. Iniciar cada chunk com uma pergunta ou afirmação que o documento responde (anchor semântico).\n"
                "4. Evitar pronomes ambíguos — cada chunk deve ser compreensível isoladamente.\n"
                "5. Incluir seção de 'Termos Relacionados' para ampliar cobertura semântica.\n"
                "6. Definir data de revisão obrigatória (máximo 6 meses para conhecimento operacional).\n"
                "7. Marcar explicitamente informações que podem mudar com frequência."
            ),
            "mandatory_rules": (
                "- Cada documento deve ter metadados completos no cabeçalho (YAML ou bloco estruturado).\n"
                "- Chunks de máximo 500 palavras — dividir documentos longos em múltiplos chunks.\n"
                "- Data de revisão obrigatória — documentos sem revisão nos últimos 6 meses são automaticamente marcados como 'Pendente de Revisão'.\n"
                "- Nomenclatura de arquivos: [domínio]_[assunto]_[versão].md"
            ),
            "forbidden_actions": (
                "- Não incluir dados pessoais (LGPD) sem processo de anonimização.\n"
                "- Não criar chunks com menos de 100 palavras — perdem contexto semântico.\n"
                "- Não referenciar sistemas ou processos sem indicar se são vigentes ou legados.\n"
                "- Não deixar documentos sem owner responsável pela manutenção."
            ),
            "validation_checklist": (
                "[ ] Metadados completos (título, domínio, keywords, versão, data, owner)\n"
                "[ ] Chunks entre 100-500 palavras\n"
                "[ ] Cada chunk compreensível isoladamente\n"
                "[ ] Anchor semântico no início de cada chunk\n"
                "[ ] Seção 'Termos Relacionados' presente\n"
                "[ ] Data de revisão definida (máx. 6 meses)\n"
                "[ ] Nenhum dado pessoal sem anonimização\n"
                "[ ] Owner responsável identificado"
            ),
            "writing_style": "Claro, direto, sem ambiguidade. Frases curtas. Vocabulário consistente em todo o documento.",
            "visual_style": "Estruturado com seções claras. Metadados em bloco destacado. Termos técnicos em destaque.",
            "tone_of_voice": "Informativo, confiável, orientado ao uso por sistemas automatizados.",
            "formatting_rules": (
                "- Cabeçalho YAML: título, domínio, keywords, versão, revisão, owner\n"
                "- Seções: H2 para domínios, H3 para chunks\n"
                "- Termos técnicos: **negrito** na primeira ocorrência\n"
                "- Seção final obrigatória: 'Termos Relacionados' e 'Data da Próxima Revisão'"
            ),
            "version_history": "v1.0.0 → criação inicial em 2026-05-18",
        },
    ]

    for skill_data in skills:
        if frappe.db.exists("GF Skill", skill_data["internal_name"]):
            continue
        doc = frappe.get_doc(skill_data)
        doc.insert(ignore_permissions=True)
        print(f"GF Atlas App: Skill '{skill_data['skill_name']}' criado.")


# ─────────────────────────────────────────────────────────────────────────────
# SAMPLE CONTENT REGISTRY
# Registros de exemplo para o GF Content Registry.
# Criados apenas se o título ainda não existir no banco.
# ─────────────────────────────────────────────────────────────────────────────

def create_sample_content_registry():
    records = [
        {
            "doctype": "GF Content Registry",
            "title": "Relatório de Horas — Timesheet",
            "item_type": "REPORT",
            "status": "Submetido",
            "content_group": "1_0010_070_relatorios_financeiros",
            "access_group": "financeiro",
            "skill": "gf_skill_erpnext_relatorios",
            "route_url": "/app/query-report/Timesheet",
            "reference_doctype": "Timesheet",
            "description": "Relatório gerencial de horas apontadas por colaborador e projeto.",
            "tags": "timesheet, horas, produção, relatório",
            "icon": "clock",
            "sort_order": 10,
            "show_on_home": 0,
            "favorite": 0,
            "active": 1,
        },
        {
            "doctype": "GF Content Registry",
            "title": "Especificação Técnica de Peças — Padrão GF",
            "item_type": "DOCUMENT",
            "status": "Submetido",
            "content_group": "1_0060_100_especificacoes_tecnicas",
            "access_group": "engenharia",
            "skill": "gf_skill_eng_pecas_tecnicas",
            "description": "Padrão corporativo para elaboração de especificações técnicas de peças usinadas e soldadas.",
            "tags": "engenharia, peças, especificação, usinagem",
            "icon": "file-check",
            "sort_order": 20,
            "show_on_home": 0,
            "favorite": 0,
            "active": 1,
        },
        {
            "doctype": "GF Content Registry",
            "title": "GF Skill — Central de Skills Corporativos",
            "item_type": "APPLICATION",
            "status": "Submetido",
            "content_group": "1_0210_030_aplicacoes_web",
            "access_group": "tecnologia_da_informacao",
            "skill": "gf_skill_html_corporativo_gf",
            "route_url": "/gf-skill",
            "description": "Aplicação interna para gestão e consulta dos Skills corporativos do GF Atlas.",
            "tags": "gf atlas, skills, documentação, ia",
            "icon": "zap",
            "sort_order": 1,
            "show_on_home": 1,
            "favorite": 1,
            "active": 1,
        },
        {
            "doctype": "GF Content Registry",
            "title": "Procedimento de Codificação de Produtos GF",
            "item_type": "DOCUMENT",
            "status": "Submetido",
            "content_group": "1_0050_010_estoque",
            "access_group": "suprimentos",
            "skill": "gf_skill_html_corporativo_gf",
            "description": "Procedimento interno que define o padrão GF.000.0000 para codificação de produtos no ERPNext.",
            "tags": "cadastro, produtos, codificação, padrão",
            "icon": "package",
            "sort_order": 30,
            "show_on_home": 0,
            "favorite": 0,
            "active": 1,
        },
    ]

    for rec in records:
        if frappe.db.exists("GF Content Registry", {"title": rec["title"]}):
            continue
        doc = frappe.get_doc(rec)
        doc.insert(ignore_permissions=True)
        print(f"GF Atlas App: Content Registry '{rec['title']}' criado.")

    print("GF Atlas App: campos Auxiliary Block 1 e 2 criados em Web Page.")
