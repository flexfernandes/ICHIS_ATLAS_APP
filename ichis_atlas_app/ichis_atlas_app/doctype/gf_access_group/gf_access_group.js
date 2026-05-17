frappe.ui.form.on("GF Access Group", {
    refresh(frm) {
        frm.set_df_property("users", "cannot_add_rows", frm.doc.system_group && !frappe.user.has_role("GF Manager"));
    }
});
