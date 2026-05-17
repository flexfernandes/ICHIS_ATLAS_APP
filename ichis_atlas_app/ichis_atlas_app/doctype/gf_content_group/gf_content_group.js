// ── Ícones disponíveis (Lucide Icons — https://lucide.dev)
const GCG_ICONS = [
    'activity','alarm-clock','alert-circle','alert-octagon','alert-triangle',
    'align-center','align-justify','align-left','align-right','anchor',
    'aperture','archive','arrow-down','arrow-left','arrow-right','arrow-up',
    'at-sign','award','banknote','bar-chart','bar-chart-2',
    'battery','bell','bell-off','bold','book','book-open','bookmark',
    'box','brain','briefcase','bug','building','building-2','bus',
    'calculator','calendar','calendar-check','calendar-days','calendar-minus',
    'calendar-plus','calendar-x','camera','camera-off','car','cast',
    'check','check-circle','check-square','chevron-down','chevron-right',
    'clipboard','clipboard-check','clipboard-list','clock','cloud',
    'cloud-off','cloud-rain','cloud-snow','code','code-2','cog','coffee',
    'columns','command','compass','construction','copy','cpu','credit-card',
    'cross','crosshair','database','disc','divide','dollar-sign',
    'download','droplets','edit','edit-2','edit-3','external-link',
    'eye','eye-off','factory','feather','file','file-check','file-minus',
    'file-plus','file-text','file-x','film','filter','fingerprint',
    'flag','flame','flask-conical','folder','folder-open','folder-plus',
    'frown','gauge','gift','git-branch','git-commit','git-merge',
    'git-pull-request','globe','graduation-cap','grid','hammer','handshake',
    'hard-drive','hard-hat','hash','headphones','heart','heart-pulse',
    'hexagon','home','hotel','hourglass','image','inbox','info',
    'italic','key','keyboard','laptop','landmark','layers',
    'layout','layout-dashboard','leaf','library','life-buoy','line-chart',
    'link','link-2','loader','lock','lock-open','log-in','log-out',
    'mail','mail-open','map','map-pin','maximize','maximize-2',
    'meh','menu','message-circle','message-square','mic','mic-off',
    'microscope','minimize','minimize-2','minus','minus-circle','monitor',
    'moon','more-horizontal','more-vertical','move','music','navigation',
    'network','newspaper','octagon','package','paperclip','parking',
    'pause','pause-circle','pen-line','pen-tool','percent','phone',
    'phone-call','phone-off','pie-chart','pill','plane','play',
    'play-circle','plug','plus','plus-circle','plus-square','power',
    'printer','receipt','refresh-cw','repeat','rocket','rotate-ccw',
    'rotate-cw','route','ruler','save','scatter-chart','scissors',
    'scroll','search','send','server','settings','settings-2',
    'share','share-2','shield','shield-alert','shield-check','shield-off',
    'ship','shopping-bag','shopping-cart','shuffle','sidebar','skip-back',
    'skip-forward','slash','sliders','smartphone','smile','sort-asc',
    'sort-desc','sparkles','speaker','square','stamp','star','stethoscope',
    'stop-circle','sun','sunrise','sunset','syringe','table','tablet',
    'tag','target','terminal','thermometer','thumbs-down','thumbs-up',
    'timer','toggle-left','toggle-right','tool','train','trash','trash-2',
    'trending-down','trending-up','triangle','truck','tv','type',
    'umbrella','underline','unlock','upload','user','user-check',
    'user-minus','user-plus','user-x','users','video','video-off',
    'voicemail','volume','volume-1','volume-2','volume-x','wallet',
    'watch','wifi','wifi-off','wind','wrench','x','x-circle','x-square',
    'zap','zoom-in','zoom-out'
];

const GCG_ICONS_UNIQUE = [...new Set(GCG_ICONS)].sort();

// ── Carrega Lucide (asset local do app)
function gcg_load_lucide(cb) {
    if (window.lucide) { cb(); return; }
    const s = document.createElement('script');
    s.src = '/assets/ichis_atlas_app/js/lucide.min.js';
    s.onload = cb;
    document.head.appendChild(s);
}

// ── Abre o icon picker
function gcg_open_icon_picker(frm) {
    gcg_load_lucide(() => {
        const d = new frappe.ui.Dialog({
            title: 'Escolher Ícone',
            fields: [
                {
                    fieldtype: 'Data',
                    fieldname: 'search',
                    label: 'Buscar ícone',
                    placeholder: 'Ex: folder, chart, user...'
                },
                { fieldtype: 'HTML', fieldname: 'icon_grid' }
            ]
        });

        const CSS = `
            .gf-ip-grid{display:flex;flex-wrap:wrap;gap:6px;padding:8px 0;max-height:380px;overflow-y:auto}
            .gf-ip-item{display:flex;flex-direction:column;align-items:center;justify-content:center;
                width:68px;height:64px;border-radius:8px;cursor:pointer;border:1.5px solid #e2e8f0;
                padding:6px 4px 4px;gap:4px;transition:border-color 120ms,background 120ms;
                font-size:9.5px;color:#475569;text-align:center;word-break:break-all;line-height:1.2}
            .gf-ip-item:hover{border-color:#166534;background:#f0fdf4;color:#166534}
            .gf-ip-item.selected{border-color:#166534;background:#dcfce7;color:#166534;font-weight:600}
            .gf-ip-empty{color:#94a3b8;font-size:13px;padding:30px 0;text-align:center;width:100%}
        `;
        if (!document.getElementById('gf-ip-style')) {
            const st = document.createElement('style');
            st.id = 'gf-ip-style';
            st.textContent = CSS;
            document.head.appendChild(st);
        }

        function render(q) {
            const list = q
                ? GCG_ICONS_UNIQUE.filter(n => n.includes(q.toLowerCase().trim()))
                : GCG_ICONS_UNIQUE;
            const cur = frm.doc.icon || '';
            const html = list.length
                ? list.map(n =>
                    `<div class="gf-ip-item${n===cur?' selected':''}" data-icon="${n}">
                        <i data-lucide="${n}" style="width:20px;height:20px;flex-shrink:0"></i>
                        <span>${n}</span>
                     </div>`
                  ).join('')
                : '<div class="gf-ip-empty">Nenhum ícone encontrado</div>';
            const $grid = d.fields_dict.icon_grid.$wrapper;
            $grid.html(`<div class="gf-ip-grid">${html}</div>`);
            lucide.createIcons({ attrs: { style: 'display:block' } });

            $grid.find('.gf-ip-item').on('click', function() {
                const name = $(this).data('icon');
                frm.set_value('icon', name);
                $grid.find('.gf-ip-item').removeClass('selected');
                $(this).addClass('selected');
                d.hide();
                gcg_refresh_icon_preview(frm);
            });
        }

        d.fields_dict.search.$input.on('input', function() {
            render($(this).val());
        });

        d.show();
        setTimeout(() => render(''), 100);
    });
}

// ── Preview do ícone no campo
function gcg_refresh_icon_preview(frm) {
    gcg_load_lucide(() => {
        const icon = frm.doc.icon;
        const $wrap = frm.fields_dict.icon.$wrapper;
        $wrap.find('.gcg-icon-preview').remove();
        if (icon) {
            $wrap.find('.control-label').after(
                `<span class="gcg-icon-preview" style="
                    display:inline-flex;align-items:center;gap:5px;
                    font-size:11px;color:#166534;margin-bottom:4px">
                    <i data-lucide="${icon}" style="width:14px;height:14px"></i>
                    <b>${icon}</b>
                </span>`
            );
            lucide.createIcons({ attrs: { style: 'display:block' } });
        }
    });
}

// ── Atualiza descrição do campo parent_group com o nome de exibição
function gcg_refresh_parent_label(frm) {
    if (frm.doc.parent_group) {
        frappe.db.get_value('GF Content Group', frm.doc.parent_group, 'display_name', (r) => {
            const label = (r && r.display_name) ? '📁 ' + r.display_name : frm.doc.parent_group;
            frm.set_df_property('parent_group', 'description', label);
        });
    } else {
        frm.set_df_property('parent_group', 'description', '');
    }
}

frappe.ui.form.on('GF Content Group', {

    refresh(frm) {
        // ── Botão Escolher Ícone
        frm.fields_dict.icon.$wrapper
            .find('.control-input-wrapper')
            .after(
                `<button class="btn btn-xs btn-default" style="margin-top:4px"
                    onclick="gcg_open_icon_picker(cur_frm)">
                    <svg xmlns="http://www.w3.org/2000/svg" width="11" height="11"
                         viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                         style="margin-right:3px;vertical-align:-1px">
                         <circle cx="12" cy="12" r="10"/>
                         <circle cx="12" cy="10" r="3"/>
                         <path d="M7 20.662V19a2 2 0 0 1 2-2h6a2 2 0 0 1 2 2v1.662"/>
                    </svg>
                    Escolher Ícone
                </button>`
            );
        gcg_refresh_icon_preview(frm);

        // ── Mostra nome do grupo pai ao abrir o form
        gcg_refresh_parent_label(frm);
    },

    icon(frm) {
        gcg_refresh_icon_preview(frm);
    },

    parent_group(frm) {
        gcg_refresh_parent_label(frm);
    }
});
