from django.conf.urls import url, include
from django.contrib import admin
from . import views
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.main.index),
    url(r'^about$', views.main.about),
    url(r'^license$', views.main.license),
    url(r'^user/', include(views.auth.urls)),
    url(r'^u/', include(views.user.urls)),
    url(r'^p/', include(views.project.urls)),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns.append(url(r'^__debug__/', include(debug_toolbar.urls)))

"""
u = ['',
     (r'^msg/unread_count/$', 'apps.message.views.get_unread_count'),
     (r'^msg/send/$', 'apps.message.views.send_msg'),
     (r'^msg/move/$', 'apps.message.views.move_msg'),
     (r'^msg/del/$', 'apps.message.views.del_msg'),
     
     (r'^prj/lang/$',    'apps.project.views.ajax_lang_view'),
     (r'^prj/watch/(?P<name>[-\w]+)/$',    'apps.project.views.watch_project'),
     (r'^prj/clean/(?P<fid>[\w]+)/$',    'ajax_urls.prj_fclean'), 
     (r'^prj/invite/(?P<name>[-\w]+)/$', 'apps.project.admin.do_invite'), 
     (r'^prj/del_member/(?P<name>[-\w]+)/$', 'apps.project.admin.del_member'), 
     (r'^prj/accept/(?P<name>[-\w]+)/$', 'apps.project.admin.do_accept'), 
     (r'^prj/reject/(?P<name>[-\w]+)/$', 'apps.project.admin.do_reject'), 
     (r'^prj/exit/(?P<name>[-\w]+)/$', 'apps.project.admin.do_exit'), 
     (r'^prj/members/(?P<name>[-\w]+)/$', 'apps.project.admin.get_members'), 
     (r'^prj/members1/(?P<name>[-\w]+)/$', 'apps.project.admin.get_members1'), 

     (r'^prj/del/(?P<name>[-\w]+)/$', 'apps.project.admin.del_prj'), 
     (r'^prj/edit/(?P<name>[-\w]+)/$', 'apps.project.admin.edit_prj'), 

     (r'^issue/del/$', 'apps.issue.admin.del_issue'),
     (r'^issue/tags/(?P<name>[-\w]+)/$',    'apps.issue.props.get_tags'),
     (r'^issue/new_tag/(?P<name>[-\w]+)/$',    'apps.issue.props.new_tag'),
     (r'^issue/del_tag/(?P<name>[-\w]+)/$',    'apps.issue.props.del_tag'),

     (r'^issue/new_comment/(?P<issue_id>\d+)/$', 'apps.issue.comments.new_comment'),
     (r'^issue/comments/(?P<issue_id>\d+)/$',    'apps.issue.comments.get_comments'),
     (r'^issue/del_comment/$',    'apps.issue.comments.del_comment'),
     (r'^issue/get_comment_count/(?P<issue_id>\d+)/$',    'apps.issue.comments.get_comment_count'),
        
     (r'^user/clean/(?P<fid>[\w]+)/$',    'ajax_urls.user_fclean'), 
     (r'^user/edit_my/$',    'apps.user.views.do_edit_my'), 
     (r'^user/edit_email/$',    'apps.user.views.do_edit_email'), 
     (r'^user/watch/(?P<name>[-\w]+)/$',    'apps.user.views.watch_user'),

     (r'^user/checkname/(?P<name>[-\w]+)/$',    'apps.user.views.check_name'),
     (r'^user/checkemail/(?P<email>[-\w|@|.]+)/$',    'apps.user.views.check_email'),
     (r'^user/checkemailauth/$',    'apps.user.views.check_email_auth'),
     (r'^user/checknameauth/$',    'apps.user.views.check_name_auth'),

     (r'^delfile/$', 'apps.main.files.del_file'),

     ]

urlpatterns = patterns(*u)

u = ['',
     ('^$',       'apps.project.views.view_project'),
     ('^info/$',       'apps.project.views.project_info'),
     ('^info/(?P<pagenum>\d+)$', 'apps.project.views.project_info'),
     ('^info/(?P<pagenum>\d+)/(?P<key>.*)$', 'apps.project.views.project_info'),
     
     ('^admin/$', 'apps.project.admin.project_admin',{'pt':'proinfo'}),
     ('^admin/proinfo/$', 'apps.project.admin.project_admin',{'pt':'proinfo'}),
     ('^admin/meminfo/$', 'apps.project.admin.project_admin',{'pt':'meminfo'}),
     ('^admin/downinfo/$', 'apps.project.admin.project_admin',{'pt':'downinfo'}),
     
     ('^admin/resources/$', 'apps.project.admin.project_resources'),
     ('^watch/$', 'apps.project.views.project_watch_list'),

     (r'^file/(?P<fid>[\d]+)/', 'apps.main.files.get_file'),

     ('^issues/$', 'apps.issue.views.all_issues'),
     ('^issues/(?P<pagenum>\d+)$', 'apps.issue.views.all_issues'),
     ('^issues/(?P<pagenum>\d+)/(?P<key>.*)$', 'apps.issue.views.all_issues'),

     ('^issues/(?P<status>\w+)/$', 'apps.issue.views.list_issues'),
     ('^issues/(?P<status>\w+)/(?P<pagenum>\d+)$', 'apps.issue.views.list_issues'),
     ('^issues/(?P<status>\w+)/(?P<pagenum>\d+)/(?P<key>.*)$', 'apps.issue.views.list_issues'),

     ('^issue/(?P<issue_id>\d+)/$', 'apps.issue.views.view_issue'),
     ('^issue/change/(?P<issue_id>\d+)/$', 'apps.issue.admin.change_issue'),

     ('^issue/new/$', 'apps.issue.views.new_issue'),
    
     ('^src/$',                         'apps.repos.views.browse'),
     ('^src/(?P<path>.*)$',            'apps.repos.views.browse'),
     ('^logs/(?P<path>.*)',             'apps.repos.views.logs'),
     ('^log/(?P<rev>\d+)/$',            'apps.repos.views.log'),
     ('^log/(?P<rev>\d+)/(?P<path>.*)', 'apps.repos.views.log'),
     ('^diff/(?P<revN>\d+)/(?P<path>.*)', 'apps.repos.views.diff'),
     ('^diff/(?P<revN>\d+):(?P<revM>\d+)/$', 'apps.repos.views.diff'),
     ('^diff/(?P<revN>\d+):(?P<revM>\d+)/(?P<path>.*)', 'apps.repos.views.diff'),


     ('^del_wiki/$', 'apps.wiki.views.del_wiki'),
     ('^edit_wiki/$', 'apps.wiki.views.edit_wiki'),
     ('^edit_wiki/(?P<path>.*)/$', 'apps.wiki.views.edit_wiki'),
     ('^wiki/$', 'apps.wiki.views.wiki_index'),
     ('^wiki/(?P<path>.*)/$', 'apps.wiki.views.wiki_content'),
     ('^wikis/$', 'apps.wiki.views.wiki_list'),
     ('^wiki_changes/(?P<path>.*)/$', 'apps.wiki.views.wiki_changes'),
     ('^raw_wiki/(?P<path>.*)/$', 'apps.wiki.views.raw_wiki'),
     ('^raw_log_wiki/(?P<logid>\d+)/$', 'apps.wiki.views.raw_log_wiki'),
     ('^diff_log_wiki/(?P<logid>\d+)/$', 'apps.wiki.views.diff_log_wiki'),
     ]

"""
