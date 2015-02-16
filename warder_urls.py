import os
from django.conf.urls.defaults import patterns, include

u = ['',
     ('^auth_svn/$', 'tools.warder.check_auth_v0'),
     ]

urlpatterns = patterns(*u)
