import frappe
from frappe.model.document import Document


class GFSkill(Document):

    def before_save(self):
        self.full_prompt = self._build_prompt()

    def before_submit(self):
        self.full_prompt = self._build_prompt()

    # ──────────────────────────────────────────────
    def _build_prompt(self):
        parts = []

        def sec(title, content):
            if content and str(content).strip():
                parts.append(f"\n## {title}\n{str(content).strip()}")

        def flag(label, value):
            return f"- {label}: {'Sim' if value else 'Não'}"

        # Header
        parts.append(
            f"# {self.skill_name or '—'} — v{self.version or '1.0.0'}"
        )

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

        # Propósito
        sec("PROPÓSITO", self.purpose)

        if self.when_to_use or self.when_not_to_use:
            parts.append("\n---")
            sec("QUANDO USAR", self.when_to_use)
            sec("QUANDO NÃO USAR", self.when_not_to_use)

        parts.append("\n---")

        # Instruções
        sec("INSTRUÇÕES PRINCIPAIS", self.main_instructions)
        sec("REGRAS OBRIGATÓRIAS", self.mandatory_rules)
        sec("AÇÕES PROIBIDAS", self.forbidden_actions)
        sec("CHECKLIST DE VALIDAÇÃO", self.validation_checklist)

        parts.append("\n---")

        # Estilo
        sec("ESTILO DE ESCRITA", self.writing_style)
        sec("ESTILO VISUAL", self.visual_style)
        sec("TOM DE VOZ", self.tone_of_voice)
        sec("REGRAS DE FORMATAÇÃO", self.formatting_rules)

        # Cabeçalho / Rodapé
        if self.header_template or self.footer_template:
            parts.append("\n---")
            sec("CABEÇALHO — TEMPLATE", self.header_template)
            sec("Observações do Cabeçalho", self.header_notes)
            sec("RODAPÉ — TEMPLATE", self.footer_template)
            sec("Observações do Rodapé", self.footer_notes)

        # Exemplo
        if self.full_example:
            parts.append("\n---")
            sec("EXEMPLO COMPLETO", self.full_example)
            sec("Observações do Exemplo", self.example_notes)

        # Técnico
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
        parts.append("\n## INFORMAÇÕES TÉCNICAS")
        parts.append("\n".join(tech))

        sec("HISTÓRICO DE VERSÕES", self.version_history)

        if self.tags:
            parts.append(f"\n**Tags:** {self.tags}")

        parts.append("\n---")
        parts.append(
            f"\n*GF Skill · {self.internal_name or self.name} · v{self.version or '1.0.0'}*"
        )

        return "\n".join(parts)
