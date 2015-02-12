#
# Copyright (C) 2011 Taobao .Inc
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution. The terms
# are also available at http://code.taobao.org/license.html.
#
# This software consists of voluntary contributions made by many
# individuals. For the exact contribution history, see the revision
# history and logs, available at http://code.taobao.org/.


from django.contrib.auth.decorators import login_required
from django.http import *

from taocode2 import settings
from taocode2.helper.utils import *
from taocode2.helper import consts
from taocode2.models import *
from taocode2.apps.project.admin import can_access, can_write
from taocode2.contrib import oss_store


import time, re, os
import binascii
import urllib

__author__ = 'luqi@taobao.com'

safe_re = re.compile(r'(\.|/|\\)')

def safe_ext(f):
    ext = os.path.splitext(f)[1].lower()

    return ext in ('.exe', '.com', '.bat', '.htm', '.js', '.html', '.php', '.swf')

def get_upload_root():
    if settings.UPLOAD_DIR[0] == '/':
        d = settings.UPLOAD_DIR
    else:
        d = os.path.join(os.getcwd(), settings.UPLOAD_DIR)
    return d

def get_file_name(ftype, ftid, fname):
    f = binascii.hexlify(os.urandom(12))
    dir_name = time.strftime('%Y-%m')
    now_time = str(time.time()).replace('.','_')
    ext = os.path.splitext(fname)[1].lower()
    fname = '%s/%s_%s_%s_%s%s'%(dir_name, now_time, ftype, ftid, f, ext)

    return fname

def add_file(request, prj, ftype, ftid, f):
    fname = f.name
    if safe_ext(fname) is True:
        return

    oss_fname = get_file_name(ftype, ftid, fname)
    oss_store.add_file(oss_fname, f.read())

    att = ProjectAttachment()
    att.project = prj
    att.ftype = ftype
    att.ftid = ftid
    att.owner = request.user
    att.status = consts.FILE_ENABLE
    att.fname = 'oss://'+oss_fname
    att.orig_name = os.path.split(fname)[1]
    att.size = f.tell()
    att.save()
    
def get_file(request, name, fid):
    item = q_get(ProjectAttachment, id=int(fid))

    if item is None or item.status != consts.FILE_ENABLE:
        raise Http404
    
    resp = can_access(item.project, request.user)
    if resp is not None:
        return resp

    fname = item.fname

    if safe_ext(item.orig_name) is True:
        return Http404
    fdata = None
    if item.fname.startswith('oss://'):
        ores = oss_store.get_file(item.fname[len('oss://'):])
        if ores.status != 200:
            return HttpResponse(status=ores.status)
        fdata = ores.read()
    else:
        fdata = file(os.path.join(get_upload_root(), fname),'rb').read()

    resp = HttpResponse(fdata, content_type="application/oct-stream")
    resp['Content-Disposition'] = 'attachment; filename="%s"'%(urllib.quote(item.orig_name.encode('utf8')),)
    
    resp['X-Content-Type-Options'] = 'nosniff'
    resp['X-XSS-Protection'] = '1; mode=block'
    
    return resp
    
@as_json
def del_file(request):

    if request.method != 'POST':
        return (False, 'Need POST')

    fid = request.POST.get('fid')
    if fid is None:
        return (False, 'Need fid')
    
    f = q_get(ProjectAttachment, pk=int(fid))

    if f is None:
        return (False, 'File not found')
    
    if can_write(f.project, request.user) is False:        
        return (False, 'Forbidden')

    f.status = consts.FILE_DELETED
    f.save()

    return True
