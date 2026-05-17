import frappe
from frappe.model.document import Document


class GFContentRegistry(Document):
    def validate(self):
        if self.content_group and not self.access_group:
            default_ag = frappe.db.get_value("GF Content Group", self.content_group, "default_access_group")
            if default_ag:
                self.access_group = default_ag
