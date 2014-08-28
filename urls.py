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

import os
from django.conf.urls.defaults import patterns, include
from taocode2.settings import SITE_ROOT,MEDIA_ROOT,ADMIN_PATH

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


u = ['',
     ('^tbsts197324129\.txt', 'apps.main.views.tbsts'),
     #('^$', 'apps.main.views.index'),
     ('^$', 'apps.user.views.fast_register'),
     ##
     ('^opensources/$', 'apps.main.views.opensources_list'),
     ('^opensources/(?P<pagenum>\d+)/(?P<key>.*)/$',  'apps.main.views.opensources_list'),
     ('^opensources/(?P<pagenum>\d+)/$',  'apps.main.views.opensources_list'),
     
     ('^opensources/(?P<key>.*)/$',  'apps.main.views.opensources_list'),
     
     
     (r'^project/recently/$', 'apps.project.views.recently'),
     (r'^project/explore/$',  'apps.project.views.explore'),
     (r'^project/lang/$',  'apps.project.views.lang_view'),
     (r'^project/lang/list/(?P<pagenum>\d+)/$',  'apps.project.views.lang_project_all'),
     (r'^project/lang/list/(?P<name>.*)/(?P<pagenum>\d+)/$',  'apps.project.views.lang_project'),
     (r'^project/view/(?P<pid>\d+)/$', 'apps.project.views.view_old'),
     (r'^project/(?P<pid>\d+)/viewSvn/$', 'apps.project.views.view_old_src'),

     (r'^trac/(?P<name>[\w]+)/wiki/(?P<path>.*)', 'apps.project.views.view_old_wiki'),
     
     (r'^rsvn/(?P<name>[\w]+)/add/', 'apps.repos.views.rsvn_add'),
     (r'^rsvn/(?P<name>[\w]+)/del/(?P<del_name>.*)', 'apps.repos.views.rsvn_del'),
     (ADMIN_PATH, include(admin.site.urls)),
     ('^about/$', 'apps.main.views.show_page', {'name':'about.html','pagename':'About Taocode'},),
     ('^aboutus/$', 'apps.main.views.show_page', {'name':'aboutus.html','pagename':'About Us'},),
     ('^about/privacy/$', 'apps.main.views.show_page', {'name':'privacy.html','pagename':'Privacy'}),
     ('^about/license/$', 'apps.main.views.show_page', {'name':'license.html','pagename':'License'}),
     ('^license.html$', 'apps.main.views.show_page', {'name':'license.html','pagename':'License'}),

     # static file
	 #
     ('^css/(?P<path>.*)$', 'django.views.static.serve', {'document_root' : os.path.join(MEDIA_ROOT,'css')}),
     ('^js/(?P<path>.*)$',  'django.views.static.serve', {'document_root' : os.path.join(MEDIA_ROOT,'js')}),
     ('^img/(?P<path>.*)$', 'django.views.static.serve', {'document_root' : os.path.join(MEDIA_ROOT,'img')}),

     
     # user profilerr
     #
     ('^u/(?P<name>[\.\s\-\w]+)/$',  'apps.user.views.view_user',{'pt':'mypro'}),
     ('^u/(?P<name>[\.\s\-\w]+)/worklogs/$',    'apps.user.views.view_user', {'pt':'worklogs'}),
     ('^u/(?P<name>[\.\s\-\w]+)/watpro/$',     'apps.user.views.view_user', {'pt':'watpro'}),
     ('^u/(?P<name>[\.\s\-\w]+)/mypro/$',     'apps.user.views.view_user', {'pt':'mypro'}),
     
     
     
     ('^my/$',           'apps.user.views.view_user',{'pt':'mypro'}),
     ('^my/edit/$',      'apps.user.views.edit_my'),   
     ('^my/doedit/$',      'apps.user.views.do_edit_my'),  
     ('^my/notify/$',    'apps.user.views.edit_notify'),      
     ('^my/newpwd/$',    'apps.user.authviews.change_password'),
    
     ('^my/worklogs/$',    'apps.user.views.view_user', {'pt':'worklogs'}),
     
     ('^my/watpro/$',     'apps.user.views.view_user', {'pt':'watpro'}),
     ('^my/mypro/$',     'apps.user.views.view_user', {'pt':'mypro'}),
     
     
     #login
     #
     ('^fastregister/$',     'apps.user.views.fast_register'),
     ('^register/$',     'apps.user.views.register'),
     (r'^login/$',  'apps.user.views.login_view'),
     (r'^logout/$',  'apps.user.views.logout_view'),

     #verify
     #
     ('^reset/$',  'apps.user.authviews.reset_password'),
     ('^reset/(?P<code>[\w]+)/$',  'apps.user.authviews.reset_password_code'),

     ('^verify/(?P<code>[\w]+)/$',  'apps.user.verify.check_code'),
     ('^verify/(?P<code>[\w]+)/cancel/$',  'apps.user.verify.do_check_code_cancel'),
     ('^verify/(?P<code>[\w]+)/ok/$',  'apps.user.verify.do_check_code_ok'),
 
     #message
     #
     ('^msg/$',      'apps.message.views.show_box'),
     ('^msg/(?P<name>[\w]+)/$',      'apps.message.views.show_box'),
     ('^msg/(?P<name>[\w]+)/(?P<pagenum>\d+)/$',  'apps.message.views.show_box'),
    
     #search (user-nav)
     #
     ('^search/$',                   'apps.main.views.search'),  
     ('^search/(?P<type>.*)/(?P<pagenum>\d+)/(?P<key>.*)/$',  'apps.main.views.search'),
     ('^search/(?P<type>.*)/(?P<pagenum>\d+)/$',  'apps.main.views.search'), 
     
     ('^search/(?P<type>.*)/(?P<key>.*)/$',  'apps.main.views.search'),
     ('^search/(?P<type>.*)/$',  'apps.main.views.search'),
     
     
     # projects
     #
     ('^all/$',                   'apps.project.views.all_projects'),
     ('^all/(?P<pagenum>\d+)/$',  'apps.project.views.all_projects'),
     ('^all/(?P<pagenum>\d+)/(?P<key>.*)/$',  'apps.project.views.all_projects'),

     ('^hot/$',                   'apps.project.views.list_projects', {'pt':'hot'}),
     ('^newest/$',                'apps.project.views.list_projects', {'pt':'newest'}),
     ('^newest/(?P<pagenum>\d+)/$',  'apps.project.views.list_projects', {'pt':'newest'}),
     ('^newest/(?P<pagenum>\d+)/(?P<key>.*)/$',  'apps.project.views.list_projects', {'pt':'newest'}),
     ('^random/$',                'apps.project.views.list_projects', {'pt':'random'}),
     ('^committimes/$',                'apps.project.views.list_projects', {'pt':'committimes'}),
     ('^downloadtimes/$',                'apps.project.views.list_projects', {'pt':'downloadtimes'}),
     ('^issuetimes/$',                'apps.project.views.list_projects', {'pt':'issuetimes'}),
     ('^watched/$',               'apps.project.views.list_projects', {'pt':'watched'}),
 
     ('^new/$',                   'apps.project.views.new_project'),
     ('^tool/$',                   'apps.project.views.tool'),

     #project url
     #
     (r'^p/(?P<name>[\.\s\-\w]+)/',   include('prj_urls')),  
     ('^wiki_formarts/$', 'apps.wiki.views.wiki_formarts'),

     #api
     #
     (r'^api/', include('api.urls')),         
     
     #ajax
     #
     (r'^ajax/', include('ajax_urls')),

     #opens
     (r'^open/', include('apps.open.urls')),

     ]

urlpatterns = patterns(*u)
