# -*- coding: utf-8 -*-
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
from django.utils.translation import gettext

from taocode2.helper import consts

from taocode2.models import *
from taocode2.apps.user.forms import *
from taocode2.apps.user.verify import new_change_email_task

from taocode2.helper.utils import *
from taocode2.helper.page import build_page
from taocode2.settings import SITE_ROOT
from taocode2.apps.user.activity import get_user_activitys
from django.conf import settings
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth import authenticate, REDIRECT_FIELD_NAME
from django.http import *

from django.contrib.auth.decorators import login_required
#from django.contrib.auth.forms import AuthenticationForm

from django.forms import ValidationError

from django.db.models import Count,Q
from django.core.urlresolvers import reverse
from django.core.validators import slug_re, email_re

from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect

import urlparse

import os  

import Cookie  
import datetime  
import random  


__author__ = 'luqi@taobao.com'


def update_project(request, projects):
     for project in projects:
        project.watcher_count = q_gets(ProjectWatcher, project = project, 
                                       user__status = consts.USER_ENABLE).aggregate(watchers = Count('id'))['watchers']
                                    
    
    

def fast_register(request):
    rc = request.rc 
    rc.report=q_get(ProjectReport,id=9999)

    if request.user.is_authenticated():
        view_user(request=request,name=request.user)
         
    rc.pagename = "Create your account."
     
    if "_taocode" in request.COOKIES:
        rc.form = AuthenticationForm(request)
        return send_response(request, 'user/login.html')

    if request.method != 'POST':
        rc.form = NewUserFastForm()
        return send_response(request, 'index.html')
    
    form = NewUserFastForm(request.POST)
    if form.is_valid() is False:
        rc.form = form
        return send_response(request, 'index.html')

    cd = form.cleaned_data
    
    user = form.save(commit=False)
    user.set_password(cd['password'])
    user.status = consts.USER_ENABLE
    user.sex = consts.USER_UNKNOWN
    #user.pic = consts.DEFAULT_PIC
    user.last_login_ip = request.META.get('HTTP_X_REAL_IP','0.0.0.0')

    user.save()
    
    auser = authenticate(username=cd['name'], password=cd['password'])
    if auser is not None and auser.is_active:
        auth_login(request, auser)
        
        
    return redirect(reverse('apps.user.views.view_user', args=[]))


def build_user_nav_menu(choice = None):
    uri = '/my/'

   # navmenus = [{'uri': '/my', 'txt':'My'},
   #             {'uri': '/my/edit', 'txt':'Change profile'},
   #             {'uri': '/my/newpwd', 'txt':'Change Password'}]
     
    profilenavmenus = [{'uri': '/my/edit', 'txt':'基本信息'},
                #{'uri': '/my/social', 'txt':'社交网络'},
                {'uri': '/my/newpwd', 'txt':'修改密码'}]

    if choice is None:
        profilenavmenus[0]['choice'] = True
    else:
        for m in profilenavmenus:
            if m['uri'].endswith(choice):
                m['choice'] = True
    return profilenavmenus


def build_user_body_menu(pt):
    bodymenus = [{'uri':'/worklogs/', 'text':'worklogs'},
                 {'uri':'/watpro/', 'text':'watpro'},
                 {'uri':'/mypro/', 'text':'mypro'}
                ]

    for v in  bodymenus:
        if v['uri'].find(pt) != -1:
            v['choice'] = True
            break

    return bodymenus

def login_view(request):
    
    rc = request.rc 

    rc.report=q_get(ProjectReport,id=9999)
    redirect_to = request.REQUEST.get("next", '')

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            netloc = urlparse.urlparse(redirect_to)[1]

            # Use default setting if redirect_to is empty
            if not redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL

            # Security check -- don't allow redirection to a different
            # host.
            elif netloc and netloc != request.get_host():
                redirect_to = settings.LOGIN_REDIRECT_URL

            # Okay, security checks complete. Log the user in.
            auth_login(request, form.get_user())

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
                
            if request.POST.get('remember', None) is not None:
                request.session.set_expiry(604800)# 7* 24*3600
                    
            return redirect(redirect_to)
    else:
        form = AuthenticationForm(request)

    request.session.set_test_cookie()

    #rc = request.rc

    rc.form = form
    rc.next = redirect_to

    return send_response(request, 'user/login.html')


def logout_view(request):
    auth_logout(request)
    redirect_to = request.REQUEST.get('next', '')

    if redirect_to:
        netloc = urlparse.urlparse(redirect_to)[1]
        # Security check -- don't allow redirection to a different host.
        if not (netloc and netloc != request.get_host()):
            return redirect(redirect_to)
        
    return fast_register(request)

def register(request):
    rc = request.rc
    rc.pagename = "Create your account."
    if request.method != 'POST':
        rc.form = NewUserForm()
        
        return send_response(request, 'user/register.html')
    
    form = NewUserForm(request.POST)
    if form.is_valid() is False:
        rc.form = form
        
        return send_response(request, 'user/register.html')

    cd = form.cleaned_data
    
    user = form.save(commit=False)
    user.set_password(cd['password_0'])
    user.status = consts.USER_ENABLE
    user.sex = consts.USER_UNKNOWN
    #user.pic = consts.DEFAULT_PIC
    user.last_login_ip = request.META.get('HTTP_X_REAL_IP', '0.0.0.0')

    user.save()
    
    auser = authenticate(username=cd['name'], password=cd['password_0'])
    if auser is not None and auser.is_active:
        auth_login(request, auser)
        
    return redirect(reverse('apps.user.views.view_user', args=[]))

def view_user(request,pt='mypro', name=None):    
    rc = request.rc
    rc.bodymenus = build_user_body_menu(pt)
    if name is None:
        
        if request.user.is_authenticated():
            name = request.user.name
        else:
            raise Http404
    rc.user=request.user   
    rc.current_user = q_get(User, name=name, status=consts.USER_ENABLE)


    if rc.current_user is None:
        raise Http404


    prj_q = Q(project__status = consts.PROJECT_ENABLE)

    owner_q = Q(owner = rc.current_user, 
                status = consts.PROJECT_ENABLE)
    
    public_q = Q(is_public = True)

    if rc.user != rc.current_user:
         owner_q = Q(owner_q, public_q)
             
    rc.pagename = rc.current_user.name

    rc.owner_projects = Project.objects.filter(owner_q)

    rc.joined_projects=q_gets(ProjectMember, 
                              user = rc.current_user).filter(prj_q).exclude(member_type=consts.PM_REJECT_INV)
  
                                
    watch_projects = q_gets(ProjectWatcher, 
                            user = rc.current_user).filter(prj_q)

    for p in watch_projects:
        p.watcher_count=q_gets(ProjectWatcher, project = p.project,
                                       user__status = consts.USER_ENABLE).aggregate(watchers = Count( 'id'))[ 'watchers']
        
    rc.watch_projects=watch_projects
    
    rc.follows = q_gets(UserWatcher, 
                        user = rc.current_user, 
                        target__status = consts.USER_ENABLE)
    
    rc.fans = q_gets(UserWatcher, 
                     target = rc.current_user, 
                     user__status = consts.USER_ENABLE)

    rc.logs = get_user_activitys(rc.current_user, request, 20)
    
    if pt=='mypro':       
        rc.current_page='mypro'    
            
    if pt=='watpro':
        rc.current_page='watpro'  
    
    if pt=='worklogs':
        rc.current_page='worklogs'

    return send_response(request, 'user/view.html')

@login_required
def edit_my(request):
    rc = request.rc
    rc.pagename = "Change profile"
    rc.profilenavmenus = build_user_nav_menu('edit')

    
    return send_response(request, 'user/edit_my.html')

@login_required
def edit_notify(request):
    rc = request.rc
    rc.pagename = "Change notify"

    uri = request.META['PATH_INFO']

    return send_response(request, 'user/edit_notify.html')


@as_json
@login_required
def do_edit_my(request):
    e = request.POST.get('email', '').strip()
    if len(e) > 3:
         user = User.objects.get(name=request.user.name)
         user.email = e
         user.signature=request.POST['signature']
         user.save()

    return redirect(reverse('apps.user.views.view_user', args=[]))
    
@as_json
@login_required
def do_edit_email(request):
    if request.method != 'POST':
        return False
    
    e = request.POST.get('e', '').strip()
    if len(e) <= 0 or e == request.user.email:
        return False

    if not email_re.search(e):
        return False
     
    new_change_email_task(request.user, e)
    #
    #
    return True


@as_json
@login_required
def watch_user(request, name):
    target = q_get(User, name=name, status=consts.USER_ENABLE)
    if target is None:
        return False

    uw = q_get(UserWatcher, target=target, user=request.user)
    
    if uw is None:
        uw = UserWatcher(user = request.user,
                         target = target)
        uw.save()
        result_text = 'unfollow'
    else:
        uw.delete()
        result_text = 'follow'

    rs = UserWatcher.objects.filter(target = target).aggregate(watchers = Count('id'))

    return (True, (result_text, rs['watchers']))

@as_json
def check_name(request, name):
    target = q_get(User, name=name)
    if target is None:
        return True
    return False

@as_json
def check_email(request, email):
    target = q_get(User, email=email)
    if target is None:
        return True
    return False

@as_json
def check_email_auth(request):
    if request.method=='POST':
        email=request.POST.get('email')
        pwd=request.POST.get('pwd')
        target = q_get(User, email=email)

        if target is None:
            return (False,gettext('Email Not Exist'))

        return target.password == secpwd(pwd)
    else:
        return (False,gettext('InValid Request'))

@as_json
def check_name_auth(request):
    if request.method=='POST':
        name=request.POST.get('name')
        pwd=request.POST.get('pwd')
        target = q_get(User, name=name)

        if target is None:
            return (False,gettext('Name Not Exist'))

        return target.password == secpwd(pwd)
    else:
        return (False,gettext('InValid Request'))
