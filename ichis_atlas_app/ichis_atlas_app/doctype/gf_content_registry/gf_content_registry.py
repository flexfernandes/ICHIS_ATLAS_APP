import re
import unicodedata
import frappe
from frappe.model.document import Document


class GFContentRegistry(Document):

    def before_insert(self):
        if not self.internal_name and self.title:
            self.internal_name = self._generate_internal_name(self.title)
        if not self.version:
            self.version = "1.0.0"

    def validate(self):
        if self.content_group and not self.access_group:
            default_ag = frappe.db.get_value("GF Content Group", self.content_group, "default_access_group")
            if default_ag:
                self.access_group = default_ag

    def _generate_internal_name(self, title):
        name = unicodedata.normalize("NFD", title.lower())
        name = "".join(c for c in name if unicodedata.category(c) != "Mn")
        name = re.sub(r"[^a-z0-9]+", "_", name)
        name = name.strip("_")
        return name[:64] if len(name) > 64 else name
