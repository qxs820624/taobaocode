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

from taocode2.models import *
from taocode2.helper import consts
from django.db.models import Q,Count, Sum
from django.views.static import serve

from taocode2.helper.page import build_page
from taocode2.settings import SITE_ROOT
from taocode2.apps.project.views import update_my_project_status

from taocode2.apps.user.activity import get_user_activitys
from taocode2.helper.utils import *
from django.core.cache import cache
from random import randint
from django.http import *

try:
    from taocode2.private_setting import *
except ImportError:
    pass

__author__ = 'luqi@taobao.com'


def index(request):
    rc =  request.rc

    ev = cache.get('index_cache')

    if ev is None:
        rc.new_projects = Project.objects.filter(status=consts.PROJECT_ENABLE,
                                                 is_public=True).order_by('-ctime')[:6]

        #hps = Activity.objects.filter(project__status=consts.PROJECT_ENABLE,
        #                              project__is_public=True).values('project').annotate(pc = Count("project")).order_by('-pc')[:6]

        #rc.hot_projects = sort_models(Project, hps, 
        #                              'project', 'pc')

        #aus = Activity.objects.filter(user__status=consts.USER_ENABLE,
        #                              project__status=consts.PROJECT_ENABLE,
        #                              project__is_public=True).values('user').annotate(uc = Count("user")).order_by('-uc')[:10]

        #rc.ausers = sort_models(User, aus, 
        #                        'user', 'uc')
        
        rc.feature_prjs = FeatureProject.objects.all().order_by('-mtime')[:5]
        rc.logs = get_user_activitys(None, request, 10, False)
        ev = {}
        ev['new_projects'] = rc.new_projects
        ev['hot_projects'] = rc.hot_projects
        ev['ausers'] = rc.ausers 
        
        ev['feature_prjs'] = rc.feature_prjs
        ev['logs'] = rc.logs

        cache.set('index_cache', ev, 60) #60secs

    rc.new_projects = ev['new_projects']
    rc.hot_projects = ev['hot_projects']
    rc.ausers = ev['ausers']
    
    rc.feature_prjs = ev['feature_prjs']
    rc.logs = ev['logs']

    prj_count = Project.objects.filter(status = consts.PROJECT_ENABLE,
                                       is_public=True).count()
    pos = randint(0,prj_count)
    random_prjs = Project.objects.filter(status = consts.PROJECT_ENABLE,
                                         is_public=True)[pos:pos+10]

    rc.random0_projects = random_prjs[:5]
    rc.random1_projects = random_prjs[5:]
    
    if "taocode" in request.COOKIES:
        c=request.COOKIES['taocode']
    
    return send_response(request, 'index.html')

def show_page(request, name, pagename=''):
    request.rc.pagename = pagename
    return send_response(request, name)

def search(request, pagenum=1,type='user', key=None):
    
    rc = request.rc
    rc.t=type
    ptype='Project'
    if request.method == 'POST' and request.POST.get('jump') is not None:
        pagenum =request.POST.get('jump')


    else:
        if request.method == 'POST':
            qq = request.POST.get('q', None)
            type = request.POST.get('type', None)

            return redirect(SITE_ROOT + '/search/' + type + '/1/'+qq )
    
       
    pagenum = int(pagenum)

    if type == 'user':
        ptype='User'
        if key is not None:
            q = Q(name__icontains=key)
        else:
            rc.ptype='error'

            return send_response(request, 
                         'main/search.html')
        
    elif type == 'project':
        if key is not None:
            q = Q(name__icontains=key) | Q(title__icontains=key)
        else:
            q = Q()
        q = q & Q(status = consts.PROJECT_ENABLE, is_public=True)
      
    elif type == 'language':
        if key is not None:
            q = Q(language__icontains=key)
        else:
            q = Q()
        q = q & Q(status = consts.PROJECT_ENABLE, is_public=True)
            

    tmpkey =  key
    key_text = tmpkey and tmpkey.encode('utf8') or ''

    key = key and key.encode('utf8') or ''
    if type == 'user':
        build_page(rc, User, q,
                   pagenum, 
                   '/search/user',
                   key_text, order=['-ctime'],page_count=40)
        rc.users=rc.page.object_list
        
    else: 
        build_page(rc, Project, q,
                   pagenum, 
                   '/search/{0}'.format(type),
                   key_text, order=['-ctime'])

        update_my_project_status(request, 
                                 rc.page.object_list)
    
        rc.all_projects = True
        rc.prjs = rc.page.object_list
        
    if len(rc.page.object_list)<=0:
        ptype="nothing"
        
    
    rc.key = key
    
    rc.ptype=ptype
        
    return send_response(request, 
                         'main/search.html')

def opensources_list(request, pagenum=1,key=None):
    rc = request.rc
    pagenum=int(pagenum)
    key = None
    
    if request.method == 'POST':
        pagenum = int(request.POST.get('jump', pagenum))
        key = request.POST.get('q', None)
        
    if key is not None:
        q = Q(subject__icontains=key)
    else:
        q = Q()   
    
    key_text = key and key.encode('utf8') or ''

    build_page(rc, AliProject, q,
               pagenum, 
               '/opensources',
               key_text, 
               order=['-ctime'])
    for prj in rc.page.object_list:
        prj.users = [u.name for u in AliProjectUser.objects.filter(project = prj)]
        
    rc.projectCount= len(AliProject.objects.all())
    rc.peopleCount= AliProjectUser.objects.values('name').distinct().count()
    rc.opensources=rc.page.object_list
    rc.key_text = key_text

    return send_response(request,'main/opensources.html')
