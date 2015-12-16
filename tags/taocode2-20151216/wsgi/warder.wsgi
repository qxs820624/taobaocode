import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
os.environ['DJANGO_SETTINGS_MODULE'] = 'taocode2.settings'
os.environ['ROOT_URLCONF'] = 'taocode2.warder_urls'
import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
