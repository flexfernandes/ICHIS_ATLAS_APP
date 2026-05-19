// ── Ícones disponíveis (Lucide Icons — https://lucide.dev)
const GF_ICONS = [
    // Ações e Navegação
    'activity','arrow-right','arrow-left','arrow-up','arrow-down',
    'check','check-circle','check-square','chevron-right','chevron-down',
    'copy','download','edit','edit-2','edit-3','external-link',
    'eye','eye-off','filter','link','link-2','log-in','log-out',
    'maximize','minimize','minus','more-horizontal','more-vertical',
    'move','pen-line','pen-tool','plus','plus-circle','refresh-cw',
    'repeat','rotate-ccw','save','search','send','settings','settings-2',
    'share','share-2','slash','sort-asc','sort-desc','trash','trash-2',
    'upload','x','x-circle','zoom-in','zoom-out',
    // Arquivos e Documentos
    'archive','book','book-open','bookmark','clipboard','clipboard-check',
    'clipboard-list','file','file-check','file-minus','file-plus','file-text',
    'file-x','folder','folder-open','folder-plus','inbox','layers',
    'layout','library','newspaper','package','paperclip','receipt',
    'scroll','stamp','table','tag',
    // Comunicação
    'at-sign','bell','bell-off','mail','mail-open','message-circle',
    'message-square','mic','mic-off','phone','phone-call','phone-off',
    'rss','send','voicemail',
    // Pessoas e Usuários
    'baby','briefcase','graduation-cap','handshake','heart','heart-pulse',
    'smiley','user','user-check','user-minus','user-plus','user-x','users',
    // Negócios e Finanças
    'banknote','bar-chart','bar-chart-2','building','building-2',
    'calculator','credit-card','dollar-sign','landmark','line-chart',
    'percent','pie-chart','receipt','trending-down','trending-up','wallet',
    // Tecnologia
    'airplay','cast','cloud','cloud-off','code','code-2','command',
    'cpu','database','globe','hard-drive','hash','keyboard','laptop',
    'layout-dashboard','monitor','radio','server','smartphone','tablet',
    'terminal','tv','wifi','wifi-off','zap',
    // Indústria e Engenharia
    'alert-circle','alert-octagon','alert-triangle','anchor','award',
    'box','clipboard-list','cog','construction','cpu','factory',
    'flame','flask-conical','gauge','hammer','hard-hat','layers',
    'microscope','package','plug','ruler','settings','settings-2',
    'shield','shield-check','shield-off','tool','truck','wrench','zap',
    // Saúde
    'activity','alert-circle','cross','droplets','heart','heart-pulse',
    'pill','syringe','thermometer','stethoscope',
    // Natureza e Ambiente
    'cloud','cloud-rain','cloud-snow','droplets','leaf','moon',
    'sun','sunrise','sunset','umbrella','wind',
    // Interface e Layout
    'align-center','align-justify','align-left','align-right',
    'aperture','bold','circle','columns','crop','feather',
    'grid','image','italic','maximize-2','minimize-2','move',
    'octagon','pentagon','sidebar','sliders','square','triangle',
    'type','underline',
    // Localização e Transporte
    'anchor','bed','bus','car','compass','flag','globe',
    'home','hotel','map','map-pin','navigation','parking',
    'plane','rocket','route','ship','train',
    // Tempo e Calendário
    'alarm-clock','calendar','calendar-check','calendar-days',
    'calendar-minus','calendar-plus','calendar-x','clock','hourglass',
    'timer','watch',
    // Segurança
    'eye','eye-off','fingerprint','key','lock','lock-open',
    'shield','shield-alert','shield-check','unlock',
    // Mídia
    'camera','camera-off','film','headphones','image','mic',
    'music','pause','pause-circle','play','play-circle','radio',
    'stop-circle','tv','video','video-off','volume','volume-1',
    'volume-2','volume-x',
    // Dados e IA
    'bar-chart','bar-chart-2','brain','cpu','database','git-branch',
    'git-commit','git-merge','git-pull-request','layers','line-chart',
    'network','pie-chart','scatter-chart','server','share-2','sparkles',
    // Outros Comuns
    'anchor','at-sign','award','battery','bluetooth','bold','bug',
    'cast','circle','clipboard','code','coffee','command','compass',
    'crosshair','disc','divide','dollar-sign','flag','flashlight',
    'frown','gift','grid','hash','headphones','hexagon','info',
    'italic','life-buoy','loader','log-in','log-out','meh',
    'menu','minus-circle','octagon','package','paperclip','pause',
    'percent','phone','plus-square','power','printer','rotate-cw',
    'rss','scissors','shopping-bag','shopping-cart','shuffle','sidebar',
    'skip-back','skip-forward','sliders','smile','speaker','square',
    'star','sun','sunrise','sunset','target','terminal','thumbs-down',
    'thumbs-up','toggle-left','toggle-right','tool','triangle',
    'type','umbrella','underline','unlock','user-check','video',
    'voicemail','watch','wifi','wind','x-square'
];

// Remove duplicatas e ordena
const GF_ICONS_UNIQUE = [...new Set(GF_ICONS)].sort();

// ── Carrega Lucide CDN se necessário
function gf_load_lucide(cb) {
    if (window.lucide) { cb(); return; }
    const s = document.createElement('script');
    s.src = 'https://cdn.jsdelivr.net/npm/lucide@0.263.1/dist/umd/lucide.min.js';
    s.onload = cb;
    document.head.appendChild(s);
}

// ── Abre o icon picker
function gf_open_icon_picker(frm) {
    gf_load_lucide(() => {
        const d = new frappe.ui.Dialog({
            title: 'Escolher Ícone',
            fields: [
                {
                    fieldtype: 'Data',
                    fieldname: 'search',
                    label: 'Buscar ícone',
                    placeholder: 'Ex: chart, user, file...'
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
                ? GF_ICONS_UNIQUE.filter(n => n.includes(q.toLowerCase().trim()))
                : GF_ICONS_UNIQUE;
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
                // Usa set_value mesmo com read_only para permitir seleção via picker
                frm.doc.icon = name;
                frm.refresh_field('icon');
                frm.dirty();
                $grid.find('.gf-ip-item').removeClass('selected');
                $(this).addClass('selected');
                d.hide();
                gf_refresh_icon_preview(frm);
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
function gf_refresh_icon_preview(frm) {
    gf_load_lucide(() => {
        const icon = frm.doc.icon;
        const $wrap = frm.fields_dict.icon.$wrapper;
        $wrap.find('.gf-icon-preview').remove();
        if (icon) {
            $wrap.find('.control-label').after(
                `<span class="gf-icon-preview" style="
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

// ── Testa a URL do campo route_url
function gf_test_url(frm) {
    const url = frm.doc.route_url;
    if (!url) {
        frappe.msgprint({ title: 'URL vazia', message: 'Preencha o campo URL / Rota antes de testar.', indicator: 'orange' });
        return;
    }
    const full = /^https?:\/\//.test(url) ? url : window.location.origin + url;
    window.open(full, '_blank');
}

frappe.ui.form.on('GF Content Registry', {

    refresh(frm) {
        // ── Botão Escolher Ícone
        frm.fields_dict.icon.$wrapper
            .find('.control-input-wrapper')
            .after(
                `<button class="btn btn-xs btn-default" style="margin-top:4px"
                    onclick="gf_open_icon_picker(cur_frm)">
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
        gf_refresh_icon_preview(frm);

        // ── Botão Testar URL
        frm.fields_dict.route_url.$wrapper
            .find('.control-input-wrapper')
            .after(
                `<button class="btn btn-xs btn-default" style="margin-top:4px"
                    onclick="gf_test_url(cur_frm)">
                    <svg xmlns="http://www.w3.org/2000/svg" width="11" height="11"
                         viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                         style="margin-right:3px;vertical-align:-1px">
                         <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>
                         <polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/>
                    </svg>
                    Testar URL
                </button>`
            );
    },

    title(frm) {
        // Auto-preenche internal_name apenas em documentos novos (antes de salvar)
        if (frm.doc.__islocal) {
            const slug = (frm.doc.title || '')
                .toLowerCase()
                .normalize('NFD').replace(/[̀-ͯ]/g, '')
                .replace(/[^a-z0-9]+/g, '_')
                .replace(/^_+|_+$/g, '');
            frm.set_value('internal_name', slug);
        }
    },

    icon(frm) {
        gf_refresh_icon_preview(frm);
    },

    content_group(frm) {
        if (frm.doc.content_group) {
            frappe.db.get_value('GF Content Group', frm.doc.content_group, 'default_access_group', (r) => {
                if (r && r.default_access_group && !frm.doc.access_group) {
                    frm.set_value('access_group', r.default_access_group);
                }
            });
        }
    }
});
