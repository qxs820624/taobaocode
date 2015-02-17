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

from taocode2.models import *
from taocode2.helper.utils import *
from taocode2.helper import consts,xmlo
from taocode2 import settings

import urllib2

import os
import time
import traceback

__author__ = 'luqi@taobao.com'

def _get_repos_path(part, name):
    if part is None:
        return settings.GET_REPOS_ADMIN_URL(name)
    
    return part.prefix

def build_repos_base(part, name, root):
    repos_path = _get_repos_path(part, name)
    if repos_path[-1] != '/':
        repos_path += '/'
    return repos_path + root

def _rsvn_op(part, name, action):
    try:
        repos_path = build_repos_base(part, name, 'svnd/')
        repos_path = repos_path + '%s/%s'%(name, action)
        urllib2.urlopen(repos_path).read()
    except:
        reason = ''.join(traceback.format_exc())
        return False, reason

    return True, None
    
def rinit_repos(part, name):
    result, reason = _rsvn_op(part, name, 'new')

    if result is True:
        trunk_path = REPOS(part, name, '/trunk')
        exec_cmd(['svn', 'mkdir', '--no-auth-cache', '--non-interactive',
                  trunk_path, '-m', 'init '+name])
    return result, reason

def rdel_repos(part, name):
    return _rsvn_op(part, name, 'del')
        
def safe_path(path):
    path = path.strip()
    if path != '/':
        return '/' + path
    return '/'

def REPOS(part, name, path = ''):
    name = name.decode('utf8')
    repos_path = build_repos_base(part, name, 'svn/')
    return repos_path + '%s%s'%(name, path)

def LIST(url):
    code, out ,err = exec_cmd(['svn', 'list','--xml', '--incremental', 
                               '--no-auth-cache', '--non-interactive', url])
    if code != 0:
        raise Exception(err)
    return xmlo.loads(out) 

def CAT(url):
    code, out ,err = exec_cmd(['svn','cat', '--no-auth-cache', '--non-interactive', url])
    if code != 0:
        raise Exception(err)
    return out

def INFO(url):
    code, out ,err = exec_cmd(['svn','info', '--xml', '--no-auth-cache', '--non-interactive', url])
    if code != 0:
        raise Exception(err)
    return xmlo.loads(out)

def LOG(url, rev=None, limit=-1):
    cmd = 'svn log -v --xml --no-auth-cache --non-interactive'.split(' ')
    if rev is not None:
        cmd.append('-r')
        cmd.append(rev)
    if limit != -1:
        cmd.append('-l')
        cmd.append(str(limit))
    cmd.append(url)
    code, out ,err = exec_cmd(cmd)

    if code != 0:
        raise Exception(err)

    return xmlo.loads(out)
    
def DIFF(url, revN, revM=None):
    cmd = 'svn diff --no-auth-cache --non-interactive --no-diff-deleted'.split(' ')
    if revN is not None and revM is None:
        cmd.append('-c')
        cmd.append(revN)
    elif revN is not None and revM is not None:
        cmd.append('-r')
        cmd.append(revN + ':' + revM)

    cmd.append(url)    
    code, out ,err = exec_cmd(cmd)

    if code != 0:
        return None
    return out

