import frappe
import os
import re
from werkzeug.utils import secure_filename

NS_ROOT     = 'gf_atlas'
IMAGE_EXTS  = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.bmp', '.ico', '.tiff', '.avif'}


def _get_ns_path(internal_name=None, route_url=None):
    """Retorna o caminho local: public/files/gf_atlas/{route_url...}/{internal_name}"""
    base = frappe.get_site_path('public', 'files', NS_ROOT)
    if not internal_name:
        return base
    if route_url is None:
        route_url = frappe.db.get_value(
            "GF Content Registry", {"internal_name": internal_name}, "route_url"
        ) or ""
    path = base
    for part in [p for p in (route_url or "").split('/') if p]:
        path = os.path.join(path, part)
    return os.path.join(path, internal_name)


def _ns_url(internal_name, filename, route_url=None):
    """Monta a URL pública correspondente ao path local."""
    if route_url is None:
        route_url = frappe.db.get_value(
            "GF Content Registry", {"internal_name": internal_name}, "route_url"
        ) or ""
    parts = [NS_ROOT] + [p for p in (route_url or "").split('/') if p] + [internal_name, filename]
    return '/files/' + '/'.join(parts)


def _safe_name(name):
    if not name or '..' in name or '/' in name or '\\' in name:
        frappe.throw('Nome inválido.')


@frappe.whitelist()
def list_files(internal_name):
    _safe_name(internal_name)
    path = _get_ns_path(internal_name)
    os.makedirs(path, exist_ok=True)
    result = []
    try:
        for fname in sorted(os.listdir(path)):
            fpath = os.path.join(path, fname)
            if not os.path.isfile(fpath):
                continue
            ext  = os.path.splitext(fname)[1].lower()
            stat = os.stat(fpath)
            result.append({
                'name':     fname,
                'url':      _ns_url(internal_name, fname),
                'size':     stat.st_size,
                'is_image': ext in IMAGE_EXTS,
            })
    except Exception as e:
        frappe.log_error(f'Natural Studio list_files error: {e}')
    return result


@frappe.whitelist()
def delete_file(internal_name, filename):
    _safe_name(internal_name)
    _safe_name(filename)
    fpath = os.path.join(_get_ns_path(internal_name), filename)
    if not os.path.isfile(fpath):
        frappe.throw('Arquivo não encontrado.')
    os.remove(fpath)
    return {'ok': True}


@frappe.whitelist()
def upload_file(internal_name):
    _safe_name(internal_name)
    if not frappe.request or not frappe.request.files:
        frappe.throw('Nenhum arquivo enviado.')
    f = frappe.request.files.get('file')
    if not f:
        frappe.throw('Campo "file" não encontrado.')

    safe_name = secure_filename(f.filename or 'arquivo')
    if not safe_name:
        safe_name = 'arquivo'

    path = _get_ns_path(internal_name)
    os.makedirs(path, exist_ok=True)

    dest = os.path.join(path, safe_name)
    base, ext = os.path.splitext(safe_name)
    counter = 1
    while os.path.exists(dest):
        dest = os.path.join(path, f'{base}_{counter}{ext}')
        counter += 1

    f.save(dest)
    final_name = os.path.basename(dest)
    return {
        'name': final_name,
        'url':  _ns_url(internal_name, final_name),
    }


@frappe.whitelist()
def ensure_record_directories(internal_name, route_url=None):
    _safe_name(internal_name)

    if not route_url:
        # Sem route_url não é possível montar a hierarquia completa; cria apenas a raiz
        base = frappe.get_site_path('public', 'files', NS_ROOT)
        os.makedirs(base, exist_ok=True)
        return {'ok': False, 'reason': 'route_url ausente; hierarquia incompleta não criada'}

    # gf_atlas/
    base = frappe.get_site_path('public', 'files', NS_ROOT)
    os.makedirs(base, exist_ok=True)

    # gf_atlas/{route_url_parts...}/
    path = base
    for part in [p for p in route_url.split('/') if p]:
        path = os.path.join(path, part)
        os.makedirs(path, exist_ok=True)

    # gf_atlas/{route_url_parts...}/{internal_name}/
    ns_path = os.path.join(path, internal_name)
    os.makedirs(ns_path, exist_ok=True)

    return {'ok': True, 'path': ns_path}
