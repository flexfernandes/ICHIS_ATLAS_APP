import frappe
from frappe.model.document import Document


class GFSkill(Document):

    def before_save(self):
        if self.status in ('Inativo', 'Obsoleto', 'Arquivado'):
            self.active = 0
        self.last_reviewed_on = frappe.utils.today()
        self.full_prompt = self._build_prompt()

    def before_submit(self):
        self.full_prompt = self._build_prompt()
        self.status = 'Submetido'

    # ──────────────────────────────────────────────
    def _build_prompt(self):
        parts = []

        def sec(title, content, note=None):
            if content and str(content).strip():
                if note:
                    parts.append(f"\n## {title}\n> {note}\n\n{str(content).strip()}")
                else:
                    parts.append(f"\n## {title}\n{str(content).strip()}")

        def flag(label, value):
            return f"- {label}: {'Sim' if value else 'Não'}"

        # ── Cabeçalho ────────────────────────────────────────────────────────
        parts.append(f"# {self.skill_name or '—'} — v{self.version or '1.0.0'}")

        meta = []
        if self.category:      meta.append(f"Categoria: {self.category}")
        if self.status:        meta.append(f"Status: {self.status}")
        if self.output_type:   meta.append(f"Output: {self.output_type}")
        if self.skill_owner:   meta.append(f"Responsável: {self.skill_owner}")
        if meta:
            parts.append("> " + " · ".join(meta))

        if self.short_description:
            parts.append(f"\n**{self.short_description.strip()}**")

        parts.append("\n---")

        # ── Propósito ────────────────────────────────────────────────────────
        sec("PROPÓSITO",
            self.purpose,
            "Este bloco define o objetivo central do Skill. "
            "Leia com atenção para compreender o que deve ser produzido e qual valor este Skill entrega.")

        if self.when_to_use or self.when_not_to_use:
            parts.append("\n---")
            sec("QUANDO USAR",
                self.when_to_use,
                "Utilize este Skill apenas nos cenários descritos abaixo.")
            sec("QUANDO NÃO USAR",
                self.when_not_to_use,
                "Nos cenários abaixo este Skill NÃO deve ser utilizado. Respeite estas limitações.")

        parts.append("\n---")

        # ── Instruções ───────────────────────────────────────────────────────
        sec("INSTRUÇÕES PRINCIPAIS",
            self.main_instructions,
            "Estas são as regras centrais de comportamento. "
            "Siga-as rigorosamente durante toda a execução deste Skill.")
        sec("REGRAS OBRIGATÓRIAS",
            self.mandatory_rules,
            "Regras críticas e não negociáveis. "
            "Devem ser obedecidas acima de qualquer outra instrução ou preferência do usuário.")
        sec("AÇÕES PROIBIDAS",
            self.forbidden_actions,
            "Os comportamentos listados abaixo são estritamente proibidos neste Skill.")
        sec("CHECKLIST DE VALIDAÇÃO",
            self.validation_checklist,
            "Antes de finalizar a resposta, verifique cada item desta lista. "
            "Só conclua quando todos os critérios estiverem atendidos.")

        parts.append("\n---")

        # ── Estilo ───────────────────────────────────────────────────────────
        sec("ESTILO DE ESCRITA",
            self.writing_style,
            "Adote este estilo de escrita em todo o conteúdo gerado.")
        sec("ESTILO VISUAL",
            self.visual_style,
            "A aparência visual do conteúdo gerado deve seguir estas diretrizes.")
        sec("TOM DE VOZ",
            self.tone_of_voice,
            "Mantenha este tom em toda a comunicação gerada pelo Skill.")
        sec("REGRAS DE FORMATAÇÃO",
            self.formatting_rules,
            "Padrões estruturais obrigatórios. "
            "Aplique-os em todos os elementos do conteúdo gerado.")

        # ── Cabeçalho / Rodapé ───────────────────────────────────────────────
        if self.header_template or self.footer_template:
            parts.append("\n---")
            sec("CABEÇALHO — TEMPLATE",
                self.header_template,
                "Use exatamente este template como cabeçalho de cada documento gerado.")
            sec("Observações do Cabeçalho", self.header_notes)
            sec("RODAPÉ — TEMPLATE",
                self.footer_template,
                "Use exatamente este template como rodapé de cada documento gerado.")
            sec("Observações do Rodapé", self.footer_notes)

        # ── Exemplo completo ─────────────────────────────────────────────────
        if self.full_example:
            parts.append("\n---")
            sec("EXEMPLO COMPLETO",
                self.full_example,
                "Este é o modelo de referência de qualidade. "
                "O conteúdo gerado deve ser comparado a este padrão antes de ser entregue.")
            sec("Observações do Exemplo", self.example_notes)

        # ── Informações técnicas ─────────────────────────────────────────────
        tech = []
        if self.prompt_file_name: tech.append(f"- Arquivo: `{self.prompt_file_name}`")
        if self.related_module:   tech.append(f"- Módulo: {self.related_module}")
        if self.related_doctype:  tech.append(f"- DocType: {self.related_doctype}")
        if self.default_language: tech.append(f"- Idioma: {self.default_language}")
        if self.skill_priority:   tech.append(f"- Prioridade: {self.skill_priority}")
        if self.last_reviewed_on: tech.append(f"- Última Revisão: {self.last_reviewed_on}")
        tech.append(flag("Exportável", self.allow_export))
        tech.append(flag("Uso via API", self.allow_api_usage))
        tech.append(flag("Skill de Sistema", self.is_system_skill))

        parts.append("\n---")
        parts.append(
            "\n## INFORMAÇÕES TÉCNICAS\n"
            "> Metadados de configuração e controle operacional deste Skill.\n"
        )
        parts.append("\n".join(tech))

        sec("HISTÓRICO DE VERSÕES", self.version_history)

        if self.tags:
            parts.append(f"\n**Tags:** {self.tags}")

        parts.append("\n---")
        parts.append(
            f"\n*GF Skill · {self.internal_name or self.name} · v{self.version or '1.0.0'}*"
        )

        return "\n".join(parts)
