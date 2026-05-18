frappe.ui.form.on('GF Skill', {

    refresh(frm) {
        // Default owner for new docs
        if (frm.doc.__islocal && !frm.doc.skill_owner) {
            frm.set_value('skill_owner', frappe.session.user);
        }

        // Copy Prompt button
        if (frm.doc.full_prompt) {
            frm.add_custom_button('Copiar Prompt', () => {
                frappe.utils.copy_to_clipboard(frm.doc.full_prompt);
                frappe.show_alert({ message: 'Prompt copiado!', indicator: 'green' });
            }, 'Ações');
        }

        // Open dashboard button
        frm.add_custom_button('Abrir Dashboard', () => {
            window.open('/gf-skill', '_blank');
        }, 'Ações');

        // Status badge in header
        if (frm.doc.status) {
            const colors = {
                'Draft': 'gray', 'Em Desenvolvimento': 'blue', 'Em Teste': 'orange',
                'Ativo': 'green', 'Obsoleto': 'yellow', 'Arquivado': 'red'
            };
            frm.set_indicator_formatter('status', d => colors[d.status] || 'gray');
        }
    },

    skill_name(frm) {
        // Auto-fill internal_name if empty or new doc
        if (frm.doc.__islocal || !frm.doc.internal_name) {
            const slug = (frm.doc.skill_name || '')
                .toLowerCase()
                .normalize('NFD').replace(/[̀-ͯ]/g, '')
                .replace(/[^a-z0-9]+/g, '_')
                .replace(/^_+|_+$/g, '');
            frm.set_value('internal_name', slug);
        }
    },

    before_save(frm) {
        frappe.show_alert({ message: 'Gerando Full Prompt...', indicator: 'blue' });
    }
});
