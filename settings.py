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

# Django settings for taocode2 project.
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMIN_PATH = r'^admin/'
REPOS_ROOT = '/svn/'

OSS_ID = 'test_oss_id'
OSS_KEY = 'test_oss_key'
OSS_NAME = 'uploads'

OCS_HOST = 'ocs_host'
OCS_USER = 'ocs_user'
OCS_PASSWORD = 'ocs_password'

REALM = 'taocode'
LOG_FIFO = '/tmp/taocode.fifo'

def GET_REPOS_ADMIN_URL(name):
    return REPOS_URL

ADMINS = ()

MAIL_SENDER = 'admin@localhost'
TEAM_NAME = 'Taocode team'
SITE_URL = 'http://code.taobao.org'

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME':'test.db3',                              # Or path to database file if using sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Shanghai'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'zh-CN'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = 'media'
SITE_ROOT  = ''


# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

LOGIN_URL = SITE_ROOT + '/login/'
LOGIN_REDIRECT_URL = SITE_ROOT + '/my/'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
DEFAULT_CHARSET = 'utf-8'

UPLOAD_DIR='uploads'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    #'taocode2.helper.cache_filesystem.load_template_source',(
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.csrf',
    'django.contrib.auth.context_processors.auth',
    'taocode2.helper.middleware.simple_context',
    'django.contrib.messages.context_processors.messages',
    )

MIDDLEWARE_CLASSES = (
    #'appenlight_client.django_middleware.AppenlightMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'taocode2.helper.middleware.SimpleContextMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    )

ROOT_URLCONF = os.getenv('ROOT_URLCONF', 'taocode2.urls')

TEMPLATE_DIRS = (
    'templates',
)

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.humanize',
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.messages',
    'taocode2',
    )

AUTHENTICATION_BACKENDS = (
    'taocode2.apps.user.auth.UserAuthBackend',
    )

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

SECRET_KEY = 'test'
DATETIME_FORMAT='Y-m-d H:i:s'
DATE_FORMAT='Y-m-d'

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'


try:
    from private_setting import *
except ImportError:
    pass

