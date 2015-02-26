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
from taocode2.models import *
from taocode2.helper.utils import *
from taocode2.helper import consts, xmlo
from taocode2 import settings
from taocode2.apps.project.views import *
from taocode2.apps.project.admin import can_access
from taocode2.apps.repos import svn
from taocode2.apps.wiki.views import safe_esc
from taocode2.apps.user import activity

from mimetypes import guess_type, add_type
from isodate import  parse_datetime

from django.db.models import Q
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.core.cache import cache

import marshal
import os, sys, re

__author__ = 'luqi@taobao.com'


add_type('text/x-javascript', '.js')
add_type('text/x-sh', '.sh')
add_type('text/x-java', '.java')
add_type('text/x-cpp', '.cpp')
add_type('text/x-cpp', '.cc')
add_type('text/x-cpp', '.cxx')
add_type('text/x-cpp', '.h')
add_type('text/x-cpp', '.hxx')
add_type('text/x-cpp', '.hpp')
add_type('text/x-ruby', '.rb')
add_type('text/x-yml', '.yml')
add_type('text/x-sql', '.sql')
add_type('text/x-cfg', '.cfg')
add_type('text/plain', '.ac')
add_type('text/plain', '.am')
add_type('text/plain', '.m4')
add_type('text/plain', '.spec')
add_type('text/plain', '.conf')


textchars = ''.join(map(chr, [7, 8, 9, 10, 12, 13, 27] + range(0x20, 0x100)))
is_binary_string = lambda bytes: bool(bytes.translate(None, textchars))

def get_repos_base(request, name):
    repos_path = request.META.get('HOST', 'code.taobao.org')
    repos_path += os.path.join(settings.REPOS_ROOT,name)
    return 'http://' + repos_path + '/'
    
    
def get_ext_class(fname):
    ext = os.path.splitext(fname)[1]
    if ext.startswith('.'):
        return ext[1:]
    return ''

def mark_highlight(content, fname, lexer=None):
    return force_unicode2(content)

def get_author(v):
    v = unicode(v)
    u = q_get(User, Q(name__iexact=v) | Q(email__iexact=v),
              status=consts.USER_ENABLE)
    if u is None:
        return ''

    return u.name

def build_paths(path):
    vals = path.split('/')
    paths = []
    for i in range(1, len(vals) - 1):
        paths.append({'url':'/'.join(vals[1:i + 1]), 'path':vals[i]})
    return paths


def check_acl(request, name, path):
    project = q_get(Project, name=name)
    resp = can_access(project, request.user)
    if resp != None:
        return resp, None, request.rc
    
    path = svn.safe_path(path)

    rc = request.rc
    rc.navmenusSource = build_prj_nav_menu(request, project, 'src')

    rc.project = project

    rc.pagename = path
    rc.pagedesc = project.title
    rc.path = path   
    rc.paths = build_paths(path)
    if path != '/' and path[-1] == '/':
        rc.parent = os.path.split(path[:-1])[0]
        if rc.parent != '/':
            rc.parent += '/'

    r = svn.REPOS(project.part, name, path)
    return resp, r, rc

def update_last_log(request, r, project):
    # ReposChecker

    rchk = q_get(ReposChecker, project=project)
    if rchk is None:
        rchk = ReposChecker()
        rchk.project = project
        last_rev = 1
    else:
        last_rev = rchk.last_rev
        
        info = svn.INFO(r)
        rev = int(str(info.entry.commit['revision']))
        if rev <= last_rev:
            return
        
    try:
        logs = get_logs(request, r, '%s:HEAD' % last_rev, -1)
        for log in logs:
            last_rev = log['rev']
            author = unicode(log['author'])
            u = q_get(User, Q(name__iexact=author) | Q(email__iexact=author),
                      status=consts.USER_ENABLE)
        
            if u is None:
                continue
            msg = unicode(log['msg'])
            msg = msg[:128]

            activity.new_commit(project, u, last_rev, msg,
                                ctime=log['date'])
    except:
        import traceback
        traceback.print_exc()
        #raise
        return
    
    if rchk.last_rev != last_rev:
        rchk.last_rev = last_rev
        rchk.save()

def browse(request, name, path='/'):
    resp, r, rc = check_acl(request, name, path)
    if resp is not None:
        return resp
    try:
        o = svn.LIST(r)
    except Exception, e:
        if 'E200009' in e.message:
            raise Http404
        raise


    entrys = getattr(o.list, 'entry', [])

    if path[-1] != '/':
        if type(entrys) == list or entrys['kind'] == 'dir':
            return redirect(reverse('apps.repos.views.browse', args=[name, path + '/']))

        return view_file(request, name, path, r, o)

    if path == '/':
        update_last_log(request, r, rc.project)
    
    files = []

    if type(entrys) != list:
        entrys = [entrys]

    for e in entrys:
        co = e.commit
        f = {
            'dir':e['kind'] == 'dir' and True or False,
            'name':unicode(e.name),
            'rev':co['revision'],
            'date':parse_datetime(str(co.date)),
            'author':get_author(getattr(e, 'author', '')),
            'size':int(str(getattr(e, 'size', '0')))
            }

        files.append(f)

    rc.files = files 
    rc.REPOS = get_repos_base(request, name)

    if path == '/':
        for v in ['/trunk/README', '/README']:
            try:
                c = svn.CAT(svn.REPOS(rc.project.part, name, v))
                if len(c) > 0:
                    rc.README = force_unicode2(c)
                    rc.README_FILE = v
                    break
            except:
                continue
            
    prj_q = Q(project__status=consts.PROJECT_ENABLE)

    current_user = q_get(User, name=request.user, status=consts.USER_ENABLE)
    
    owner_q = Q(owner=current_user,
                status=consts.PROJECT_ENABLE)
    
    owner_projects = Project.objects.filter(owner_q)
    
    
    joined_projects = q_gets(ProjectMember,
                                user=current_user).filter(prj_q).exclude(member_type=consts.PM_REJECT_INV)

    power='read'
    if current_user==rc.project.owner:
        power = 'all'
    
            
    for j in joined_projects:
        if current_user==j.user and rc.project==j.project:
            power='all'    
        
        


    rc.power = power
         
         
    project = q_get(Project, name=rc.project)  
    rc.project = project
    ''' 
    owner=q_get(User,name=project.owner)
    members = q_gets(ProjectMember, project = project, 
                        member_type = consts.PM_ACCEPT_INV)
    
    
    if owner==current_user:
        rc.good = 'admin'
        
    if current_user in members:
        rc.good = 'join'
    '''    

    
    update_my_project_status(request, [project])
    rs = ProjectWatcher.objects.filter(project=project).aggregate(watchers=Count('id'))
    rc.rs = rs['watchers']
    project.click = project.click +1
    project.save()

    
    return send_response(request,
                         'repos/browse.html')

def no_preview_file(fname):
    ext = os.path.splitext(fname)[1].lower()
    if ext in ('.pdf', '.docx', '.xlsx', '.doc', '.xls'):
        return True
    return False
    
def view_file(request, name, path, r, info):   
    rc = request.rc
    ul = os.path.join(settings.REPOS_ROOT, name + '/' + path)

    if request.GET.get('orig', None) is not None:
        return redirect(ul)

    rc.REPOS = get_repos_base(request, name)

    rc.mtime = parse_datetime(str(info.entry.commit.date))
    rc.author = get_author(getattr(info.entry.commit, 'author', ''))
    fsize = int(str(getattr(info.entry, 'size', '0')))
    
    rc.rev = info.entry.commit['revision']

    ft = guess_type(path)[0]
    fname = os.path.split(path)[1]

    if no_preview_file(fname):
        rc.srcurl = ul
    elif ft is not None and ft.startswith('image'):
        rc.imgurl = ul
    elif fsize / (1024.0 * 1024.0) >= 1.0:  # file to big
        rc.srcurl = ul
    else:
        is_binary = False
        try:
            content = svn.CAT(r)
            is_binary = is_binary_string(content[0:128])
        except:
            is_binary = True
            
        if is_binary:
            rc.srcurl = ul
        else:
            rc.mimetype = get_ext_class(fname)
            rc.content = mark_highlight(content, fname)

    return send_response(request,
                             'repos/view_file.html')

def get_logs(request, r, rev=None, limit=20):

    o = svn.LOG(r, rev, limit)

    logs = []
    
    entrys = getattr(o.log, 'logentry', [])
    if type(entrys) != list:
        entrys = [entrys]

    for e in entrys:
        log = {
            'rev':e['revision'],
            'author':get_author(getattr(e, 'author', '')),
            'date':parse_datetime(str(e.date)),
            'msg':unicode(e.msg)
        }
        logs.append(log)
    return logs
    
def log(request, name, path='/', rev=None):
    resp, r, rc = check_acl(request, name, path)
    if resp is not None:
        return resp

    o = svn.LOG(r, rev, limit= -1)
    e = o.log.logentry
    
    rc.REPOS = get_repos_base(request, name)

    rc.author = get_author(getattr(e, 'author', ''))
    rc.mtime = parse_datetime(str(e.date))
    rc.msg = unicode(e.msg)

    paths = e.paths
    if type(paths) != list:
        paths = [paths]

    cfiles = []
    for p in e.paths:
        path = {'dir':p['kind'] == 'dir' and True or False,
                'action':p['action'],
                'name':unicode(p)}
        cfiles.append(path)

    rc.cfiles = cfiles
    rc.rev = rev
    rc.content = ''
    
    """
    content = svn.DIFF(r, rev)
    if content is not None and len(content) > 0:
        rc.content = mark_highlight(content, 'uname.diff')
    """ 
    return send_response(request,
                         'repos/view_log.html')

def logs(request, name, path='/'):
    resp, r, rc = check_acl(request, name, path)
    if resp is not None:
        return resp

    rc.logs = get_logs(request, r, limit=100)
    
    return send_response(request,
                         'repos/view_logs.html')


def diff(request, name, revN, revM=None, path='/'):
    resp, r, rc = check_acl(request, name, path)
    if resp is not None:
        return resp

    content = svn.DIFF(r, revN, revM)
    rc.content = force_unicode2(content)
        
    if  revM==None:
        revM=int(revN)
        revN=revM-1
    rc.revN = revN
    rc.revM = revM
    
    rc.REPOS = get_repos_base(request, name)
    prj_q = Q(project__status=consts.PROJECT_ENABLE)

    current_user = q_get(User, name=request.user, status=consts.USER_ENABLE)
    
    owner_q = Q(owner=current_user,
                status=consts.PROJECT_ENABLE)
    
    owner_projects = Project.objects.filter(owner_q)
    
    joined_projects = q_gets(ProjectMember,
                                user=current_user).filter(prj_q).exclude(member_type=consts.PM_REJECT_INV)


    power='read'
    if current_user==rc.project.owner:
        power = 'all'
    
            
    for j in joined_projects:
        if current_user==j.user and rc.project==j.project:
            power='all'    
        
        


    rc.power = power
         
    project = q_get(Project, name=rc.project)  
    rc.project = project
    ''' 
    owner=q_get(User,name=project.owner)
    members = q_gets(ProjectMember, project = project, 
                        member_type = consts.PM_ACCEPT_INV)
    
    
    if owner==current_user:
        rc.good = 'admin'
        
    if current_user in members:
        rc.good = 'join'
    '''    

    
    update_my_project_status(request, [project])
    rs = ProjectWatcher.objects.filter(project=project).aggregate(watchers=Count('id'))
    rc.rs = rs['watchers']
    
    

    return send_response(request,
                         'repos/view_diff.html')





def handle_content(newContent):
    indexTmp = []
    leftCont = ''
    rightCont = ''

    oldStart = 0
    oldEnd = 0
    newStart = 0
    newEnd = 0
    content=[]
    for index, item in enumerate(newContent):
        if re.search('^@@', item) and re.search('@@\r$', item):
            indexTmp.append(index)
    lenIndex = len(indexTmp)

    if lenIndex > 1:
        for i, c in enumerate(indexTmp):
            if i + 1 == lenIndex:
                oneContent = newContent[indexTmp[i]:len(newContent)]
                oldStart, oldEnd, newStart, newEnd = build_line(oneContent)
                tmpOneContent = oneContent[1:len(oneContent)]
                for ii, tt in enumerate(tmpOneContent):
                    if re.search('^-', tt):
                        leftCont = leftCont + tt[1:len(tt)] + '\n'
                    elif re.search('^\+', tt):
                        rightCont = rightCont + tt[1:len(tt)] + '\n'
                    elif not re.search('^-', tt) and not re.search('^\+', tt):
                        leftCont = leftCont + tt + '\n'
                        rightCont = rightCont + tt + '\n'
                leftCont=  force_unicode2(leftCont)  
                rightCont = force_unicode2(rightCont)
                cc=({'oldStart':oldStart, 'oldEnd':oldEnd, 'newStart':newStart, 'newEnd':newEnd, 'leftCont':leftCont, 'rightCont':rightCont})
                    
                content.append({'content':cc})
                rightCont=''
                leftCont=''
                    
            else:
                oneContent = newContent[indexTmp[i]:indexTmp[i+1]]  
                oldStart, oldEnd, newStart, newEnd = build_line(oneContent)
                tmpOneContent = oneContent[1:len(oneContent)]
                for ii, tt in enumerate(tmpOneContent):
                    if re.search('^-', tt):
                        leftCont = leftCont + tt[1:len(tt)] + '\n'
                    elif re.search('^\+', tt):
                        rightCont = rightCont + tt[1:len(tt)] + '\n'
                    elif not re.search('^-', tt) and not re.search('^\+', tt):
                        leftCont = leftCont + tt + '\n'
                        rightCont = rightCont + tt + '\n'
                leftCont=  force_unicode2(leftCont)  
                rightCont = force_unicode2(rightCont)    
                cc=({'oldStart':oldStart, 'oldEnd':oldEnd, 'newStart':newStart, 'newEnd':newEnd, 'leftCont':leftCont, 'rightCont':rightCont})
                    
                content.append({'content':cc})
                rightCont=''
                leftCont=''
                        
    else:
        oneContent = newContent[indexTmp[0]:len(newContent)]
        oldStart, oldEnd, newStart, newEnd = build_line(oneContent)
        tmpOneContent = oneContent[1:len(oneContent)]
        for ii, tt in enumerate(tmpOneContent):
            if re.search('^-', tt):
                leftCont = leftCont + tt[1:len(tt)] + '\n'
            elif re.search('^\+', tt):
                rightCont = rightCont + tt[1:len(tt)] + '\n'
            elif not re.search('^-', tt) and not re.search('^\+', tt):
                leftCont = leftCont + tt + '\n'
                rightCont = rightCont + tt + '\n'
        leftCont=  force_unicode2(leftCont)  
        rightCont = force_unicode2(rightCont) 
        cc=({'oldStart':oldStart, 'oldEnd':oldEnd, 'newStart':newStart, 'newEnd':newEnd, 'leftCont':leftCont, 'rightCont':rightCont})
                    
        content.append({'content':cc})   
        rightCont=''
        leftCont=''

        
    return content



def build_line(oneContent):
    tmpOne = oneContent[0].split(" ")
   
    if re.search('^\,',tmpOne[1]):
        oldStart = int(tmpOne[1][1:tmpOne[1].index(',')])
        tmp1 = int(tmpOne[1][tmpOne[1].index(',') + 1:len(tmpOne[1])])
        oldEnd = oldStart + tmp1
    else:
        oldEnd=tmpOne[1]
        oldStart=tmpOne[1]
    
  
    
    
    if re.search('^\,',tmpOne[2]):
        newStart = int(tmpOne[2][1:tmpOne[2].index(',')])
        tmp2 = int(tmpOne[2][tmpOne[2].index(',') + 1:len(tmpOne[2])])
        newEnd = newStart + tmp2
    else:
        newStart=tmpOne[2]
        newEnd=tmpOne[2]

    
    return oldStart, oldEnd, newStart, newEnd
    

def rsvn_add(request, name):
    svn.init_local_repos(name)
    return send_json_response("OK")

def rsvn_del(request, name):
    svn.del_local_repos(name)
    return send_json_response("OK")
