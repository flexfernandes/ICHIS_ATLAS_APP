frappe.ui.form.on("GF Content Registry", {
    content_group(frm) {
        if (frm.doc.content_group) {
            frappe.db.get_value("GF Content Group", frm.doc.content_group, "default_access_group", (r) => {
                if (r && r.default_access_group && !frm.doc.access_group) {
                    frm.set_value("access_group", r.default_access_group);
                }
            });
        }
    }
});
