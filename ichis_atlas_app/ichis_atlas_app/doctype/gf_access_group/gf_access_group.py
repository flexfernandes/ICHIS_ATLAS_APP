import frappe
from frappe.model.document import Document


class GFAccessGroup(Document):
    def validate(self):
        if self.internal_name:
            self.internal_name = self.internal_name.strip().lower().replace(" ", "_")
