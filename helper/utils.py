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

from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from taocode2.helper.func import wrap
import subprocess
from datetime import datetime
from datetime import timedelta
from string import join
from django.utils.encoding import smart_unicode
from decimal import *
import time
import string

try:
    from djangoutils import simplejson as json
except ImportError:
    import json

__author__ = 'luqi@taobao.com'


def send_json_response(data):
    return HttpResponse(json.dumps(data,cls=ComplexJsonEncoder), mimetype='application/json')

def send_response(request, name, dicts = {}):
    return render_to_response(name, dicts, RequestContext(request))

def q_get(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None


def q_gets(model, **args):
    return model.objects.filter(**args)


def is_exist(model, **args):
    try:
        model.objects.get(**args)
        return True
    except model.DoesNotExist:
        pass

    return False

def fast_form(template, formname, from_arg='form'):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.method != 'POST':
                return send_response(request,
                                     template, {from_arg:formname()})
            
            form = formname(request.POST)
            if form.is_valid() is False:
                return send_response(request, template, {from_arg:form})
            setattr(request, from_arg, form)
            return view_func(request, *args, **kwargs)
        return wrap(view_func, _wrapped_view)
    return decorator


def as_json(view_func):
    def _wrapped_view(*args, **kwargs):
        resp = view_func(*args, **kwargs)
        if isinstance(resp, HttpResponse) is False:
            return send_json_response(resp)
        return resp
    return wrap(view_func, _wrapped_view)

def build_menu(items, choice):
    menus = []
    for i in items:
        if i[0] == choice:
            menus.append({'uri':i[1], 'txt':i[2], 'choice':True})
        else:
            menus.append({'uri':i[1], 'txt':i[2]})
    return menus



def exec_cmd(args, std_in = None):

    p = subprocess.Popen(args,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    out,err = p.communicate(std_in)
    
    code = p.wait()
    return code, out,err #p.stdout.read(), p.stderr.read()
            
def sort_models(model, vals, k, c, reverse=True):
    sps = {}
    for v in vals:
        sps[v[k]] = v[c]
        
    outvals = [p for p in model.objects.filter(pk__in = [v[k] for v in vals])]
    
    outvals.sort(key=lambda x: sps[x.id], reverse=reverse)
    return outvals

def total_models(model, vals, k, c, reverse=True):
    total=0
    for v in vals:
        total = v[c]+total
    
    return total

def build_project_graph(model, vals, k, c, totals,titlestr):
    menus = []
    for v in vals:
        p=model.objects.filter(pk__in=[v[k]])
        menus.append({'project':p[0], 'uc':force_unicode(titlestr)+str(v[c]), 'width':v[c]*500/totals})
        
    return menus

def utc2loc(v):
    if v is None:
        return None
    return v - timedelta(seconds = time.timezone)

def str_splice(v, split):
    result = join(v,split)
    return result

def str_none_to_empty(v):
    if v is None:
        return ""
    return v

def str_none_to_none_str(v):
    if v is None or v.strip() =="":
        return "None"
    return v


def force_unicode(v):
    try:
        # enc = chardet.detect(v)['encoding']
        # if enc is None:
        #    enc = 'utf8'
        return smart_unicode(v, 'gbk')
    except:
        pass
    return v
    
    
class ComplexJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        else:
            return json.JSONEncoder.default(self, obj)
