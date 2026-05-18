INSTRUÇÃO INICIAL PARA DESENVOLVIMENTO DO GF SKILL
================================================================================

Com base em todas as informações descritas abaixo, desenvolver integralmente o
Doctype `GF Skill` dentro do app em desenvolvimento, seguindo rigorosamente
toda a estrutura funcional, operacional, visual e de versionamento definida
neste documento.

Além do Doctype padrão do ERPNext/Frappe, desenvolver também uma interface
HTML moderna, sofisticada e independente da manutenção padrão do ERPNext,
funcionando como uma camada visual própria do app.

================================================================================
OBJETIVO DA INTERFACE
================================================================================

A interface deverá funcionar como um painel moderno de gestão de Skills,
prompts e inteligência operacional corporativa.

O objetivo é criar uma experiência premium e enterprise para:
- criação
- edição
- visualização
- versionamento
- navegação
- organização
- reutilização de Skills

Tudo de forma:
- intuitiva
- moderna
- altamente visual
- organizada
- rápida
- escalável

================================================================================
PADRÃO VISUAL OBRIGATÓRIO
================================================================================

Utilizar como referência visual principal:
- GF Atlas
- WikiHub
- Kino Land

Seguir rigorosamente:
- identidade visual moderna
- layout clean
- visual enterprise
- aparência sofisticada
- estrutura modular
- tipografia premium
- cards modernos
- navegação fluida
- componentes elegantes
- experiência semelhante a plataformas modernas SaaS enterprise

================================================================================
REQUISITOS DA INTERFACE HTML
================================================================================

A interface deve possuir:

- CRUD completo
- criação de registros
- edição de registros
- exclusão controlada
- visualização detalhada
- sistema de abas
- versionamento visual
- histórico de alterações
- filtros
- pesquisa dinâmica
- busca rápida
- visualização hierárquica
- status visual
- indicadores de versão
- painel lateral
- navegação inteligente
- responsividade total

================================================================================
PADRÃO DAS ABAS
================================================================================

A interface deve respeitar integralmente as abas definidas no documento:

1. Informações Gerais
2. Instruções
3. Estilo
4. Cabeçalho
5. Rodapé
6. Exemplo Completo
7. Campos Técnicos
8. Prompt Completo

================================================================================
REGRAS IMPORTANTES
================================================================================

- O `Full Prompt` deve ser gerado automaticamente
- O campo `Full Prompt` não pode ser editável manualmente
- O sistema deve consolidar automaticamente todas as informações
- O conteúdo deve ser regenerado automaticamente antes do Save
- O sistema deve seguir o padrão de versionamento do ERPNext/Frappe
- O Submit deve bloquear alterações estruturais diretas
- Novas alterações devem gerar nova versão do Skill
- O histórico deve permanecer rastreável

================================================================================
PADRÃO TÉCNICO
================================================================================

A interface deve ser desenvolvida:
- dentro do app
- desacoplada da UI padrão do ERPNext
- utilizando páginas customizadas
- com arquitetura limpa
- preparada para crescimento futuro

A manutenção deve ocorrer:
- via interface própria do app
- sem depender diretamente do Form padrão do ERPNext

================================================================================
EXPERIÊNCIA VISUAL ESPERADA
================================================================================

A tela deve transmitir sensação de:

- plataforma premium
- central de inteligência
- painel enterprise
- sistema moderno de IA
- gestão corporativa avançada
- biblioteca profissional de prompts
- SaaS moderno
- knowledge hub corporativo

================================================================================
RECURSOS VISUAIS SUGERIDOS
================================================================================

Implementar:
- animações suaves
- transições elegantes
- tabs modernas
- sidebar inteligente
- cards sofisticados
- indicadores de status
- timeline de versões
- editor monoespaçado para prompts
- syntax highlight
- botões premium
- dark/light mode preparado
- responsividade completa
- dashboard operacional

================================================================================
OBJETIVO FINAL
================================================================================

O resultado final deve transformar o `GF Skill` em:

- central corporativa de Skills
- biblioteca enterprise de prompts
- motor de inteligência operacional
- sistema de governança de IA
- plataforma reutilizável de automação
- knowledge hub enterprise
- estrutura moderna de versionamento e reutilização de prompts





GF Skill
================================================================================

OBJETIVO DO DOCTYPE
--------------------------------------------------------------------------------
Cadastro corporativo de Skills reutilizáveis para IA, prompts, documentações,
templates, automações, geração de HTML, relatórios, workflows e padrões
internos da empresa.

Cada Skill representa um conjunto organizado de:
- instruções
- comportamento
- estilo
- exemplos
- cabeçalhos
- rodapés
- padrões corporativos
- regras obrigatórias
- versionamento
- histórico evolutivo

O objetivo é transformar o `GF Skill` em uma biblioteca corporativa centralizada
de inteligência operacional, reutilização de prompts, governança documental e
padronização enterprise.

================================================================================
PADRÃO OPERACIONAL E VERSIONAMENTO
================================================================================

O cadastro do Doctype `GF Skill` deve seguir o padrão nativo de versionamento já
existente no ERPNext/Frappe Framework.

Fluxo operacional esperado:

1. O usuário cria o Skill normalmente.
2. O registro permanece editável enquanto estiver em Draft.
3. Após validação, o usuário executa Save + Submit.
4. Após o Submit, o registro torna-se protegido contra alterações estruturais.
5. Caso seja necessário realizar alterações futuras:
   - o registro atual pode ser marcado como:
     - Inativo
     - Obsoleto
     - Substituído
   - e uma nova versão do Skill deve ser criada.
6. O histórico entre versões deve permanecer rastreável dentro do sistema.

Objetivos:
- preservar histórico
- evitar perda de padronização
- manter rastreabilidade
- garantir governança
- permitir evolução segura dos Skills
- manter compatibilidade enterprise

================================================================================
CAMPOS OBRIGATÓRIOS
================================================================================

Os campos abaixo devem ser obrigatórios no cadastro do Skill:

- Skill Name
  → identificação principal do Skill

- Internal Name
  → identificador técnico único

- Category
  → categorização organizacional

- Version
  → controle de versionamento

- Status
  → situação operacional do Skill

- Owner
  → responsável pelo Skill

- Short Description
  → resumo operacional

- Purpose
  → objetivo principal do Skill

- Main Instructions
  → regras principais de execução

- Mandatory Rules
  → regras críticas obrigatórias

- Writing Style
  → padrão textual

- Visual Style
  → padrão visual

- Output Type
  → tipo principal de saída

- Active
  → controle operacional de disponibilidade

================================================================================
PADRÃO DE EVOLUÇÃO DAS VERSÕES
================================================================================

Exemplo esperado:

- v1.0.0 → criação inicial
- v1.1.0 → ajustes visuais
- v1.2.0 → inclusão de novas regras
- v2.0.0 → revisão estrutural completa

O sistema deve manter:
- versão atual
- versões anteriores
- data da revisão
- responsável pela alteração
- observações da alteração
- histórico de evolução

================================================================================
PADRÃO VISUAL DOS CAMPOS
================================================================================

Todos os campos do cadastro devem possuir:

- Label amigável
- Pequeno texto explicativo abaixo do campo
- Linguagem clara e objetiva
- Padrão visual do ERPNext/Frappe
- Auxílio operacional ao usuário

Objetivos:
- facilitar preenchimento
- reduzir erros
- acelerar onboarding
- melhorar experiência do usuário
- tornar o cadastro autoexplicativo

================================================================================
ABA 1 — Informações Gerais
================================================================================

Skill Name
Descrição:
Nome principal do Skill exibido para os usuários.

Obrigatório:
SIM

Texto auxiliar abaixo do campo:
Nome amigável utilizado para identificação principal do Skill.

Exemplo:
Documentação Interna HTML


Internal Name
Descrição:
Nome técnico interno utilizado pelo sistema, APIs e integrações.

Obrigatório:
SIM

Texto auxiliar abaixo do campo:
Identificador técnico único utilizado internamente pelo sistema.

Exemplo:
gf_internal_html_documentation


Category
Descrição:
Categoria principal do Skill.

Obrigatório:
SIM

Texto auxiliar abaixo do campo:
Define o agrupamento funcional e organizacional do Skill.

Sugestões de categorias:

- Documentação
  → Skills voltados para documentação técnica e corporativa

- HTML
  → Geração de HTML simples, inline ou páginas web

- ERPNext
  → Regras específicas para ERPNext/Frappe

- Relatórios
  → Geração de relatórios técnicos, financeiros e operacionais

- Prompt Engineering
  → Estruturas de prompts inteligentes

- Automação
  → Workflows, integrações e automações

- IA e Agentes
  → Skills para IA, agentes e MCPs

- Programação
  → Skills para geração de código

- SQL e Banco de Dados
  → Queries, modelagem e banco de dados

- APIs e Integrações
  → APIs REST, integrações e webhooks

- Frontend
  → UI, UX, páginas e componentes

- Backend
  → Lógica de negócio e serviços

- DevOps e Cloud
  → Infraestrutura, deploy e cloud

- Segurança
  → Segurança, LGPD, autenticação e compliance

- Comercial
  → Propostas, apresentações e vendas

- Engenharia
  → Engenharia industrial e processos

- Industrial
  → Processos fabris e chão de fábrica

- Qualidade
  → Controle de qualidade e inspeções

- Financeiro
  → Fluxos financeiros e indicadores

- Jurídico
  → Contratos e compliance

- RH
  → Recursos humanos e treinamentos

- Templates
  → Modelos reutilizáveis

- Padrões Corporativos
  → Padronizações internas

- Outros
  → Categoria genérica


Version
Descrição:
Versão atual do Skill.

Obrigatório:
SIM

Texto auxiliar abaixo do campo:
Versão atual seguindo padrão corporativo de versionamento.

Exemplo:
1.0.0


Version Notes
Descrição:
Descrição resumida das alterações realizadas na versão atual.

Obrigatório:
NÃO

Texto auxiliar abaixo do campo:
Resumo rápido das alterações realizadas nesta versão do Skill.


Status
Descrição:
Status operacional do Skill.

Obrigatório:
SIM

Texto auxiliar abaixo do campo:
Define a situação atual do Skill dentro do sistema.

Sugestões:
- Draft
- Em Desenvolvimento
- Em Teste
- Ativo
- Obsoleto
- Arquivado


Owner
Descrição:
Usuário responsável pelo Skill.

Obrigatório:
SIM

Texto auxiliar abaixo do campo:
Usuário principal responsável pela manutenção do Skill.


Short Description
Descrição:
Resumo rápido do propósito do Skill.

Obrigatório:
SIM

Texto auxiliar abaixo do campo:
Descrição curta utilizada em listas, buscas e consultas rápidas.


Purpose
Descrição:
Objetivo principal e responsabilidade do Skill.

Obrigatório:
SIM

Texto auxiliar abaixo do campo:
Explica claramente o propósito operacional do Skill.


When to Use
Descrição:
Situações recomendadas para utilização do Skill.

Obrigatório:
NÃO

Texto auxiliar abaixo do campo:
Define os cenários ideais para utilização deste Skill.


When Not to Use
Descrição:
Situações onde o Skill não deve ser utilizado.

Obrigatório:
NÃO

Texto auxiliar abaixo do campo:
Define limitações e situações inadequadas para uso do Skill.


Tags
Descrição:
Palavras-chave para pesquisa e organização.

Obrigatório:
NÃO

Texto auxiliar abaixo do campo:
Facilita localização, indexação e agrupamento dos Skills.


Active
Descrição:
Define se o Skill está ativo no sistema.

Obrigatório:
SIM

Texto auxiliar abaixo do campo:
Controla disponibilidade operacional do Skill.

================================================================================
ABA 2 — Instruções
================================================================================

Main Instructions
Descrição:
Instruções principais e comportamento obrigatório do Skill.

Obrigatório:
SIM

Texto auxiliar abaixo do campo:
Define as regras centrais que a IA ou usuário deve seguir.


Mandatory Rules
Descrição:
Regras obrigatórias que nunca podem ser ignoradas.

Obrigatório:
SIM

Texto auxiliar abaixo do campo:
Define regras críticas e obrigatórias do Skill.


Forbidden Actions
Descrição:
Ações proibidas para o Skill.

Obrigatório:
NÃO

Texto auxiliar abaixo do campo:
Define comportamentos proibidos durante a utilização.


Validation Checklist
Descrição:
Checklist interno de validação antes da resposta final.

Obrigatório:
NÃO

Texto auxiliar abaixo do campo:
Lista de verificações obrigatórias antes da conclusão da execução.

================================================================================
ABA 3 — Estilo
================================================================================

Writing Style
Descrição:
Define o estilo textual da resposta.

Obrigatório:
SIM

Texto auxiliar abaixo do campo:
Define como os textos devem ser escritos.

Exemplo:
Objetivo, técnico, corporativo e didático.


Visual Style
Descrição:
Define o padrão visual esperado.

Obrigatório:
SIM

Texto auxiliar abaixo do campo:
Define aparência visual geral do conteúdo gerado.

Exemplo:
Clean, moderno, enterprise e minimalista.


Tone of Voice
Descrição:
Tom da comunicação.

Obrigatório:
NÃO

Texto auxiliar abaixo do campo:
Define o tom geral da comunicação.

Exemplo:
Profissional, técnico e confiável.


Formatting Rules
Descrição:
Regras de formatação visual e estrutural.

Obrigatório:
NÃO

Texto auxiliar abaixo do campo:
Define padrões estruturais obrigatórios de formatação.

================================================================================
ABA 4 — Cabeçalho
================================================================================

Header Template
Descrição:
Modelo padrão de cabeçalho utilizado pelo Skill.

Obrigatório:
NÃO

Texto auxiliar abaixo do campo:
Estrutura visual e textual do cabeçalho padrão.


Header Notes
Descrição:
Observações e regras específicas do cabeçalho.

Obrigatório:
NÃO

Texto auxiliar abaixo do campo:
Regras adicionais relacionadas ao cabeçalho.

================================================================================
ABA 5 — Rodapé
================================================================================

Footer Template
Descrição:
Modelo padrão de rodapé utilizado pelo Skill.

Obrigatório:
NÃO

Texto auxiliar abaixo do campo:
Estrutura visual e textual do rodapé padrão.


Footer Notes
Descrição:
Observações e regras específicas do rodapé.

Obrigatório:
NÃO

Texto auxiliar abaixo do campo:
Regras adicionais relacionadas ao rodapé.

================================================================================
ABA 6 — Exemplo Completo
================================================================================

Full Example
Descrição:
Exemplo completo real do resultado esperado.

Obrigatório:
NÃO

Texto auxiliar abaixo do campo:
Modelo completo utilizado como referência operacional.


Example Notes
Descrição:
Observações importantes sobre o exemplo.

Obrigatório:
NÃO

Texto auxiliar abaixo do campo:
Comentários e observações complementares sobre o exemplo.

================================================================================
ABA 7 — Campos Técnicos
================================================================================

Prompt File Name
Descrição:
Nome padrão do arquivo relacionado ao Skill.

Obrigatório:
NÃO

Texto auxiliar abaixo do campo:
Nome técnico do arquivo utilizado para exportação ou armazenamento.

Exemplo:
GF_INTERNAL_HTML_RULES.md


Related Module
Descrição:
Módulo relacionado dentro do ERPNext/Frappe.

Obrigatório:
NÃO

Texto auxiliar abaixo do campo:
Define o módulo principal relacionado ao Skill.


Related Doctype
Descrição:
Doctype relacionado ao Skill.

Obrigatório:
NÃO

Texto auxiliar abaixo do campo:
Define relacionamento com outros Doctypes do sistema.


Output Type
Descrição:
Tipo principal de saída gerada.

Obrigatório:
SIM

Texto auxiliar abaixo do campo:
Define o formato principal esperado da saída do Skill.

Sugestões:
- HTML
- Markdown
- Texto
- JSON
- SQL
- Python
- JavaScript
- CSS
- XML
- YAML
- Relatório
- Prompt
- Documentação
- API
- Workflow
- Outro


Default Language
Descrição:
Idioma padrão utilizado pelo Skill.

Obrigatório:
NÃO

Texto auxiliar abaixo do campo:
Define idioma principal esperado das respostas.


Last Reviewed On
Descrição:
Data da última revisão técnica do Skill.

Obrigatório:
NÃO

Texto auxiliar abaixo do campo:
Data da última validação técnica realizada.


Review Notes
Descrição:
Observações da revisão mais recente.

Obrigatório:
NÃO

Texto auxiliar abaixo do campo:
Comentários técnicos da última revisão.


Version History
Descrição:
Histórico resumido de evolução do Skill.

Obrigatório:
NÃO

Texto auxiliar abaixo do campo:
Mantém rastreabilidade resumida da evolução do Skill.

Exemplo:
- v1.0.0 → criação inicial
- v1.1.0 → inclusão de regras HTML inline
- v1.2.0 → padronização de cabeçalhos
- v2.0.0 → revisão estrutural completa


Is System Skill
Descrição:
Define se o Skill é sistêmico e protegido contra alterações críticas.

Obrigatório:
NÃO

Texto auxiliar abaixo do campo:
Protege Skills internos críticos do sistema.


Allow Export
Descrição:
Permite exportação do Skill para arquivos externos.

Obrigatório:
NÃO

Texto auxiliar abaixo do campo:
Define se o Skill pode ser exportado.


Allow API Usage
Descrição:
Permite utilização do Skill via APIs e integrações externas.

Obrigatório:
NÃO

Texto auxiliar abaixo do campo:
Define se APIs externas podem utilizar este Skill.


Skill Priority
Descrição:
Prioridade operacional do Skill dentro do sistema.

Obrigatório:
NÃO

Texto auxiliar abaixo do campo:
Define prioridade operacional e importância do Skill.

Sugestões:
- Baixa
- Normal
- Alta
- Crítica

================================================================================
ABA 8 — Prompt Completo
================================================================================

OBJETIVO DA ABA
--------------------------------------------------------------------------------
Esta aba será responsável por armazenar automaticamente o Prompt Final Completo
gerado a partir da consolidação de todas as informações preenchidas nas abas
anteriores do cadastro do `GF Skill`.

O objetivo é transformar o cadastro estruturado em um prompt único,
padronizado, consolidado e reutilizável.

================================================================================
COMPORTAMENTO OPERACIONAL
================================================================================

O campo desta aba NÃO deve ser editável manualmente pelo usuário.

O conteúdo será:
- gerado automaticamente
- consolidado dinamicamente
- reconstruído a cada salvamento
- atualizado automaticamente antes do Save

Fluxo esperado:

1. Usuário preenche os campos das abas anteriores
2. Sistema consolida automaticamente:
   - informações gerais
   - instruções
   - estilo
   - cabeçalho
   - rodapé
   - exemplos
   - configurações técnicas
3. Antes do salvamento:
   - o sistema monta automaticamente o Prompt Completo
4. O resultado consolidado é armazenado nesta aba

================================================================================
NOME DO CAMPO
================================================================================

Full Prompt

================================================================================
TIPO DO CAMPO
================================================================================

Code
ou
Long Text

Preferencialmente:
Code

Motivos:
- melhor visualização
- melhor cópia
- preservação de estrutura
- leitura técnica facilitada

================================================================================
CONFIGURAÇÕES DO CAMPO
================================================================================

Read Only:
SIM

Allow On Submit:
SIM

Track Changes:
SIM

Copy Button:
SIM

Monospace:
SIM

================================================================================
OBJETIVO DO FULL PROMPT
================================================================================

O campo `Full Prompt` será utilizado para:

- exportação
- reutilização
- APIs
- IA
- MCPs
- automações
- geração dinâmica
- versionamento
- integração futura
- biblioteca corporativa de prompts

================================================================================
PADRÃO DE CONSOLIDAÇÃO
================================================================================

O sistema deve consolidar automaticamente:

- nome do Skill
- categoria
- propósito
- regras
- estilo
- formatação
- exemplos
- cabeçalho
- rodapé
- observações
- regras obrigatórias
- restrições
- checklist
- informações técnicas

Tudo em um único prompt final estruturado.

================================================================================
REGRAS IMPORTANTES
================================================================================

- O usuário NÃO deve editar manualmente o Full Prompt
- O campo deve sempre refletir a versão mais recente
- O conteúdo deve ser regenerado automaticamente
- O sistema deve evitar duplicações
- O prompt consolidado deve manter estrutura organizada
- O prompt deve ser formatado de forma legível
- O conteúdo deve ser compatível com IA e APIs

================================================================================
SUGESTÃO TÉCNICA
================================================================================

A geração do `Full Prompt` pode ocorrer:

- before_save
ou
- validate

do Frappe Framework.

Sugestão recomendada:
before_save

Motivo:
garante atualização automática antes do registro ser salvo.

================================================================================
RESULTADO FINAL ESPERADO
================================================================================

O `GF Skill` deve funcionar como:

- biblioteca corporativa de Skills
- central de padrões internos
- motor de prompts reutilizáveis
- estrutura governada de IA
- base de conhecimento versionada
- sistema enterprise de reutilização operacional
- núcleo de padronização corporativa
- central de automação e inteligência operacional
- gerador corporativo de prompts
- biblioteca enterprise de inteligência operacional