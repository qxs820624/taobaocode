import os
import cache_client
import traceback

from django.http import *
from django.contrib.auth import authenticate

from base64 import b64decode
from threading import Lock

from taocode2 import settings
from taocode2.models import *
from taocode2.helper.utils import *
from taocode2.helper import consts

_cacheMan = cache_client.ConnMan(settings.OCS_HOST,
                                 settings.OCS_USER,
                                 settings.OCS_PASSWORD)
_lock = Lock()
_parts = {}

def get_prj_meta(cli, name):
    key_prj = 'prj-' + name
    prj_meta = cli.get(key_prj)
    if prj_meta is not None:
        return prj_meta

    prj = q_get(Project, name=name, 
                status = consts.PROJECT_ENABLE)
    
    if prj is None:
        return None

    part_id = None
    if prj.part is not None:
        part_id = prj.part.id

    prj_meta = (prj.id, prj.is_public, prj.owner.id, part_id)
    cli.set(key_prj, prj_meta)

    return prj_meta

def get_user_meta(cli, username, password):
    key_user = 'u-%s-p-%s'%(username, password)
    user_meta = cli.get(key_user)

    if user_meta is not None:
        return user_meta

    user = authenticate(username=username, password=password)
    if user is None:
        return None

    user_meta = (user.id, user.status, user.supper)
    cli.set(key_user, user_meta)
    return user_meta

def get_pm_meta(cli, prj_id, user_id):
    key_pm = 'pm-%d-%d'%(prj_id, user_id)
    pm_meta = cli.get(key_pm)
    if pm_meta is not None:
        return pm_meta

    pm = q_get(ProjectMember, 
               project__id = prj_id, user__id = user_id, 
               member_type = consts.PM_ACCEPT_INV)

    if pm is None:
        return None

    pm_meta = pm.id
    cli.set(key_pm, pm_meta)
    return pm_meta

def is_write_method(request):
    mtd = request.method

    if mtd  in ('GET','PROPFIND','OPTIONS','REPORT'):
        return False
    return True

def get_part_meta(part_id):

    with _lock:
        part_meta = _parts.get(part_id, None)
        if part is not None:
            return part_meta
        
        part = q_get(ReposPart, pk=part_id)
        if part is None:
            return
        part_meta = (part.id, part.enable, part.prefix)
        _parts[part.id] = part_meta
        return part_meta
        
def build_repos_path(part_id, name):
    repos_path = None
    if part_id is None:
        # build default repos_path
        repos_path = settings.GET_REPOS_ADMIN_URL(name)
    else:
        part_meta = get_part_meta(part_id)
        if part_meta is None:
            return None
        repos_path = part_meta[2]

    return os.path.join(repos_path, name)

def check_auth_v0(request):
    uri = request.META.get('HTTP_X_ORIGINAL_URI')
    uri = uri[5:] #/svn/
    name = uri.split('/', 1)[0]
    
    resp =  check_auth(request, name, uri)
    return resp
    
def check_auth(request, name, uri):
    # project cache obj:
    # key: 'prj-' + name
    # tuple value: (id, is_public, owner.id, part_id)
    
    # project member cache obj:
    # key: 'pm-'+ name +'-u-' + username
    # int value: pm.id
    
    # user cache obj:
    # key: 'u-'+username+'-p-'+password
    # tuple value: (user_id, status, super)
    #
    
    cli = cache_client.get_client(_cacheMan)
    prj_meta = get_prj_meta(cli, name)
    if prj_meta is None:
        return Http404()

    resp = HttpResponse()
    resp['REPOS'] = build_repos_path(prj_meta[3], uri)
    
    is_write = is_write_method(request)

    if prj_meta[1] is True and not is_write: # is_public 
        resp.status_code = 200
        return resp
    
    auth_value = request.META.get('HTTP_AUTHORIZATION', None)

    if auth_value is None:
        resp.status_code = 401
        resp['WWW-Authenticate'] = 'Basic realm="%s"'%(settings.REALM,)
        return resp

    auth = auth_value.split(' ', 1)[1]
    name, password = b64decode(auth).split(':', 1)
    user_meta = get_user_meta(cli, name, password)

    if user_meta is None:
        resp.status_code = 403
        return resp

    if user_meta[0] == prj_meta[2]: # check is member
        resp.status_code = 200
        return resp

    pm_meta = get_pm_meta(cli, prj_meta[0], user_meta[1])
    if pm_meta is None:
        resp.status_code = 403
        return resp
        
    resp.status_code = 200
    return resp
