urls = []

"""
import sys
from decimal import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.forms import ValidationError
from django.http import *
from django.db.models import Q, Count,Sum
from django.core.cache import cache
from django.utils.translation import ugettext as _
from django.utils.http import urlquote

from taocode2.models import *
from taocode2.helper.utils import *

from taocode2.helper import consts
from taocode2.helper.page import build_page
from taocode2.settings import SITE_ROOT
from taocode2.apps.user.activity import get_prj_activitys
from taocode2.apps.user.activity import get_user_recent_activities

from taocode2.apps.project.forms import NewProjectForm
from taocode2.apps.project.admin import can_access, build_prj_nav_menu
from taocode2.apps.user import activity
from taocode2.apps.repos import svn

from random import randint
import datetime

__author__ = ['luqi@taobao.com',
              'canjian@taobao.com']

def update_my_project_status(request, projects):
    if request.user.is_authenticated() is False:
        return

    for project in projects:
        project.member_count = q_gets(ProjectMember, project = project, 
                                      user__status = consts.USER_ENABLE).aggregate(members = Count('id'))['members']
        project.watcher_count = q_gets(ProjectWatcher, project = project, 
                                       user__status = consts.USER_ENABLE).aggregate(watchers = Count('id'))['watchers']

        if project.owner == request.user:
            project.my_status = consts.MY_PROJECT_OWNER
        else:
            pm = q_get(ProjectMember, project=project, user=request.user)
            if pm is not None and pm.member_type == consts.PM_ACCEPT_INV:
                project.my_status = consts.MY_PROJECT_MEMBER
                continue
            pw = q_get(ProjectWatcher, project=project, user=request.user)
            if pw is not None:
                project.my_status = consts.MY_PROJECT_WATCH
                continue
            project.my_status = consts.MY_PROJECT_NONE

def build_body_nav_menu(pt):
    bodymenus = [{'uri':'/all/', 'text':'All'},
                 {'uri':'/hot/', 'text':'Most hot'},
                 {'uri':'/newest/', 'text':'Newest'},
                 {'uri':'/random/', 'text':'Random'},
                 {'uri':'/committimes/', 'text':'committimes'},
                 {'uri':'/downloadtimes/', 'text':'downloadtimes'},
                 {'uri':'/issuetimes/', 'text':'issuetimes'},
                 {'uri':'/watched/', 'text':'Popular Watched'}]
    
    for v in  bodymenus:
        if v['uri'].find(pt) != -1:
            v['choice'] = True
            break
    return bodymenus

def all_projects(request, pagenum=1, key=None):
    rc = request.rc
    rc.pagename = 'Projects'
    rc.bodymenus = build_body_nav_menu('all')
    
    pagenum = int(pagenum)
    if request.method == 'POST':
        q = request.POST.get('q', None)
        return redirect(SITE_ROOT + '/all/1/'+q)

    #
    # get project 
    #
    if key is not None:
        q = Q(name__icontains=key) | Q(title__icontains=key)
    else:
        q = Q()

    q = q & Q(status = consts.PROJECT_ENABLE, is_public=1)
    key_text = key and key.encode('utf8') or ''


    build_page(rc, Project, q,
               pagenum, '/all', key_text, order=['-ctime'])

    update_my_project_status(request, 
                             rc.page.object_list)
    
    rc.all_projects = True
    rc.prjs = rc.page.object_list
    rc.key_text = key_text
    return send_response(request, 
                         'project/list.html')


def list_projects(request, pt, pagenum=1):
    rc = request.rc
    rc.pagename = 'Projects'
    rc.bodymenus = build_body_nav_menu(pt)
    if request.method=='POST':
        pagenum=int(request.POST.get('jump'))

    q = Q(status = consts.PROJECT_ENABLE, is_public=1, )
    od = []
    totals=0
    if pt == 'hot':
        rc.current_page = "hot"
        pn = int(pagenum)
        if pn <= 0:
          pn = 1
        pos = consts.PAGE_SIZE * (pn - 1)
        
        ps = Project.objects.filter(status = consts.PROJECT_ENABLE,
                                      is_public=1).values("id").annotate(uc=Sum('click')).filter(uc__gt=0).order_by('-uc')[pos:pos + 50]
        totals = total_models(Project, ps, 
                           'id', 'uc')
        
        prjs = sort_models(Project, ps, 
                           'id', 'uc')
        prjsgraph = build_project_graph(Project,ps,'id', 'uc',totals,_("total_visit_times"))
        
    
    elif pt == 'newest':
        rc.current_page = "newest"
        pn = int(pagenum)
        if pn <= 0:
          pn = 1
        pos = consts.PAGE_SIZE * (pn - 1)
        
        prjs = Project.objects.filter(status = consts.PROJECT_ENABLE,
                                      is_public=1).order_by('-ctime')[pos:pos + 50]

        update_my_project_status(request, prjs)
        key=None
        q = q & Q(status = consts.PROJECT_ENABLE, is_public=1)
        key_text = key and key.encode('utf8') or ''


        build_page(rc, Project, q,pagenum, '/newest', key_text,page_count=consts.PAGE_SIZE, order=['-ctime'])

        rc.prjs = prjs
        return send_response(request,'project/list.html')
    elif pt == 'random':
        prj_count = Project.objects.filter(status = consts.PROJECT_ENABLE,
                                           is_public=1).count()
        
        pos = randint(0,prj_count)
        
        prjs = Project.objects.filter(status = consts.PROJECT_ENABLE,
                                      is_public=1)[pos:pos+10]
    elif pt == 'watched':
        rc.current_page="watched"
        pn = int(pagenum)
        if pn <= 0:
          pn = 1
        pos = consts.PAGE_SIZE * (pn - 1)
        
        ps = ProjectWatcher.objects.filter(project__is_public=1).values("project").annotate(uc=Count('user')).filter(uc__gt=0).order_by('-uc')[pos:pos + 50]
        totals = total_models(Project, ps, 
                           'project', 'uc')
        
        prjs = Project.objects.filter(pk__in = [h['project'] for h in ps])
        prjsgraph = build_project_graph(Project,ps,'project', 'uc',totals,_("total_watched_times"))
    elif pt == 'issuetimes':
        rc.current_page="issuetimes"
        pn = int(pagenum)
        if pn <= 0:
          pn = 1
        pos = consts.PAGE_SIZE * (pn - 1)
        
        ps = Issue.objects.filter(project__is_public=1).values("project").annotate(uc=Count("title")).filter(uc__gt=0).order_by('-uc')[pos:pos + 50]
        totals = total_models(Project, ps, 
                           'project', 'uc') 
                                    
        prjs = Project.objects.filter(pk__in = [h['project'] for h in ps])
        prjsgraph = build_project_graph(Project,ps,'project', 'uc',totals,_("total_issue_times"))
    elif pt == 'committimes':
        rc.current_page="committimes"
        pn = int(pagenum)
        if pn <= 0:
          pn = 1
        pos = consts.PAGE_SIZE * (pn - 1)
        
        ps = Activity.objects.filter(project__is_public=1,act_type='new_commit').values("project").annotate(uc=Count('user')).filter(uc__gt=0).order_by("-uc")[pos:pos + 50]
        totals = total_models(Project, ps, 
                           'project', 'uc') 
                                    
        prjs = Project.objects.filter(pk__in = [h['project'] for h in ps])
        prjsgraph = build_project_graph(Project,ps,'project', 'uc',totals,_("total_submit_times"))
    elif pt == 'downloadtimes':
        rc.current_page="downloadtimes"
        pn = int(pagenum)
        if pn <= 0:
          pn = 1
        pos = consts.PAGE_SIZE * (pn - 1)
        ps = ProjectReport.objects.filter(project__status = consts.PROJECT_ENABLE, 
                                           project__is_public=1).values('project')\
                                           .annotate(uc=Sum('download_times'))[pos:pos + 50]
        totals = total_models(Project, ps, 
                           'project', 'uc') 
                                   
        prjs = Project.objects.filter(pk__in = [h['project'] for h in ps])
        prjsgraph = build_project_graph(Project,ps,'project', 'uc',totals,_("total_download_times"))

    update_my_project_status(request, prjs)
    
    

    rc.prjs = prjs
    rc.prjsgraph=prjsgraph
    return send_response(request, 
                         'project/projectGraph.html')

def view_project(request, name):
    return redirect(reverse('apps.repos.views.browse', args=[name]))

def project_info(request, name,pagenum=1,key=None):
    if request.method == 'POST':
        pagenum =request.POST.get('jump', None)
    
    pagenum = int(pagenum)
    
    project = q_get(Project, name=name)

    resp = can_access(project, request.user)
    if resp != None:
        return resp
    
    rc = request.rc
    rc.pagename = 'Info'
    rc.project = project
    rc.logs =get_prj_activitys(project)

    rc.members = q_gets(ProjectMember, project = project, 
                        member_type = consts.PM_ACCEPT_INV)

    update_my_project_status(request, [project])

    rc.navmenusSource = build_prj_nav_menu(request, project, 'info')

    rc.REPOS = svn.REPOS(project.part, name, '/trunk')
    
    q = Q(project=project)
    
    build_page(rc, Activity, q,
           pagenum,
           '/p/{0}/{1}'.format(name, 'info'),
           order=['-ctime'],
           )
    cc=[]
    for i in rc.page.object_list:
        if i.act_type=='new_commit':
            cc=i.content.split(' ')
            rev=cc[0]
            tmp=cc[1:len(cc)]
            msg=' '.join(tmp)
            i.commit={'rev':int(rev),'msg':msg}

    return send_response(request, 'project/view.html')

@login_required
def new_project(request):
    rc = request.rc
    rc.licenses = map(lambda x:x[0], consts.LICENSES)
    rc.langs = map(lambda x:x, consts.LANGS)
    rc.pagename = "Create project."
    rc.pagedesc = "Don't Repeat Yourself (DRY)"
    if request.method == "POST":
        is_public=int(request.POST.get("public",'1'))
        #license=request.POST.get("license",'')
        language=request.POST.get("language",'')
    if request.method != 'POST':
        rc.form = NewProjectForm()
        return send_response(request, 'project/new.html')
    
    form = NewProjectForm(request.POST)
    if form.is_valid() is False:
        rc.form = form
        return send_response(request, 'project/new.html')

    cd = form.cleaned_data

    prj_name = cd['name']

    parts = ReposPart.objects.filter(can_new=True).order_by('count')
    if len(parts) <= 0:
        # not available part
        log_error(request, 'not available parts!')
        rc.form = form
        return send_response(request, 'project/new.html')

    part = parts[0]

    result, reason = svn.rinit_repos(part, prj_name)
    if not result:
        log_error(request, reason)
        rc.form = form
        return send_response(request, 'project/new.html')

    project = form.save(commit=False)

    project.owner = request.user
    project.status = consts.PROJECT_ENABLE
    project.name = prj_name
    project.is_public=bool(is_public)
    #project.license=license
    project.language=language
    project.part = part
    project.save()

    part.count += 1
    part.save()

    activity.new_prj(project, request.user)
    
    return redirect(reverse('apps.project.views.view_project', args=[project.name]))

def project_watch_list(request, name):
    return send_response(request, 'project/watch_list.html')


@as_json
@login_required
def watch_project(request, name):
    project = q_get(Project, name=name)

    resp = can_access(project, request.user)
    if resp != None:
        return False

    pw = q_get(ProjectWatcher, project=project, user=request.user)
    
    if pw is None:
        pw = ProjectWatcher(user = request.user,
                            project = project)
        pw.save()
        activity.watch_prj(project, request.user)
        result_text = 'unwatch'
    else:
        pw.delete()
        result_text = 'watch'

    rs = ProjectWatcher.objects.filter(project = project).aggregate(watchers = Count('id'))

    return (True, (rs['watchers'], rs['watchers']))


def view_old(request, pid):
    prj = q_get(OldProject, oldid=int(pid))
    if prj is None:
        return redirect(reverse('apps.project.views.all_projects', args=[]))
    
    return redirect(reverse('apps.project.views.view_project', args=[prj.name]))

def view_old_src(request, pid):
    prj = q_get(OldProject, oldid=int(pid))
    if prj is None:
        return redirect(reverse('apps.project.views.all_projects', args=[]))
    
    return redirect(reverse('apps.repos.views.browse', args=[prj.name]))

def view_old_wiki(request, name, path):
    if path == 'ZhWikiStart':
        path = 'index'
    return redirect(reverse('apps.wiki.views.wiki_content', args=[name, path]))


# #language
def lang_view(request):
    rc = request.rc      
    rc.current_page = "language"
    rc.langs_distribution = lang_distribution(10)
    rc.langs = consts.LANGS
    return send_response(request, 'project/lang-view.html')

@as_json
def ajax_lang_view(request):
    langs_distribution = lang_distribution(10)
    return langs_distribution

def lang_distribution(top_n=10):
    cacheName = 'langs_distribution_cache' + str(top_n)
    lang_distribution = cache.get(cacheName)
    ##lang_distribution = None
    if lang_distribution is None:      
        lang_set = Project.objects.values('language').annotate(lang_ct=Count('id')).order_by('-lang_ct')
        lang_num = {}
        for ln in lang_set:
            lang_num[ln['language']] = ln['lang_ct'] 
        lang_distribution = cpu_lang_distribution(lang_num, top_n)
        
        other = Decimal('100.0')
        for lang in lang_distribution:
            other  = other - lang[1]
        
        if other >  Decimal('0.0'):
            lang_distribution.append(['Other', other])

        cache.set(cacheName, lang_distribution, 60 * 60)  # 60*60secs 

    return lang_distribution


def cpu_lang_distribution(lang_num, top_n=10):  
    proj_sum = sum(lang_num.values())
    sorted_lang_num = sorted(lang_num.iteritems(), key=lambda lang_num : lang_num[1], reverse=True)
    
    if top_n <= 0:
        top_n = 10
    
    top_lang_num = None
    if sorted_lang_num is not None and len(sorted_lang_num) <= top_n :
        top_lang_num = sorted_lang_num
    else:
        top_lang_num = sorted_lang_num[0:top_n]

    #top_lang_distribution = [(str_none_to_none_str(x[0]), round(x[1] * 100.0 / proj_sum, 2))  for x in top_lang_num]
    top_lang_distribution = [(str_none_to_none_str(x[0]), Decimal(str(x[1] * 100.0 / proj_sum)).quantize(Decimal('0.01'),rounding=ROUND_UP))  for x in top_lang_num]
    return top_lang_distribution


def lang_project(request, name, pagenum=1):
    rc = request.rc
    rc.current_page = "language"
    pn = int(pagenum)
    if pn <= 0:
        pn = 1
                     
    q = Q()
    q = q & Q(status = consts.PROJECT_ENABLE, is_public=1,language=name)         
    build_page(rc, Project, q,
               pn,'/project/lang/list/{0}'.format(urlquote(name,"")), "", order=['-ctime'])                          
    update_my_project_status(request, rc.page.object_list)
    update_proj_info(rc.page.object_list)
    rc.projs = rc.page.object_list

    rc.currentlang = name
    rc.langs = consts.LANGS
    return send_response(request, 'project/lang-proj.html')


def lang_project_all(request, pagenum=1):
    rc = request.rc
    rc.current_page = "language"

    pn = int(pagenum)
    if pn <= 0:
        pn = 1
        
    q = Q()
    q = q & Q(status = consts.PROJECT_ENABLE, is_public=1)         
    build_page(rc, Project, q,
               pn,'/project/lang/list', "", order=['-ctime'])                          

    update_my_project_status(request, rc.page.object_list)
    update_proj_info(rc.page.object_list)
    rc.projs = rc.page.object_list

    rc.langs = consts.LANGS
    return send_response(request, 'project/lang-proj.html')

# 项目概览
def explore(request,day=1):
    rc = request.rc
    rc.current_page = "explore"
    
    rc.hotlangs = lang_distribution(20)

    rc.dayhot = update_proj_info(hot_list_projects("hot", 1, 1))
    rc.weekhot = update_proj_info(hot_list_projects("hot", 1, 7))
    rc.monthhot = update_proj_info(hot_list_projects("hot", 1, 30))
    

    rc.featurePrjs = FeatureProject.objects.all().order_by('-mtime')[:10]


    rc.ausers = avtive_user(10, 7)
    if rc.ausers is not None:
        for user in rc.ausers:
            update_user_info(user)
    
    newestprojs = Project.objects.filter(status=consts.PROJECT_ENABLE, is_public=1).order_by('-ctime')[:5]
    rc.newestprojs = newestprojs
        
    rc.recently = get_user_recent_activities(request, 5)

    return send_response(request, 'project/explore-proj.html')

##recently
def recently(request):
    rc = request.rc    
    rc.current_page = "recently"
    rc.recently = get_user_recent_activities(request, 50)
    return send_response(request, 'project/recently.html')

def avtive_user(num=10, days=7):
        now = datetime.datetime.now()
        start = now - datetime.timedelta(days)
        
        aus = Activity.objects.filter(user__status=consts.USER_ENABLE,
                                      project__status=consts.PROJECT_ENABLE,
                                      project__is_public=1, ctime__gt=start).values('user').annotate(uc=Count("user")).order_by('-uc')[:num]
        return sort_models(User, aus, 'user', 'uc');
    

def hot_list_projects(pt, pagenum=1, days=1):
    cacheName = 'hot_list_projects' + str(pagenum) + '_' + str(days)
    prjs = cache.get(cacheName)
    if prjs is None:
        now = datetime.datetime.now()
        start = now - datetime.timedelta(hours=23 * days, minutes=59, seconds=59)
    
        q = Q(status=consts.PROJECT_ENABLE, is_public=1,)
        od = []
        totals = 0
        if pt == 'hot':
            pn = int(pagenum)
            if pn <= 0:
              pn = 1
            pos = consts.PAGE_SIZE * (pn - 1)
            
            ps = Activity.objects.filter(project__status=consts.PROJECT_ENABLE, ctime__gt=start,
                                         project__is_public=1).values('project').annotate(uc=Count('project')).order_by('-uc')[pos:pos + consts.PAGE_SIZE]
            totals = total_models(Project, ps, 'project', 'uc')                             
            prjs = sort_models(Project, ps, 'project', 'uc')

            cache.set(cacheName, prjs, 24* 3600)  # 10*60secs 

    return prjs

def update_proj_info(projs):
    if projs is None:
        return []
    
    for proj in projs:
        proj.issue_times = q_gets(ProjectReport, project = proj, 
                                  project__status = consts.PROJECT_ENABLE, project__is_public=1)\
                                  .aggregate(Sum('issue_times'))['issue_times__sum']
        proj.watcher_count = q_gets(ProjectWatcher, project = proj, 
                                    project__status = consts.PROJECT_ENABLE, project__is_public=1)\
                                    .aggregate(Count('id'))['id__count']
    return projs
                                    
def update_user_info(user):
    if user is not None:
        prj_q = Q(project__status=consts.PROJECT_ENABLE)
        user.owner_projects = q_gets(Project, owner=user, status=consts.PROJECT_ENABLE, is_public=1)
        user.joined_projects = q_gets(ProjectMember,
                                user=user).filter(prj_q).exclude(member_type=consts.PM_REJECT_INV)
        user.proj_num = len(user.owner_projects) + len(user.joined_projects)
        
        lang_set = set()
        for i, proj in enumerate(user.owner_projects):
            if len(lang_set) == 2:
                break
            if proj.language is None:
                continue
            
            lang_set.add(proj.language)
        user.languages = str_splice(lang_set, ",")
    return user
"""
