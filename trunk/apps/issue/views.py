# -*- coding: utf-8 -*-
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

from django.utils.translation.trans_real import gettext
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.http import *
from django.utils.html import escape
from django.db.models import Count

from taocode2.models import *
from taocode2.helper.utils import *

from taocode2.helper import consts
from taocode2.helper.page import build_page
from taocode2.settings import SITE_ROOT
from taocode2.apps.project.views import update_my_project_status, build_prj_nav_menu
from taocode2.apps.project.admin import can_access
from taocode2.apps.project import prj_key
from taocode2.apps.main.files import add_file

from taocode2.apps.user import activity
from django.db.models import Q

from taocode2.apps.message.views import *

__author__ = 'luqi@taobao.com'


def all_issues(request, name, pagenum=1, key=None):
    if request.method == 'POST':
        pagenum =request.POST.get('jump', None)
   
    return query_issues(request, name,
                        pagenum, key)

def list_issues(request, name, status, pagenum=1, key=None):
    st = None
    if status == 'opened':
        st = consts.ISSUE_OPEN
    elif status == 'closed':
        st = consts.ISSUE_CLOSED
        
    return query_issues(request, name,
                        pagenum, key,
                        st)

def query_issues(request, name, pagenum, key, st=None):
    rc = request.rc
    project = q_get(Project, name=name)

    if project is None:
        raise Http404

    rc.navmenusSource = build_prj_nav_menu(request, project, 'issues')

    rc.bodymenus = [{'uri':'issues/', 'text':'all','class':'p-p-project-btn all'},
                    {'uri':'issues/opened/', 'text':'opened','class':'tosolve'},
                    {'uri':'issues/closed/', 'text':'closed','class':'solve'}]
    
    prefix = 'issues'

    if st == consts.ISSUE_OPEN:
        rc.pagename = "Opened issues"
        prefix += '/opened'
        rc.bodymenus[1]['choice'] = True
        rc.currentMenu='opened'
    elif st == consts.ISSUE_CLOSED:
        rc.pagename = "Closed issues"
        prefix += '/closed'
        rc.bodymenus[2]['choice'] = True
        rc.currentMenu='closed'
    else:
        rc.pagename = "All issues"
        rc.bodymenus[0]['choice'] = True    
        rc.currentMenu='all'    
    #if request.method == 'POST':
       # q = request.POST.get('q', None)
       # return redirect(SITE_ROOT + '/p/%s/%s/1/%s'%(name, prefix, q))

    resp = can_access(project, request.user)
    if resp != None:
        return resp

    rc.project_name = name
    rc.project = project

    update_my_project_status(request,[rc.project])

    if project is None:
        return send_response(request, 
                             'project/notfound.html')
    pagenum = int(pagenum)

    if key is not None:
        q = Q(Q(project=project), Q(Q(title__icontains=key) | Q(content__icontains=key)))
    else:
        q = Q(project=project)

    if st is not None:
        q = q & Q(status = st)

    q = q & ~Q(status = consts.ISSUE_DELETED)
    key_text = key and key.encode('utf8') or ''

    build_page(rc, Issue, q,
               pagenum,
               '/p/{0}/{1}'.format(name, prefix),
               key_text,
               order=['-mtime'])

    for i in rc.page.object_list:
        if request.user in (project.owner, i.creator):
            i.can_op = True
        else:
            i.can_op = False

        i.comments_count = IssueComment.objects.filter(issue=i,status=consts.COMMENT_ENABLE).count();

    rc.key_text = key_text
    return send_response(request, 
                         'issue/list.html')

def view_issue(request, name, issue_id):
    rc = request.rc
    rc.project = q_get(Project, name = name)

    resp = can_access(rc.project, request.user)
    if resp != None:
        return resp

    issue = q_get(Issue, pk = issue_id)

    if issue.status == consts.ISSUE_DELETED:
        raise Http404
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content is not None:
            comment = IssueComment()
            comment.issue = issue
            comment.owner = request.user
            comment.content = content
            comment.status = consts.COMMENT_ENABLE
    
            comment.save()
            activity.new_comment(issue.project, request.user, comment)
            
            return redirect(reverse('apps.issue.views.view_issue', 
                                    args=[name, issue.id]))
            
            
    rc.issue = issue
    rc.pagename = '#%s - %s'%(rc.issue.id, rc.issue.title)
    rc.navmenusSource = build_prj_nav_menu(request, rc.project, 'issues')

    rc.comments = q_gets(IssueComment, issue=rc.issue, 
                         status = consts.COMMENT_ENABLE).order_by('ctime')

    rc.files = q_gets(ProjectAttachment, project=rc.project,
                      ftype='issue', ftid=rc.issue.id,
                      status = consts.FILE_ENABLE)

    projectmember=q_gets(ProjectMember,project=rc.project)

    rc.issueowner = request.user in (rc.issue.creator,
                                     rc.project.owner)

    rc.commowner=False    
    if request.user == rc.project.owner:
        rc.commowner=True
        
    for m in projectmember:
        if request.user == m.user:
             rc.issueowner =True
             rc.commowner=True
    
    return send_response(request, 
                         'issue/view.html')

@login_required
def new_issue(request, name):
    rc = request.rc
    project = q_get(Project, name = name)

    resp = can_access(project, request.user)
    if resp != None:
        return resp

    rc.project = project
    rc.pagename = 'create issue'
    rc.navmenusSource = build_prj_nav_menu(request, rc.project, 'issues')

    if request.method != 'POST':
        return send_response(request, 
                         'issue/new.html')
    
    title = request.POST.get('title', '')
    content = request.POST.get('content', '')
    
    if len(title) <= 0:
        return send_response(request, 
                             'issue/new.html')
    
    if len(content) <= 0:
        return send_response(request, 
                             'issue/new.html')
    
    issue = Issue()
    issue.project = rc.project
    
    issue.creator = request.user

    issue.title = title
    issue.content = content
    issue.status = consts.ISSUE_OPEN
    issue.vote_count = 0
    
    issue.save()

    #admin = q_get(User, name='taocodeadmin')

    
    
    admin = q_get(User, name=request.user)
    
    project=q_get(Project,name=rc.project)

    owner=q_get(User,name=project.owner)
    

    content = "System message: The project "+ rc.project.name+" have an issue . http://code.taobao.org/p/"+project.name+"/issues/ . Please check it."
    send_newissuemsg(request,owner,admin,content)
    
    members = q_gets(ProjectMember, project = project, 
                        member_type = consts.PM_ACCEPT_INV)
    
    for m in members:
        send_newissuemsg(request,m.user,admin,content)

    # add file
    atts = request.FILES.getlist('attachment')
    fc = 0
    for f in atts:
        if fc <= prj_key.get(project, prj_key.UPLOAD_LIMIT_COUNT, 5):
            add_file(request, project, 'issue', issue.id, f)
            fc += 1

    activity.new_issue(rc.project, request.user, issue)

    return redirect(reverse('apps.issue.views.view_issue', 
                            args=[name, issue.id]))
