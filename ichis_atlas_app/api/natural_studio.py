import frappe
import os
import re
from werkzeug.utils import secure_filename

NS_URL_BASE = '/files/natural_studio/'
IMAGE_EXTS  = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.bmp', '.ico', '.tiff', '.avif'}


def _get_ns_path(internal_name=None):
    base = frappe.get_site_path('public', 'files', 'natural_studio')
    if internal_name:
        return os.path.join(base, internal_name)
    return base


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
                'url':      NS_URL_BASE + internal_name + '/' + fname,
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
        'url':  NS_URL_BASE + internal_name + '/' + final_name,
    }


@frappe.whitelist()
def ensure_record_directories(internal_name, route_url=None):
    _safe_name(internal_name)

    # Sempre garante: public/files/natural_studio/{internal_name}/
    ns_path = _get_ns_path(internal_name)
    os.makedirs(ns_path, exist_ok=True)

    created = [ns_path]

    if route_url:
        # Sanitiza route_url em nome de diretório seguro
        clean = re.sub(r'[^a-zA-Z0-9._-]', '_', route_url.strip('/'))
        clean = re.sub(r'_+', '_', clean).strip('_')
        if clean and '..' not in clean and len(clean) <= 200:
            route_base = frappe.get_site_path('public', 'files', clean)
            os.makedirs(route_base, exist_ok=True)
            route_sub = os.path.join(route_base, internal_name)
            os.makedirs(route_sub, exist_ok=True)
            created.extend([route_base, route_sub])

    return {'ok': True, 'created': created}
