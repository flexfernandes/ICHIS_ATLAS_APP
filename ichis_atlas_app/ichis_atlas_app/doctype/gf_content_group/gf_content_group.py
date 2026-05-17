import frappe
from frappe.utils.nestedset import NestedSet


class GFContentGroup(NestedSet):
    nsm_parent_field = "parent_group"

    def validate(self):
        if self.internal_name:
            self.internal_name = self.internal_name.strip().lower().replace(" ", "_")
