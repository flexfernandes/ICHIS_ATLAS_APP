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
        // ── Settings workspace (sempre visível)
        gf_st_ensure_styles();
        gf_st_render(frm);

        // ── Natural Studio (somente após criação)
        if (!frm.doc.__islocal) {
            gf_ns_ensure_styles();
            gf_ns_render(frm);
        }
    },

    title(frm) {
        if (frm.doc.__islocal) {
            const ver  = (frm.doc.version || '1.0.0').replace(/\./g, '_');
            const slug = (frm.doc.title || '')
                .toLowerCase()
                .normalize('NFD').replace(/[̀-ͯ]/g, '')
                .replace(/[^a-z0-9]+/g, '_')
                .replace(/^_+|_+$/g, '');
            const newName = slug ? `${slug}_v${ver}` : '';
            frm.set_value('internal_name', newName);
            // Atualiza a exibição no Settings workspace sem re-renderizar tudo
            const $stRoot = frm.fields_dict.settings_workspace
                ? frm.fields_dict.settings_workspace.$wrapper.find('#gf-st-root')
                : $();
            $stRoot.find('[data-st-field="internal_name"]').val(newName);
        }
    },

    icon(frm) {
        // Atualiza o preview de ícone no Settings workspace
        const $stRoot = frm.fields_dict.settings_workspace
            ? frm.fields_dict.settings_workspace.$wrapper.find('#gf-st-root')
            : $();
        gf_st_update_icon_preview($stRoot, frm.doc.icon);
    },

    content_group(frm) {
        if (!frm.doc.content_group) {
            frm.doc.route_url = '';
            frm.refresh_field('route_url');
            return;
        }
        frappe.db.get_value(
            'GF Content Group',
            frm.doc.content_group,
            ['default_access_group', 'external_reference'],
            (r) => {
                if (!r) return;
                if (r.default_access_group && !frm.doc.access_group) {
                    frm.set_value('access_group', r.default_access_group);
                }
                if (r.external_reference) {
                    frm.doc.route_url = `🔍 Pasta: ${r.external_reference} (será resolvida ao salvar)`;
                    frm.refresh_field('route_url');
                } else {
                    frm.doc.route_url = '';
                    frm.refresh_field('route_url');
                    frappe.show_alert({
                        message: __('O Grupo de Conteúdo selecionado não possui Referência Externa (Google Drive) configurada.'),
                        indicator: 'orange'
                    }, 6);
                }
            }
        );
    }
});

// ═══════════════════════════════════════════════════════════════════════════
//  NATURAL STUDIO
// ═══════════════════════════════════════════════════════════════════════════

function gf_ns_ensure_styles() {
    if (document.getElementById('gf-ns-styles')) return;
    const css = `
        /* ── Natural Studio reset & vars ── */
        #gf-ns-root *,#gf-ns-root *::before,#gf-ns-root *::after{box-sizing:border-box;margin:0;padding:0}
        #gf-ns-root{
            --ns-bg:        #0d1117;
            --ns-surface:   #161b22;
            --ns-border:    #30363d;
            --ns-border2:   #21262d;
            --ns-text:      #e6edf3;
            --ns-text2:     #8b949e;
            --ns-text3:     #484f58;
            --ns-accent:    #238636;
            --ns-accent-h:  #2ea043;
            --ns-accent-b:  #1f6feb;
            --ns-accent-bh: #388bfd;
            --ns-danger:    #da3633;
            --ns-danger-h:  #f85149;
            --ns-overlay:   rgba(13,17,23,.85);
            --ns-radius:    8px;
            --ns-radius-sm: 5px;
            font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',system-ui,sans-serif;
            font-size: 13px;
            background: var(--ns-bg);
            color: var(--ns-text);
            border-radius: 10px;
            overflow: hidden;
            border: 1px solid var(--ns-border);
            min-height: 520px;
        }

        /* ── Header ── */
        .ns-header{
            display:flex;align-items:center;gap:10px;
            padding:12px 16px;
            background:var(--ns-surface);
            border-bottom:1px solid var(--ns-border);
        }
        .ns-header-logo{
            display:flex;align-items:center;gap:6px;
            font-size:13px;font-weight:600;color:var(--ns-text);letter-spacing:.3px;
        }
        .ns-header-logo svg{flex-shrink:0}
        .ns-badge{
            font-size:9px;font-weight:600;letter-spacing:.8px;text-transform:uppercase;
            padding:2px 7px;border-radius:20px;background:rgba(35,134,54,.18);
            color:#3fb950;border:1px solid rgba(63,185,80,.25);
        }
        .ns-header-meta{
            margin-left:auto;display:flex;align-items:center;gap:8px;
            font-size:11px;color:var(--ns-text2);
        }
        .ns-header-meta span{
            background:var(--ns-bg);border:1px solid var(--ns-border2);
            border-radius:4px;padding:2px 8px;
        }
        .ns-header-meta .ns-version{color:var(--ns-accent-bh)}

        /* ── Main layout ── */
        .ns-body{display:flex;height:460px}

        /* ── Left panel — Prompt ── */
        .ns-panel-prompt{
            flex:0 0 55%;display:flex;flex-direction:column;
            border-right:1px solid var(--ns-border);
        }
        .ns-panel-title{
            padding:10px 14px;font-size:11px;font-weight:600;
            color:var(--ns-text2);letter-spacing:.5px;text-transform:uppercase;
            border-bottom:1px solid var(--ns-border2);
            background:rgba(22,27,34,.6);
            display:flex;align-items:center;gap:6px;
        }
        .ns-panel-title svg{opacity:.7}
        .ns-context-area{
            flex:1;overflow-y:auto;padding:14px;display:flex;flex-direction:column;gap:10px;
        }
        .ns-context-area::-webkit-scrollbar{width:5px}
        .ns-context-area::-webkit-scrollbar-track{background:transparent}
        .ns-context-area::-webkit-scrollbar-thumb{background:var(--ns-border);border-radius:3px}
        .ns-msg{
            display:flex;gap:9px;align-items:flex-start;
            animation:ns-fadein .2s ease;
        }
        @keyframes ns-fadein{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:none}}
        .ns-msg-avatar{
            width:26px;height:26px;border-radius:50%;flex-shrink:0;
            display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;
            margin-top:1px;
        }
        .ns-msg-avatar.user{background:rgba(31,111,235,.25);color:#388bfd;border:1px solid rgba(56,139,253,.3)}
        .ns-msg-avatar.ai{background:rgba(35,134,54,.2);color:#3fb950;border:1px solid rgba(63,185,80,.25)}
        .ns-msg-body{flex:1;min-width:0}
        .ns-msg-role{font-size:10px;font-weight:600;letter-spacing:.4px;color:var(--ns-text2);margin-bottom:3px;text-transform:uppercase}
        .ns-msg-text{
            background:var(--ns-surface);border:1px solid var(--ns-border2);
            border-radius:0 var(--ns-radius) var(--ns-radius) var(--ns-radius);
            padding:9px 12px;font-size:12.5px;line-height:1.6;color:var(--ns-text);
            white-space:pre-wrap;word-break:break-word;
        }
        .ns-msg.user .ns-msg-text{
            background:rgba(31,111,235,.1);border-color:rgba(56,139,253,.2);
            border-radius:var(--ns-radius) 0 var(--ns-radius) var(--ns-radius);
        }
        .ns-msg-empty{
            flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;
            gap:8px;color:var(--ns-text3);font-size:12px;
        }
        .ns-msg-empty svg{opacity:.3}

        /* ── Input area ── */
        .ns-input-area{
            padding:12px 14px;border-top:1px solid var(--ns-border2);
            background:rgba(22,27,34,.5);
        }
        .ns-input-row{display:flex;gap:8px;align-items:flex-end}
        .ns-textarea{
            flex:1;background:var(--ns-bg);border:1px solid var(--ns-border);
            border-radius:var(--ns-radius);color:var(--ns-text);font-size:12.5px;
            line-height:1.5;padding:9px 12px;resize:none;outline:none;
            font-family:inherit;min-height:40px;max-height:120px;overflow-y:auto;
            transition:border-color .15s;
        }
        .ns-textarea:focus{border-color:var(--ns-accent-b)}
        .ns-textarea::placeholder{color:var(--ns-text3)}
        .ns-btn{
            display:inline-flex;align-items:center;gap:5px;
            padding:8px 14px;border-radius:var(--ns-radius-sm);
            font-size:12px;font-weight:500;cursor:pointer;
            border:1px solid transparent;transition:all .15s;white-space:nowrap;
        }
        .ns-btn:disabled{opacity:.45;cursor:not-allowed}
        .ns-btn-primary{background:var(--ns-accent);color:#fff;border-color:var(--ns-accent)}
        .ns-btn-primary:hover:not(:disabled){background:var(--ns-accent-h)}
        .ns-btn-secondary{background:transparent;color:var(--ns-text2);border-color:var(--ns-border)}
        .ns-btn-secondary:hover:not(:disabled){background:rgba(255,255,255,.05);color:var(--ns-text);border-color:var(--ns-border2)}
        .ns-btn-danger{background:transparent;color:var(--ns-danger);border-color:rgba(218,54,51,.3)}
        .ns-btn-danger:hover:not(:disabled){background:rgba(218,54,51,.12);color:var(--ns-danger-h)}
        .ns-btn-icon{padding:7px;border-radius:var(--ns-radius-sm);background:transparent;color:var(--ns-text2);border:1px solid var(--ns-border);cursor:pointer;transition:all .15s;display:inline-flex;align-items:center}
        .ns-btn-icon:hover{background:rgba(255,255,255,.06);color:var(--ns-text);border-color:var(--ns-border2)}
        .ns-context-actions{display:flex;gap:6px;margin-top:8px;justify-content:flex-end}

        /* ── Right panel — Images ── */
        .ns-panel-images{
            flex:1;display:flex;flex-direction:column;overflow:hidden;
        }
        .ns-images-toolbar{
            padding:8px 12px;border-bottom:1px solid var(--ns-border2);
            display:flex;align-items:center;gap:8px;
            background:rgba(22,27,34,.6);
        }
        .ns-images-toolbar .ns-folder-path{
            flex:1;font-size:10.5px;color:var(--ns-text2);
            white-space:nowrap;overflow:hidden;text-overflow:ellipsis;
        }
        .ns-images-toolbar .ns-folder-path b{color:var(--ns-accent-bh)}
        .ns-drop-zone{
            flex:1;overflow-y:auto;padding:12px;
            display:grid;grid-template-columns:repeat(auto-fill,minmax(100px,1fr));
            gap:10px;align-content:start;
            transition:background .2s;
        }
        .ns-drop-zone::-webkit-scrollbar{width:5px}
        .ns-drop-zone::-webkit-scrollbar-track{background:transparent}
        .ns-drop-zone::-webkit-scrollbar-thumb{background:var(--ns-border);border-radius:3px}
        .ns-drop-zone.drag-over{
            background:rgba(31,111,235,.07);
            outline:2px dashed rgba(56,139,253,.4);
            outline-offset:-4px;
        }
        .ns-img-card{
            position:relative;border-radius:var(--ns-radius-sm);overflow:hidden;
            background:var(--ns-surface);border:1px solid var(--ns-border2);
            cursor:pointer;aspect-ratio:1;
            transition:border-color .15s,transform .1s;
        }
        .ns-img-card:hover{border-color:var(--ns-border);transform:scale(1.02)}
        .ns-img-card img{width:100%;height:100%;object-fit:cover;display:block}
        .ns-img-card-overlay{
            position:absolute;inset:0;background:var(--ns-overlay);
            display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px;
            opacity:0;transition:opacity .15s;padding:6px;
        }
        .ns-img-card:hover .ns-img-card-overlay{opacity:1}
        .ns-img-name{
            font-size:9px;color:var(--ns-text);text-align:center;
            word-break:break-all;line-height:1.3;max-width:100%;
        }
        .ns-img-del{
            background:rgba(218,54,51,.8);border:none;border-radius:4px;
            color:#fff;padding:4px 8px;font-size:10px;cursor:pointer;
            display:flex;align-items:center;gap:3px;transition:background .15s;
        }
        .ns-img-del:hover{background:var(--ns-danger-h)}
        .ns-drop-hint{
            grid-column:1/-1;
            display:flex;flex-direction:column;align-items:center;justify-content:center;
            gap:10px;padding:40px 20px;color:var(--ns-text3);font-size:12px;text-align:center;
            border:2px dashed var(--ns-border2);border-radius:var(--ns-radius);
            cursor:pointer;transition:border-color .15s,color .15s;min-height:140px;
        }
        .ns-drop-hint:hover{border-color:var(--ns-accent-b);color:var(--ns-text2)}
        .ns-drop-hint svg{opacity:.4}
        .ns-upload-bar{
            padding:8px 12px;border-top:1px solid var(--ns-border2);
            background:rgba(22,27,34,.5);display:flex;align-items:center;gap:8px;
        }
        .ns-upload-count{font-size:11px;color:var(--ns-text2);margin-left:auto}
        .ns-progress-wrap{height:3px;background:var(--ns-border2);border-radius:2px;overflow:hidden;flex:1}
        .ns-progress-bar{height:100%;background:var(--ns-accent-b);border-radius:2px;transition:width .3s;width:0}

        /* ── Lightbox ── */
        .ns-lightbox{
            position:fixed;inset:0;z-index:9999;background:rgba(0,0,0,.88);
            display:flex;align-items:center;justify-content:center;
            opacity:0;pointer-events:none;transition:opacity .2s;
        }
        .ns-lightbox.open{opacity:1;pointer-events:all}
        .ns-lightbox img{
            max-width:90vw;max-height:88vh;border-radius:8px;
            box-shadow:0 20px 60px rgba(0,0,0,.7);
        }
        .ns-lightbox-close{
            position:fixed;top:16px;right:16px;background:rgba(255,255,255,.1);
            border:none;border-radius:50%;width:36px;height:36px;cursor:pointer;
            color:#fff;font-size:20px;display:flex;align-items:center;justify-content:center;
            transition:background .15s;
        }
        .ns-lightbox-close:hover{background:rgba(255,255,255,.2)}

        /* ── Spinner ── */
        .ns-spinner{
            display:inline-block;width:16px;height:16px;
            border:2px solid rgba(255,255,255,.15);
            border-top-color:var(--ns-accent-bh);
            border-radius:50%;animation:ns-spin .7s linear infinite;
        }
        @keyframes ns-spin{to{transform:rotate(360deg)}}

        /* ── Status dot ── */
        .ns-dot{
            display:inline-block;width:7px;height:7px;border-radius:50%;flex-shrink:0;
        }
        .ns-dot.green{background:#3fb950;box-shadow:0 0 6px rgba(63,185,80,.5)}
        .ns-dot.blue{background:#388bfd;box-shadow:0 0 6px rgba(56,139,253,.4)}
        .ns-dot.orange{background:#d29922}
    `;
    const st = document.createElement('style');
    st.id = 'gf-ns-styles';
    st.textContent = css;
    document.head.appendChild(st);
}

// ── Estado global da sessão NS (por nome de documento) ──
const _gfNsState = {};

function gf_ns_state(frm) {
    const k = frm.doc.name;
    if (!_gfNsState[k]) {
        _gfNsState[k] = { messages: [], folderId: null, folderPath: null, images: [], loading: false };
    }
    return _gfNsState[k];
}

function gf_ns_render(frm) {
    const $root = frm.fields_dict.ns_workspace.$wrapper.find('#gf-ns-root');
    if (!$root.length) return;

    const st = gf_ns_state(frm);

    $root.html(`
        <div class="ns-header">
            <div class="ns-header-logo">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#3fb950" stroke-width="1.8">
                    <path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/>
                </svg>
                Natural Studio
                <span class="ns-badge">BETA</span>
            </div>
            <div class="ns-header-meta">
                <span>${frm.doc.title || frm.doc.name}</span>
                <span class="ns-version">v${frm.doc.version || '1.0.0'}</span>
                <span style="color:var(--ns-text2)">${frm.doc.internal_name || ''}</span>
            </div>
        </div>
        <div class="ns-body">
            <div class="ns-panel-prompt">
                <div class="ns-panel-title">
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
                    </svg>
                    Prompt &amp; Contexto
                </div>
                <div class="ns-context-area" id="gf-ns-msgs"></div>
                <div class="ns-input-area">
                    <div class="ns-input-row">
                        <textarea class="ns-textarea" id="gf-ns-input" rows="2"
                            placeholder="Descreva o que deseja gerar, analisar ou revisar…"></textarea>
                        <button class="ns-btn ns-btn-primary" id="gf-ns-send">
                            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/>
                            </svg>
                            Enviar
                        </button>
                    </div>
                    <div class="ns-context-actions">
                        <button class="ns-btn ns-btn-secondary" id="gf-ns-clear" title="Limpar conversa">
                            <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <polyline points="1 4 1 10 7 10"/><path d="M3.51 15a9 9 0 1 0 .49-3.51"/>
                            </svg>
                            Limpar
                        </button>
                        <button class="ns-btn ns-btn-secondary" id="gf-ns-ctx-doc" title="Incluir dados do registro como contexto">
                            <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                                <polyline points="14 2 14 8 20 8"/>
                            </svg>
                            + Contexto do Registro
                        </button>
                    </div>
                </div>
            </div>
            <div class="ns-panel-images">
                <div class="ns-panel-title">
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/>
                        <polyline points="21 15 16 10 5 21"/>
                    </svg>
                    Imagens
                    <span id="gf-ns-img-count" style="margin-left:auto;font-size:10px;background:var(--ns-border2);padding:1px 7px;border-radius:10px;font-weight:normal"></span>
                </div>
                <div class="ns-images-toolbar">
                    <div class="ns-folder-path" id="gf-ns-folder-path">
                        <span class="ns-spinner" style="width:11px;height:11px;border-width:1.5px"></span>
                        Carregando…
                    </div>
                    <button class="ns-btn-icon" id="gf-ns-refresh" title="Atualizar listagem">
                        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <polyline points="1 4 1 10 7 10"/><path d="M3.51 15a9 9 0 1 0 .49-3.51"/>
                        </svg>
                    </button>
                </div>
                <div class="ns-drop-zone" id="gf-ns-drop">
                    <div style="grid-column:1/-1;display:flex;align-items:center;justify-content:center;min-height:140px">
                        <span class="ns-spinner"></span>
                    </div>
                </div>
                <div class="ns-upload-bar">
                    <button class="ns-btn ns-btn-secondary" id="gf-ns-upload-btn" style="font-size:11px">
                        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <polyline points="16 16 12 12 8 16"/><line x1="12" y1="12" x2="12" y2="21"/>
                            <path d="M20.39 18.39A5 5 0 0 0 18 9h-1.26A8 8 0 1 0 3 16.3"/>
                        </svg>
                        Upload
                    </button>
                    <input type="file" id="gf-ns-file-input" accept="image/*" multiple style="display:none">
                    <div class="ns-progress-wrap" id="gf-ns-progress-wrap" style="display:none">
                        <div class="ns-progress-bar" id="gf-ns-progress-bar"></div>
                    </div>
                    <span class="ns-upload-count" id="gf-ns-upload-status"></span>
                </div>
            </div>
        </div>
        <div class="ns-lightbox" id="gf-ns-lightbox">
            <button class="ns-lightbox-close" id="gf-ns-lb-close">✕</button>
            <img src="" alt="" id="gf-ns-lb-img">
        </div>
    `);

    gf_ns_bind(frm);
    gf_ns_load_workspace(frm);
}

function gf_ns_bind(frm) {
    const $root = frm.fields_dict.ns_workspace.$wrapper.find('#gf-ns-root');

    // ── Send message ──
    $root.find('#gf-ns-send').on('click', () => gf_ns_send(frm));
    $root.find('#gf-ns-input').on('keydown', (e) => {
        if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) gf_ns_send(frm);
    });
    // auto-resize textarea
    $root.find('#gf-ns-input').on('input', function() {
        this.style.height = 'auto';
        this.style.height = Math.min(this.scrollHeight, 120) + 'px';
    });

    // ── Clear conversation ──
    $root.find('#gf-ns-clear').on('click', () => {
        gf_ns_state(frm).messages = [];
        gf_ns_render_messages(frm);
    });

    // ── Add doc context ──
    $root.find('#gf-ns-ctx-doc').on('click', () => gf_ns_add_doc_context(frm));

    // ── Refresh images ──
    $root.find('#gf-ns-refresh').on('click', () => gf_ns_load_workspace(frm));

    // ── Upload button ──
    $root.find('#gf-ns-upload-btn').on('click', () => $root.find('#gf-ns-file-input').trigger('click'));
    $root.find('#gf-ns-file-input').on('change', function() {
        if (this.files && this.files.length) gf_ns_upload_files(frm, Array.from(this.files));
        this.value = '';
    });

    // ── Drag & drop ──
    const $drop = $root.find('#gf-ns-drop');
    $drop.on('dragenter dragover', (e) => { e.preventDefault(); $drop.addClass('drag-over'); });
    $drop.on('dragleave', (e) => { if (!$drop[0].contains(e.relatedTarget)) $drop.removeClass('drag-over'); });
    $drop.on('drop', (e) => {
        e.preventDefault();
        $drop.removeClass('drag-over');
        const files = Array.from(e.originalEvent.dataTransfer.files).filter(f => f.type.startsWith('image/'));
        if (files.length) gf_ns_upload_files(frm, files);
    });

    // ── Lightbox close ──
    $root.find('#gf-ns-lb-close, #gf-ns-lightbox').on('click', function(e) {
        if (e.target === this) $root.find('#gf-ns-lightbox').removeClass('open');
    });
    $(document).on('keydown.gf-ns', (e) => {
        if (e.key === 'Escape') $root.find('#gf-ns-lightbox').removeClass('open');
    });
}

function gf_ns_load_workspace(frm) {
    const $root = frm.fields_dict.ns_workspace.$wrapper.find('#gf-ns-root');
    const $drop = $root.find('#gf-ns-drop');
    const $path = $root.find('#gf-ns-folder-path');

    $path.html('<span class="ns-spinner" style="width:11px;height:11px;border-width:1.5px"></span> Carregando…');
    $drop.html('<div style="grid-column:1/-1;display:flex;align-items:center;justify-content:center;min-height:140px"><span class="ns-spinner"></span></div>');

    frappe.call({
        method: 'ichis_atlas_app.ichis_atlas_app.doctype.gf_content_registry.gf_content_registry.ns_get_workspace',
        args: { doc_name: frm.doc.name },
        callback(r) {
            if (r.exc) {
                $path.html(`<span style="color:var(--ns-danger-h)">⚠ Erro ao carregar. Verifique a configuração do Google Drive.</span>`);
                $drop.html('<div class="ns-drop-hint" style="cursor:default"><svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>Não foi possível conectar ao Google Drive.</div>');
                return;
            }
            const d = r.message;
            const st = gf_ns_state(frm);
            st.folderId   = d.folder_id;
            st.folderPath = d.folder_path;
            st.images     = d.images || [];

            $path.html(`<b>${d.folder_path}</b>${d.created ? ' <span style="color:#3fb950;font-size:9px;margin-left:4px">● criada agora</span>' : ''}`);
            gf_ns_render_images(frm);
            gf_ns_render_messages(frm);
        }
    });
}

function gf_ns_render_images(frm) {
    const $root  = frm.fields_dict.ns_workspace.$wrapper.find('#gf-ns-root');
    const $drop  = $root.find('#gf-ns-drop');
    const $count = $root.find('#gf-ns-img-count');
    const st     = gf_ns_state(frm);
    const imgs   = st.images || [];

    $count.text(imgs.length ? `${imgs.length} imagem${imgs.length > 1 ? 'ns' : ''}` : '');

    if (!imgs.length) {
        $drop.html(`
            <div class="ns-drop-hint" id="gf-ns-drop-hint">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <rect x="3" y="3" width="18" height="18" rx="2"/>
                    <circle cx="8.5" cy="8.5" r="1.5"/>
                    <polyline points="21 15 16 10 5 21"/>
                </svg>
                Arraste imagens aqui ou clique em Upload<br>
                <span style="font-size:10px;opacity:.6">JPG, PNG, GIF, WebP, SVG</span>
            </div>
        `);
        $drop.find('#gf-ns-drop-hint').on('click', () => $root.find('#gf-ns-file-input').trigger('click'));
        return;
    }

    const cards = imgs.map(img => {
        const thumb = img.thumbnailLink
            ? img.thumbnailLink.replace('=s220', '=s200')
            : `https://drive.google.com/thumbnail?id=${img.id}&sz=w200`;
        const kb = img.size ? Math.round(img.size / 1024) + ' KB' : '';
        return `
            <div class="ns-img-card" data-id="${img.id}" data-thumb="${thumb}" data-name="${img.name}">
                <img src="${thumb}" alt="${img.name}" loading="lazy">
                <div class="ns-img-card-overlay">
                    <span class="ns-img-name">${img.name}</span>
                    ${kb ? `<span style="font-size:9px;color:var(--ns-text2)">${kb}</span>` : ''}
                    <button class="ns-img-del" data-id="${img.id}" data-name="${img.name}">
                        <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/>
                            <path d="M10 11v6"/><path d="M14 11v6"/>
                        </svg>
                        Excluir
                    </button>
                </div>
            </div>
        `;
    }).join('');

    $drop.html(cards);

    // Lightbox on card click (not delete button)
    $drop.find('.ns-img-card').on('click', function(e) {
        if ($(e.target).closest('.ns-img-del').length) return;
        const thumb = $(this).data('thumb');
        const name  = $(this).data('name');
        const fileId = $(this).data('id');
        const fullUrl = `https://drive.google.com/thumbnail?id=${fileId}&sz=w1600`;
        const $lb = $root.find('#gf-ns-lightbox');
        $lb.find('#gf-ns-lb-img').attr('src', fullUrl).attr('alt', name);
        $lb.addClass('open');
    });

    // Delete
    $drop.find('.ns-img-del').on('click', function(e) {
        e.stopPropagation();
        const fileId   = $(this).data('id');
        const fileName = $(this).data('name');
        frappe.confirm(
            `Excluir permanentemente <b>${fileName}</b> do Google Drive?`,
            () => gf_ns_delete_image(frm, fileId)
        );
    });
}

function gf_ns_delete_image(frm, fileId) {
    const $root = frm.fields_dict.ns_workspace.$wrapper.find('#gf-ns-root');
    frappe.call({
        method: 'ichis_atlas_app.ichis_atlas_app.doctype.gf_content_registry.gf_content_registry.ns_delete_file',
        args: { file_id: fileId },
        callback(r) {
            if (!r.exc) {
                const st = gf_ns_state(frm);
                st.images = st.images.filter(i => i.id !== fileId);
                gf_ns_render_images(frm);
                frappe.show_alert({ message: 'Imagem excluída.', indicator: 'green' }, 3);
            }
        }
    });
}

function gf_ns_upload_files(frm, files) {
    const $root     = frm.fields_dict.ns_workspace.$wrapper.find('#gf-ns-root');
    const $progress = $root.find('#gf-ns-progress-wrap');
    const $bar      = $root.find('#gf-ns-progress-bar');
    const $status   = $root.find('#gf-ns-upload-status');

    $progress.show();
    $bar.css('width', '0%');

    let done = 0;
    const total = files.length;

    function uploadOne(file) {
        return new Promise((resolve) => {
            const reader = new FileReader();
            reader.onload = function(e) {
                const b64 = e.target.result.split(',')[1];
                frappe.call({
                    method: 'ichis_atlas_app.ichis_atlas_app.doctype.gf_content_registry.gf_content_registry.ns_upload_file',
                    args: {
                        doc_name:    frm.doc.name,
                        filename:    file.name,
                        file_base64: b64,
                        mime_type:   file.type || 'image/jpeg',
                    },
                    callback(r) {
                        done++;
                        $bar.css('width', `${Math.round((done / total) * 100)}%`);
                        $status.text(`${done}/${total}`);
                        if (r.message && r.message.file) {
                            gf_ns_state(frm).images.unshift(r.message.file);
                        }
                        resolve();
                    }
                });
            };
            reader.readAsDataURL(file);
        });
    }

    (async () => {
        for (const f of files) await uploadOne(f);
        gf_ns_render_images(frm);
        setTimeout(() => {
            $progress.hide();
            $bar.css('width', '0%');
            $status.text('');
        }, 1500);
        frappe.show_alert({ message: `${total} imagem${total > 1 ? 'ns' : ''} enviada${total > 1 ? 's' : ''}.`, indicator: 'green' }, 4);
    })();
}

// ── Prompt / Mensagens ──────────────────────────────────────────────────────

function gf_ns_render_messages(frm) {
    const $root = frm.fields_dict.ns_workspace.$wrapper.find('#gf-ns-root');
    const $msgs = $root.find('#gf-ns-msgs');
    const st    = gf_ns_state(frm);

    if (!st.messages.length) {
        $msgs.html(`
            <div class="ns-msg-empty">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2">
                    <path d="M12 2L2 7l10 5 10-5-10-5z"/>
                    <path d="M2 17l10 5 10-5"/>
                    <path d="M2 12l10 5 10-5"/>
                </svg>
                <span>Nenhuma interação ainda.<br>Digite um prompt abaixo para começar.</span>
            </div>
        `);
        return;
    }

    const html = st.messages.map(m => {
        const isUser = m.role === 'user';
        const initials = isUser ? 'U' : 'AI';
        return `
            <div class="ns-msg ${m.role}">
                <div class="ns-msg-avatar ${isUser ? 'user' : 'ai'}">${initials}</div>
                <div class="ns-msg-body">
                    <div class="ns-msg-role">${isUser ? 'Você' : 'Assistente'}</div>
                    <div class="ns-msg-text">${frappe.utils.escape_html(m.content)}</div>
                </div>
            </div>
        `;
    }).join('');

    $msgs.html(html);
    $msgs.scrollTop($msgs[0].scrollHeight);
}

function gf_ns_send(frm) {
    const $root  = frm.fields_dict.ns_workspace.$wrapper.find('#gf-ns-root');
    const $input = $root.find('#gf-ns-input');
    const text   = ($input.val() || '').trim();
    if (!text) return;

    const st = gf_ns_state(frm);
    st.messages.push({ role: 'user', content: text });
    gf_ns_render_messages(frm);
    $input.val('').css('height', 'auto');

    // Placeholder response — será substituído por chamada real à IA
    st.messages.push({
        role: 'assistant',
        content: '⚙ Integração com IA em configuração. Em breve esta área enviará seus prompts ao Gemini / OpenAI configurados em GF Integration Settings.'
    });
    gf_ns_render_messages(frm);
}

function gf_ns_add_doc_context(frm) {
    const ctx = [
        `Título: ${frm.doc.title || ''}`,
        `Internal Name: ${frm.doc.internal_name || ''}`,
        `Tipo: ${frm.doc.item_type || ''}`,
        `Status: ${frm.doc.status || ''}`,
        `Versão: ${frm.doc.version || ''}`,
        `Grupo de Conteúdo: ${frm.doc.content_group || ''}`,
        `Rota/URL: ${frm.doc.route_url || ''}`,
        `Descrição: ${frm.doc.description || ''}`,
        `Tags: ${frm.doc.tags || ''}`,
    ].filter(l => !l.endsWith(': ')).join('\n');

    const $root  = frm.fields_dict.ns_workspace.$wrapper.find('#gf-ns-root');
    const $input = $root.find('#gf-ns-input');
    const cur    = ($input.val() || '').trim();
    $input.val(cur ? `${cur}\n\n[Contexto do Registro]\n${ctx}` : `[Contexto do Registro]\n${ctx}`);
    $input[0].style.height = 'auto';
    $input[0].style.height = Math.min($input[0].scrollHeight, 120) + 'px';
    $input.focus();
    frappe.show_alert({ message: 'Contexto do registro adicionado ao prompt.', indicator: 'blue' }, 3);
}

// ═══════════════════════════════════════════════════════════════════════════
//  SETTINGS WORKSPACE
// ═══════════════════════════════════════════════════════════════════════════

function gf_st_ensure_styles() {
    if (document.getElementById('gf-st-styles')) return;
    const css = `
        #gf-st-root *,#gf-st-root *::before,#gf-st-root *::after{box-sizing:border-box;margin:0;padding:0}
        #gf-st-root{
            --st-bg:       #0d1117;
            --st-surface:  #161b22;
            --st-card:     #1c2128;
            --st-border:   #30363d;
            --st-border2:  #21262d;
            --st-text:     #e6edf3;
            --st-text2:    #8b949e;
            --st-text3:    #484f58;
            --st-label:    #6e7681;
            --st-blue:     #1f6feb;
            --st-blue-h:   #388bfd;
            --st-green:    #238636;
            --st-green-h:  #2ea043;
            --st-amber:    #d29922;
            --st-red:      #da3633;
            --st-radius:   8px;
            --st-radius-sm:5px;
            background: var(--st-bg);
            color: var(--st-text);
            font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',system-ui,sans-serif;
            font-size: 13px;
            border-radius: 10px;
            border: 1px solid var(--st-border);
            overflow: hidden;
        }
        /* Header */
        .st-header{
            display:flex;align-items:center;gap:10px;
            padding:13px 18px;
            background:var(--st-surface);
            border-bottom:1px solid var(--st-border);
        }
        .st-header-logo{
            display:flex;align-items:center;gap:7px;
            font-size:13px;font-weight:600;color:var(--st-text);letter-spacing:.2px;
        }
        .st-header-meta{
            margin-left:auto;display:flex;align-items:center;gap:6px;font-size:11px;color:var(--st-text2);
        }
        .st-header-meta span{
            background:var(--st-bg);border:1px solid var(--st-border2);
            border-radius:4px;padding:2px 8px;
        }
        .st-header-meta .st-version{color:var(--st-blue-h)}
        .st-badge-new{
            font-size:9px;font-weight:700;letter-spacing:.8px;text-transform:uppercase;
            padding:2px 7px;border-radius:20px;background:rgba(31,111,235,.15);
            color:var(--st-blue-h);border:1px solid rgba(56,139,253,.25);
        }
        .st-badge-saved{
            font-size:9px;font-weight:700;letter-spacing:.8px;text-transform:uppercase;
            padding:2px 7px;border-radius:20px;background:rgba(35,134,54,.15);
            color:#3fb950;border:1px solid rgba(63,185,80,.25);
        }
        /* Body scroll */
        .st-body{
            padding:18px;overflow-y:auto;
            max-height:calc(100vh - 240px);
            min-height:400px;
        }
        .st-body::-webkit-scrollbar{width:5px}
        .st-body::-webkit-scrollbar-track{background:transparent}
        .st-body::-webkit-scrollbar-thumb{background:var(--st-border);border-radius:3px}
        /* Card */
        .st-card{
            background:var(--st-card);
            border:1px solid var(--st-border2);
            border-radius:var(--st-radius);
            overflow:visible;
            margin-bottom:14px;
        }
        .st-card:last-child{margin-bottom:0}
        .st-card-hd{
            display:flex;align-items:center;gap:8px;
            padding:11px 16px;
            border-bottom:1px solid var(--st-border2);
            background:rgba(255,255,255,.018);
        }
        .st-card-hd-icon{
            width:22px;height:22px;border-radius:5px;
            display:flex;align-items:center;justify-content:center;
            background:rgba(255,255,255,.05);flex-shrink:0;
        }
        .st-card-hd-title{
            font-size:11px;font-weight:600;color:var(--st-text2);
            letter-spacing:.5px;text-transform:uppercase;
        }
        .st-card-hd-desc{
            margin-left:auto;font-size:10.5px;color:var(--st-text3);
        }
        .st-card-body{padding:16px}
        /* Grid row */
        .st-row{
            display:grid;
            grid-template-columns:repeat(var(--cols,1),1fr);
            gap:14px;
            margin-bottom:14px;
        }
        .st-row:last-child{margin-bottom:0}
        /* Field */
        .st-field{display:flex;flex-direction:column;gap:5px;position:relative}
        .st-label{
            font-size:11px;font-weight:500;color:var(--st-label);
            letter-spacing:.3px;display:flex;align-items:center;gap:5px;
        }
        .st-label .st-req{color:var(--st-red);font-size:10px}
        .st-desc{font-size:10.5px;color:var(--st-text3);margin-top:2px;line-height:1.4}
        /* Inputs */
        .st-input,.st-select,.st-textarea{
            background:var(--st-bg);
            border:1px solid var(--st-border);
            border-radius:var(--st-radius-sm);
            color:var(--st-text);
            font-size:13px;
            padding:8px 11px;
            outline:none;
            width:100%;
            font-family:inherit;
            transition:border-color .15s,box-shadow .15s;
            line-height:1.4;
        }
        .st-input:focus,.st-select:focus,.st-textarea:focus{
            border-color:var(--st-blue);
            box-shadow:0 0 0 3px rgba(31,111,235,.12);
        }
        .st-input[readonly],.st-input:disabled{
            color:var(--st-text2);cursor:default;
            background:rgba(255,255,255,.025);
        }
        .st-input::placeholder,.st-textarea::placeholder{color:var(--st-text3)}
        .st-select{
            appearance:none;
            background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='6'%3E%3Cpath d='M0 0l5 6 5-6z' fill='%236e7681'/%3E%3C/svg%3E");
            background-repeat:no-repeat;
            background-position:right 10px center;
            padding-right:28px;cursor:pointer;
        }
        .st-select option{background:#1c2128}
        .st-textarea{resize:vertical;min-height:72px}
        /* Read-only row with action */
        .st-input-row{display:flex;gap:6px;align-items:center}
        .st-input-row .st-input{flex:1}
        /* Link field */
        .st-link-wrap{position:relative}
        .st-link-icon{
            position:absolute;right:9px;top:50%;transform:translateY(-50%);
            color:var(--st-text3);pointer-events:none;
        }
        .st-link-wrap .st-input{padding-right:28px}
        .st-dd{
            position:absolute;top:calc(100% + 3px);left:0;right:0;z-index:9999;
            background:var(--st-surface);border:1px solid var(--st-border);
            border-radius:var(--st-radius-sm);overflow:hidden;
            box-shadow:0 8px 24px rgba(0,0,0,.5);
        }
        .st-dd-item{
            padding:8px 12px;font-size:12.5px;cursor:pointer;
            color:var(--st-text);transition:background .1s;
            white-space:nowrap;overflow:hidden;text-overflow:ellipsis;
            display:flex;align-items:center;gap:8px;
        }
        .st-dd-item:hover,.st-dd-item.active{background:rgba(56,139,253,.15);color:var(--st-blue-h)}
        .st-dd-empty{padding:10px 12px;font-size:12px;color:var(--st-text3)}
        /* Toggle */
        .st-toggle-row{
            display:flex;align-items:center;justify-content:space-between;
            padding:10px 0;border-bottom:1px solid var(--st-border2);
        }
        .st-toggle-row:last-child{border-bottom:none;padding-bottom:0}
        .st-toggle-row:first-child{padding-top:0}
        .st-toggle-info{display:flex;flex-direction:column;gap:2px}
        .st-toggle-title{font-size:13px;color:var(--st-text)}
        .st-toggle-desc{font-size:11px;color:var(--st-text3)}
        .st-toggle{
            position:relative;width:38px;height:22px;flex-shrink:0;cursor:pointer;
        }
        .st-toggle input{opacity:0;width:0;height:0;position:absolute}
        .st-toggle-track{
            position:absolute;inset:0;border-radius:11px;
            background:var(--st-border);transition:background .2s;
        }
        .st-toggle input:checked + .st-toggle-track{background:var(--st-green)}
        .st-toggle-thumb{
            position:absolute;top:3px;left:3px;
            width:16px;height:16px;border-radius:50%;
            background:#fff;box-shadow:0 1px 3px rgba(0,0,0,.4);
            transition:transform .2s;
        }
        .st-toggle input:checked ~ .st-toggle-thumb{transform:translateX(16px)}
        /* Color field */
        .st-color-wrap{display:flex;align-items:center;gap:10px}
        .st-color-swatch{
            width:36px;height:36px;border-radius:var(--st-radius-sm);
            border:1px solid var(--st-border);cursor:pointer;flex-shrink:0;
            background:#888;transition:border-color .15s;
        }
        .st-color-swatch:hover{border-color:var(--st-blue-h)}
        .st-color-input-native{
            position:absolute;opacity:0;width:36px;height:36px;cursor:pointer;
        }
        .st-color-hex{flex:1}
        /* Icon field */
        .st-icon-wrap{display:flex;align-items:center;gap:8px}
        .st-icon-preview{
            display:flex;align-items:center;gap:6px;
            padding:7px 10px;border-radius:var(--st-radius-sm);
            background:var(--st-bg);border:1px solid var(--st-border2);
            font-size:12px;color:var(--st-text2);flex:1;min-height:36px;
        }
        .st-icon-preview svg,.st-icon-preview i{color:#3fb950;flex-shrink:0}
        .st-btn{
            display:inline-flex;align-items:center;gap:5px;
            padding:7px 12px;border-radius:var(--st-radius-sm);
            font-size:11.5px;font-weight:500;cursor:pointer;border:1px solid transparent;
            transition:all .15s;white-space:nowrap;font-family:inherit;
        }
        .st-btn-ghost{
            background:transparent;color:var(--st-text2);border-color:var(--st-border);
        }
        .st-btn-ghost:hover{background:rgba(255,255,255,.05);color:var(--st-text);border-color:var(--st-border2)}
        .st-btn-blue{
            background:rgba(31,111,235,.15);color:var(--st-blue-h);border-color:rgba(56,139,253,.3);
        }
        .st-btn-blue:hover{background:rgba(31,111,235,.25)}
        /* Separator */
        .st-sep{border:none;border-top:1px solid var(--st-border2);margin:4px 0 14px}
        /* Route url special */
        .st-route-display{
            flex:1;padding:8px 11px;border-radius:var(--st-radius-sm);
            background:rgba(255,255,255,.025);border:1px solid var(--st-border2);
            color:var(--st-text2);font-size:12.5px;font-family:monospace;
            white-space:nowrap;overflow:hidden;text-overflow:ellipsis;
        }
        /* Status chip */
        .st-status-chip{
            display:inline-flex;align-items:center;gap:5px;
            font-size:10px;font-weight:600;letter-spacing:.4px;text-transform:uppercase;
            padding:3px 9px;border-radius:20px;
        }
        .st-dot{width:6px;height:6px;border-radius:50%;background:currentColor;flex-shrink:0}
        /* Inline two-col for config toggles */
        .st-toggles-grid{display:grid;grid-template-columns:1fr 1fr;gap:0}
        @media(max-width:600px){.st-toggles-grid{grid-template-columns:1fr}}
    `;
    const el = document.createElement('style');
    el.id = 'gf-st-styles';
    el.textContent = css;
    document.head.appendChild(el);
}

// ── Render principal ─────────────────────────────────────────────────────────

function gf_st_render(frm) {
    const $fd = frm.fields_dict.settings_workspace;
    if (!$fd) return;
    const $root = $fd.$wrapper.find('#gf-st-root');
    if (!$root.length) return;

    const doc   = frm.doc;
    const isNew = !!doc.__islocal;

    const ITEM_TYPES = ['','WEB_PAGE','REPORT','DASHBOARD','PDF','HTML','DOCUMENT',
        'APPLICATION','WORKFLOW','EXTERNAL_LINK','API','SCRIPT','OTHER'];
    const STATUSES   = ['Draft','Em Desenvolvimento','Em Teste','Submetido','Obsoleto','Arquivado'];

    function opt(arr, val) {
        return arr.map(o => `<option value="${o}"${o===val?' selected':''}>${o||'—'}</option>`).join('');
    }

    function stChip(status) {
        const map = {
            'Draft':             ['#768390','Draft'],
            'Em Desenvolvimento':['#d29922','Dev'],
            'Em Teste':          ['#388bfd','Teste'],
            'Submetido':         ['#3fb950','Ativo'],
            'Obsoleto':          ['#da3633','Obsoleto'],
            'Arquivado':         ['#484f58','Arquivado'],
        };
        const [color, label] = map[status] || ['#768390', status];
        return `<span class="st-status-chip" style="background:${color}22;color:${color};border:1px solid ${color}44">
            <span class="st-dot"></span>${label}
        </span>`;
    }

    $root.html(`
        <div class="st-header">
            <div class="st-header-logo">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#388bfd" stroke-width="1.8">
                    <circle cx="12" cy="12" r="3"/><path d="M12 1v4M12 19v4M4.22 4.22l2.83 2.83M16.95 16.95l2.83 2.83M1 12h4M19 12h4M4.22 19.78l2.83-2.83M16.95 7.05l2.83-2.83"/>
                </svg>
                Settings
                <span class="${isNew ? 'st-badge-new' : 'st-badge-saved'}">${isNew ? 'NOVO' : 'SALVO'}</span>
            </div>
            <div class="st-header-meta">
                ${doc.name && !isNew ? `<span style="font-family:monospace;font-size:10px">${doc.name}</span>` : ''}
                ${doc.version ? `<span class="st-version">v${doc.version}</span>` : ''}
            </div>
        </div>

        <div class="st-body">

            <!-- ── Identidade ── -->
            <div class="st-card">
                <div class="st-card-hd">
                    <div class="st-card-hd-icon">
                        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#8b949e" stroke-width="2">
                            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                            <circle cx="12" cy="7" r="4"/>
                        </svg>
                    </div>
                    <span class="st-card-hd-title">Identidade</span>
                </div>
                <div class="st-card-body">
                    <div class="st-row" style="--cols:1;margin-bottom:14px">
                        <div class="st-field">
                            <label class="st-label">Título <span class="st-req">*</span></label>
                            <input class="st-input" data-st-field="title" type="text"
                                placeholder="Nome exibido no portal"
                                value="${frappe.utils.escape_html(doc.title || '')}">
                        </div>
                    </div>
                    <div class="st-row" style="--cols:2">
                        <div class="st-field">
                            <label class="st-label">Internal Name <span class="st-req">*</span></label>
                            <input class="st-input" data-st-field="internal_name" type="text"
                                placeholder="auto-gerado"
                                value="${frappe.utils.escape_html(doc.internal_name || '')}"
                                ${isNew ? '' : 'readonly'}>
                            <span class="st-desc">Identificador técnico único — gerado ao digitar o título.</span>
                        </div>
                        <div class="st-field">
                            <label class="st-label">Versão</label>
                            <input class="st-input" type="text" readonly
                                value="${frappe.utils.escape_html(doc.version || '1.0.0')}">
                        </div>
                    </div>
                </div>
            </div>

            <!-- ── Classificação ── -->
            <div class="st-card">
                <div class="st-card-hd">
                    <div class="st-card-hd-icon">
                        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#8b949e" stroke-width="2">
                            <path d="M4 6h16M4 10h16M4 14h16M4 18h7"/>
                        </svg>
                    </div>
                    <span class="st-card-hd-title">Classificação</span>
                    ${stChip(doc.status || 'Draft')}
                </div>
                <div class="st-card-body">
                    <div class="st-row" style="--cols:2">
                        <div class="st-field">
                            <label class="st-label">Tipo do Item <span class="st-req">*</span></label>
                            <select class="st-select" data-st-field="item_type">${opt(ITEM_TYPES, doc.item_type)}</select>
                        </div>
                        <div class="st-field">
                            <label class="st-label">Status</label>
                            <select class="st-select" data-st-field="status">${opt(STATUSES, doc.status || 'Draft')}</select>
                        </div>
                    </div>
                </div>
            </div>

            <!-- ── Grupos & Acesso ── -->
            <div class="st-card">
                <div class="st-card-hd">
                    <div class="st-card-hd-icon">
                        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#8b949e" stroke-width="2">
                            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                            <circle cx="9" cy="7" r="4"/>
                            <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
                            <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
                        </svg>
                    </div>
                    <span class="st-card-hd-title">Grupos &amp; Acesso</span>
                </div>
                <div class="st-card-body">
                    <div class="st-row" style="--cols:2;margin-bottom:14px">
                        <div class="st-field">
                            <label class="st-label">Grupo de Conteúdo <span class="st-req">*</span></label>
                            <div class="st-link-wrap" data-doctype="GF Content Group" data-field="content_group">
                                <input class="st-input" data-st-field="content_group" type="text"
                                    placeholder="Buscar grupo…"
                                    value="${frappe.utils.escape_html(doc.content_group || '')}">
                                <svg class="st-link-icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
                                </svg>
                            </div>
                        </div>
                        <div class="st-field">
                            <label class="st-label">Grupo de Acesso <span class="st-req">*</span></label>
                            <div class="st-link-wrap" data-doctype="GF Access Group" data-field="access_group">
                                <input class="st-input" data-st-field="access_group" type="text"
                                    placeholder="Buscar grupo…"
                                    value="${frappe.utils.escape_html(doc.access_group || '')}">
                                <svg class="st-link-icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
                                </svg>
                            </div>
                            <span class="st-desc">Pré-preenchido pelo Grupo de Conteúdo. Editável para exceções.</span>
                        </div>
                    </div>
                    <div class="st-row" style="--cols:2">
                        <div class="st-field">
                            <label class="st-label">Responsável</label>
                            <div class="st-link-wrap" data-doctype="User" data-field="responsible_user">
                                <input class="st-input" data-st-field="responsible_user" type="text"
                                    placeholder="Buscar usuário…"
                                    value="${frappe.utils.escape_html(doc.responsible_user || '')}">
                                <svg class="st-link-icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
                                </svg>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- ── Skill & Vínculos ── -->
            <div class="st-card">
                <div class="st-card-hd">
                    <div class="st-card-hd-icon">
                        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#8b949e" stroke-width="2">
                            <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/>
                            <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>
                        </svg>
                    </div>
                    <span class="st-card-hd-title">Skill &amp; Vínculos</span>
                </div>
                <div class="st-card-body">
                    <div class="st-row" style="--cols:2">
                        <div class="st-field">
                            <label class="st-label">Skill <span class="st-req">*</span></label>
                            <div class="st-link-wrap" data-doctype="GF Skill" data-field="skill">
                                <input class="st-input" data-st-field="skill" type="text"
                                    placeholder="Buscar skill…"
                                    value="${frappe.utils.escape_html(doc.skill || '')}">
                                <svg class="st-link-icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
                                </svg>
                            </div>
                        </div>
                        <div class="st-field">
                            <label class="st-label">Web Page</label>
                            <div class="st-link-wrap" data-doctype="Web Page" data-field="web_page">
                                <input class="st-input" data-st-field="web_page" type="text"
                                    placeholder="Buscar página…"
                                    value="${frappe.utils.escape_html(doc.web_page || '')}">
                                <svg class="st-link-icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
                                </svg>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- ── Localização ── -->
            <div class="st-card">
                <div class="st-card-hd">
                    <div class="st-card-hd-icon">
                        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#8b949e" stroke-width="2">
                            <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
                            <circle cx="12" cy="10" r="3"/>
                        </svg>
                    </div>
                    <span class="st-card-hd-title">Localização &amp; Referência</span>
                </div>
                <div class="st-card-body">
                    <div class="st-row" style="--cols:1;margin-bottom:14px">
                        <div class="st-field">
                            <label class="st-label">URL / Rota Google Drive</label>
                            <div class="st-input-row">
                                <span class="st-route-display" id="gf-st-route-display">${frappe.utils.escape_html(doc.route_url || '— Será preenchida ao salvar —')}</span>
                                <button class="st-btn st-btn-ghost" id="gf-st-test-url" title="Abrir no navegador"
                                    style="${doc.route_url ? '' : 'opacity:.4;cursor:default'}">
                                    <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                        <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>
                                        <polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/>
                                    </svg>
                                    Testar
                                </button>
                            </div>
                            <span class="st-desc">Caminho hierárquico da pasta no Google Drive. Preenchido automaticamente ao salvar.</span>
                        </div>
                    </div>
                    <div class="st-row" style="--cols:2">
                        <div class="st-field">
                            <label class="st-label">DocType de Referência</label>
                            <input class="st-input" data-st-field="reference_doctype" type="text"
                                placeholder="Ex: Sales Invoice"
                                value="${frappe.utils.escape_html(doc.reference_doctype || '')}">
                        </div>
                        <div class="st-field">
                            <label class="st-label">Nome de Referência</label>
                            <input class="st-input" data-st-field="reference_name" type="text"
                                placeholder="Nome do documento referenciado"
                                value="${frappe.utils.escape_html(doc.reference_name || '')}">
                        </div>
                    </div>
                </div>
            </div>

            <!-- ── Apresentação ── -->
            <div class="st-card">
                <div class="st-card-hd">
                    <div class="st-card-hd-icon">
                        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#8b949e" stroke-width="2">
                            <circle cx="12" cy="12" r="10"/><path d="M12 8v4l3 3"/>
                        </svg>
                    </div>
                    <span class="st-card-hd-title">Apresentação</span>
                </div>
                <div class="st-card-body">
                    <div class="st-row" style="--cols:1;margin-bottom:14px">
                        <div class="st-field">
                            <label class="st-label">Descrição</label>
                            <textarea class="st-textarea" data-st-field="description"
                                placeholder="Descreva o conteúdo ou finalidade deste item…">${frappe.utils.escape_html(doc.description || '')}</textarea>
                        </div>
                    </div>
                    <div class="st-row" style="--cols:1;margin-bottom:14px">
                        <div class="st-field">
                            <label class="st-label">Tags</label>
                            <input class="st-input" data-st-field="tags" type="text"
                                placeholder="Ex: relatório, mensal, produção"
                                value="${frappe.utils.escape_html(doc.tags || '')}">
                        </div>
                    </div>
                    <div class="st-row" style="--cols:2">
                        <div class="st-field">
                            <label class="st-label">Ícone</label>
                            <div class="st-icon-wrap">
                                <div class="st-icon-preview" id="gf-st-icon-preview">
                                    <span style="opacity:.4;font-size:11.5px">Nenhum ícone</span>
                                </div>
                                <button class="st-btn st-btn-ghost" onclick="gf_open_icon_picker(cur_frm)"
                                    title="Escolher ícone Lucide">
                                    <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                        <circle cx="12" cy="12" r="10"/>
                                        <circle cx="12" cy="10" r="3"/>
                                        <path d="M7 20.662V19a2 2 0 0 1 2-2h6a2 2 0 0 1 2 2v1.662"/>
                                    </svg>
                                    Escolher
                                </button>
                            </div>
                        </div>
                        <div class="st-field">
                            <label class="st-label">Cor</label>
                            <div class="st-color-wrap">
                                <div style="position:relative;flex-shrink:0">
                                    <input type="color" class="st-color-input-native" id="gf-st-color-native"
                                        value="${doc.color || '#888888'}">
                                    <div class="st-color-swatch" id="gf-st-color-swatch"
                                        style="background:${doc.color || '#888888'}"></div>
                                </div>
                                <input class="st-input st-color-hex" data-st-field="color" type="text"
                                    placeholder="#RRGGBB"
                                    value="${frappe.utils.escape_html(doc.color || '')}">
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- ── Configurações ── -->
            <div class="st-card">
                <div class="st-card-hd">
                    <div class="st-card-hd-icon">
                        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#8b949e" stroke-width="2">
                            <circle cx="12" cy="12" r="3"/>
                            <path d="M19.07 4.93a10 10 0 0 1 0 14.14M4.93 4.93a10 10 0 0 0 0 14.14"/>
                        </svg>
                    </div>
                    <span class="st-card-hd-title">Configurações</span>
                </div>
                <div class="st-card-body">
                    <div class="st-row" style="--cols:2;margin-bottom:16px">
                        <div class="st-field">
                            <label class="st-label">Ordem de Exibição</label>
                            <input class="st-input" data-st-field="sort_order" type="number"
                                placeholder="0"
                                value="${doc.sort_order != null ? doc.sort_order : ''}">
                        </div>
                        <div class="st-field">
                            <label class="st-label">Última Revisão</label>
                            <input class="st-input" data-st-field="last_reviewed_on" type="date"
                                value="${doc.last_reviewed_on || ''}">
                        </div>
                    </div>
                    <div class="st-toggle-row">
                        <div class="st-toggle-info">
                            <span class="st-toggle-title">Ativo</span>
                            <span class="st-toggle-desc">Desmarque para ocultar do portal sem excluir.</span>
                        </div>
                        <label class="st-toggle">
                            <input type="checkbox" data-st-field="active" ${doc.active ? 'checked' : ''}>
                            <div class="st-toggle-track"></div>
                            <div class="st-toggle-thumb"></div>
                        </label>
                    </div>
                    <div class="st-toggle-row">
                        <div class="st-toggle-info">
                            <span class="st-toggle-title">Exibir na Home</span>
                            <span class="st-toggle-desc">Mostra este item no painel inicial do portal.</span>
                        </div>
                        <label class="st-toggle">
                            <input type="checkbox" data-st-field="show_on_home" ${doc.show_on_home ? 'checked' : ''}>
                            <div class="st-toggle-track"></div>
                            <div class="st-toggle-thumb"></div>
                        </label>
                    </div>
                    <div class="st-toggle-row">
                        <div class="st-toggle-info">
                            <span class="st-toggle-title">Favorito</span>
                            <span class="st-toggle-desc">Marca este item como favorito.</span>
                        </div>
                        <label class="st-toggle">
                            <input type="checkbox" data-st-field="favorite" ${doc.favorite ? 'checked' : ''}>
                            <div class="st-toggle-track"></div>
                            <div class="st-toggle-thumb"></div>
                        </label>
                    </div>
                </div>
            </div>

            <!-- ── Versionamento ── -->
            <div class="st-card">
                <div class="st-card-hd">
                    <div class="st-card-hd-icon">
                        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#8b949e" stroke-width="2">
                            <circle cx="12" cy="12" r="4"/>
                            <line x1="1.05" y1="12" x2="7" y2="12"/>
                            <line x1="17.01" y1="12" x2="22.96" y2="12"/>
                        </svg>
                    </div>
                    <span class="st-card-hd-title">Versionamento</span>
                </div>
                <div class="st-card-body">
                    <div class="st-field">
                        <label class="st-label">Versão Anterior</label>
                        <div class="st-link-wrap" data-doctype="GF Content Registry" data-field="previous_version">
                            <input class="st-input" data-st-field="previous_version" type="text"
                                placeholder="Vincular versão anterior…"
                                value="${frappe.utils.escape_html(doc.previous_version || '')}">
                            <svg class="st-link-icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
                            </svg>
                        </div>
                        <span class="st-desc">Aponta para o GF Content Registry que esta versão substitui.</span>
                    </div>
                </div>
            </div>

        </div>
    `);

    // Atualiza icon preview após render
    gf_st_update_icon_preview($root, doc.icon);
    gf_load_lucide(() => lucide.createIcons({ attrs: { style: 'display:block' } }));

    gf_st_bind(frm, $root);
}

// ── Bind de eventos ──────────────────────────────────────────────────────────

function gf_st_bind(frm, $root) {
    // Data / Text / Textarea / Number / Date / Select
    $root.find('[data-st-field]').not('[type="checkbox"]').not('[type="color"]').on('change', function() {
        const field = $(this).data('st-field');
        const val   = $(this).val();
        frm.set_value(field, val);

        // Atualiza chip de status no header do card se for o campo status
        if (field === 'status') {
            const STATUSES = ['Draft','Em Desenvolvimento','Em Teste','Submetido','Obsoleto','Arquivado'];
            const map = {
                'Draft':'#768390','Em Desenvolvimento':'#d29922','Em Teste':'#388bfd',
                'Submetido':'#3fb950','Obsoleto':'#da3633','Arquivado':'#484f58'
            };
            const color = map[val] || '#768390';
            $root.find('.st-status-chip').html(
                `<span class="st-dot"></span>${val}`
            ).css({'background': color + '22', 'color': color, 'border': `1px solid ${color}44`});
        }
    });

    // Checkboxes (toggles)
    $root.find('[data-st-field][type="checkbox"]').on('change', function() {
        frm.set_value($(this).data('st-field'), $(this).is(':checked') ? 1 : 0);
    });

    // Color — native picker + hex input
    $root.find('#gf-st-color-native').on('input', function() {
        const hex = $(this).val();
        $root.find('#gf-st-color-swatch').css('background', hex);
        $root.find('[data-st-field="color"]').val(hex);
        frm.set_value('color', hex);
    });
    $root.find('[data-st-field="color"]').on('change', function() {
        const hex = $(this).val();
        if (/^#[0-9a-fA-F]{6}$/.test(hex)) {
            $root.find('#gf-st-color-swatch').css('background', hex);
            $root.find('#gf-st-color-native').val(hex);
        }
    });
    $root.find('#gf-st-color-swatch').on('click', function() {
        $root.find('#gf-st-color-native').trigger('click');
    });

    // Testar URL
    $root.find('#gf-st-test-url').on('click', function() {
        const url = frm.doc.route_url;
        if (!url || url.startsWith('🔍')) return;
        window.open(/^https?:\/\//.test(url) ? url : window.location.origin + url, '_blank');
    });

    // Link fields — autocomplete
    $root.find('.st-link-wrap').each(function() {
        const $wrap    = $(this);
        const doctype  = $wrap.data('doctype');
        const fieldname = $wrap.data('field');
        const $input   = $wrap.find('input');
        gf_st_bind_link($input, $wrap, doctype, fieldname, frm);
    });

    // title → auto-slug internal_name
    $root.find('[data-st-field="title"]').on('input', function() {
        if (!frm.doc.__islocal) return;
        const ver  = (frm.doc.version || '1.0.0').replace(/\./g, '_');
        const slug = $(this).val()
            .toLowerCase()
            .normalize('NFD').replace(/[̀-ͯ]/g, '')
            .replace(/[^a-z0-9]+/g, '_')
            .replace(/^_+|_+$/g, '');
        const newName = slug ? `${slug}_v${ver}` : '';
        $root.find('[data-st-field="internal_name"]').val(newName);
        frm.doc.internal_name = newName;
    });
    $root.find('[data-st-field="title"]').on('change', function() {
        frm.set_value('title', $(this).val());
    });

    // content_group → preenche access_group
    $root.find('[data-st-field="content_group"]').on('_linkselect', function(e, val) {
        if (!val) return;
        frappe.db.get_value('GF Content Group', val, ['default_access_group', 'external_reference'], (r) => {
            if (!r) return;
            if (r.default_access_group && !frm.doc.access_group) {
                frm.set_value('access_group', r.default_access_group);
                $root.find('[data-st-field="access_group"]').val(r.default_access_group);
            }
            if (r.external_reference) {
                const preview = `🔍 Pasta: ${r.external_reference} (será resolvida ao salvar)`;
                frm.doc.route_url = preview;
                $root.find('#gf-st-route-display').text(preview);
            }
        });
    });
}

// ── Link autocomplete ────────────────────────────────────────────────────────

function gf_st_bind_link($input, $wrap, doctype, fieldname, frm) {
    let $dd = null;
    let _t  = null;

    function showDd(rows) {
        if ($dd) $dd.remove();
        $dd = $('<div class="st-dd"></div>');
        if (!rows.length) {
            $dd.append('<div class="st-dd-empty">Nenhum resultado</div>');
        } else {
            rows.forEach((r, i) => {
                const label = r.title && r.title !== r.name
                    ? `<span>${frappe.utils.escape_html(r.name)}</span><span style="color:var(--st-text3);font-size:11px">${frappe.utils.escape_html(r.title)}</span>`
                    : `<span>${frappe.utils.escape_html(r.name)}</span>`;
                $(`<div class="st-dd-item${i===0?' active':''}" data-val="${frappe.utils.escape_html(r.name)}">${label}</div>`)
                    .appendTo($dd)
                    .on('mousedown', function(e) {
                        e.preventDefault();
                        const val = $(this).data('val');
                        $input.val(val);
                        frm.set_value(fieldname, val);
                        $input.trigger('_linkselect', [val]);
                        $dd.remove(); $dd = null;
                    });
            });
        }
        $wrap.append($dd);
    }

    function search(q) {
        const filters = [['name', 'like', `%${q}%`]];
        frappe.db.get_list(doctype, { filters, fields: ['name', 'title'], limit: 8 })
            .then(rows => showDd(rows));
    }

    $input.on('focus', function() {
        search($(this).val());
    });
    $input.on('input', function() {
        clearTimeout(_t);
        _t = setTimeout(() => search($(this).val()), 220);
    });
    $input.on('blur', function() {
        setTimeout(() => { if ($dd) { $dd.remove(); $dd = null; } }, 200);
        // Se o usuário limpou o campo, propaga
        if (!$(this).val()) frm.set_value(fieldname, '');
    });
    $input.on('keydown', function(e) {
        if (!$dd) return;
        const $items = $dd.find('.st-dd-item');
        const $cur   = $items.filter('.active');
        if (e.key === 'ArrowDown') {
            e.preventDefault();
            const $next = $cur.next('.st-dd-item');
            if ($next.length) { $cur.removeClass('active'); $next.addClass('active'); }
        } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            const $prev = $cur.prev('.st-dd-item');
            if ($prev.length) { $cur.removeClass('active'); $prev.addClass('active'); }
        } else if (e.key === 'Enter') {
            e.preventDefault();
            const $a = $dd.find('.st-dd-item.active');
            if ($a.length) $a.trigger('mousedown');
        } else if (e.key === 'Escape') {
            $dd.remove(); $dd = null;
        }
    });
}

// ── Icon preview no Settings ──────────────────────────────────────────────

function gf_st_update_icon_preview($root, icon) {
    const $preview = $root.find('#gf-st-icon-preview');
    if (!$preview.length) return;
    if (icon) {
        $preview.html(`<i data-lucide="${icon}" style="width:16px;height:16px"></i><span style="font-size:12px;color:var(--st-text2)">${icon}</span>`);
        gf_load_lucide(() => lucide.createIcons({ attrs: { style: 'display:block' } }));
    } else {
        $preview.html('<span style="opacity:.4;font-size:11.5px">Nenhum ícone</span>');
    }
}
