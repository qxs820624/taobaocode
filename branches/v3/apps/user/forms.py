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
from django.utils.translation.trans_real import gettext
import re
from taocode2.models import User
from taocode2.helper.validator import UniqueValidator, fast_validator 
from taocode2.helper.utils import as_json, q_get
from taocode2.helper import consts

from taocode2.settings import SITE_ROOT
from django.core.validators import validate_slug, validate_email,RegexValidator

from django import forms

from django.contrib.auth import authenticate
from django.utils.translation import ugettext, ugettext_lazy as _


__author__ = 'luqi@taobao.com'


class NewUserFastForm(forms.ModelForm):
    name=forms.CharField(   label='',
                            min_length = 3,
                            max_length = 40,
                            #help_text=gettext("login account"),
                            validators=[validate_slug, 
                                        UniqueValidator(User, 'name')],
                           # widget=forms.TextInput(attrs={'class':'name-text','value':'username','onclick':'if(this.value==this.defaultValue){this.value=""}'})
                             widget=forms.TextInput(attrs={'class':'name-text','placeholder':u'用户名'})
                            )
    
    
    email = forms.EmailField(label='',
                             validators=[validate_email,
                                         UniqueValidator(User, 'email')],
                             widget=forms.TextInput(attrs={'class':'email-text','placeholder':u'电邮地址'})
                             )   
                    
    
    password = forms.CharField(  label='',
                                 min_length = 7,
                                 max_length = 12,
                                 widget=forms.PasswordInput(attrs={'class':'password-text','placeholder':u'密码'})
                                 )
    

    
    def clean_password(self):
        pw=self.cleaned_data['password']
        if not re.search('^[a-zA-Z]+$',pw) and re.search('^[0-9]+$',pw):
            raise forms.ValidationError(gettext('error password format'))
        
        return pw

            
         
    class Meta:
        model = User
        fields = ('name', 'password', 'email') 
       


class NewUserForm(forms.ModelForm):
    name = forms.CharField(label='',
                           min_length = 3,
                           max_length = 40,
                           #help_text=gettext("min_length"),
                           #validators=[validate_slug,
                           validators=[validate_slug,
                                       UniqueValidator(User, 'name')],
                           error_messages={
                                           'required': '请输入用户名，用户名长度不少于3个字符，不能使用中文',
                                           'invalid': '请输入有效的用户名',
                                           'min_length':'用户名长度不少于3个字符，不能使用中文',
                                           'max_length':'用户名长度不能多于40个字符，不能使用中文',
                                           },
                           widget=forms.TextInput(attrs={'class':'text'}),
                        

                           )
    #nick = forms.CharField(label=gettext("nick name"),
    #                       min_length = 2,
    #                       max_length = 32,
    #                       help_text=gettext("display name"),
    #                       validators=[validate_slug,
    #                                   UniqueValidator(User, 'nick')])
    
    email = forms.EmailField(label=gettext("email address"),
                             help_text=gettext("eg:user@example.org"),
                             validators=[UniqueValidator(User, 'email')],
                             widget=forms.TextInput(attrs={'class':'text'}),
                             error_messages={
                                           'required': '请输入电邮地址',
                                           'invalid': '请输入有效的电邮地址',
                                           },
                             )   
    
    phone = forms.CharField(label=gettext("phone"),
                            min_length=11,
                            max_length=11,
                            required=False,
                            widget=forms.TextInput(attrs={'class':'text'}),
                            )
    
    title = forms.CharField(label=gettext("title"),
                            help_text=gettext("eg:taobao,diaosi ','"),
                            min_length=2,
                            max_length=200,
                            required=False,
                            widget=forms.TextInput(attrs={'class':'text'}),
                            )
    
    password_0 = forms.CharField(label=gettext("password"),
                                 min_length = 7,
                                 max_length = 12,
                                # required=False,
                                 widget=forms.PasswordInput(attrs={'class':'text'}),
                                 error_messages={
                                           'required': '请输入密码，密码长度不少于7个字符，至少包含一个字母或数字',
                                           'invalid': '密码长度不少于7个字符，至少包含一个字母或数字',
                                           'min_length':'密码长度不少于7个字符，至少包含一个字母或数字',
                                           },
                                 validators=[RegexValidator(re.compile(r'[^a-zA-Z+]|^.{1,6}$')),RegexValidator(re.compile(r'[^0-9+]|^.{1,6}$'))],
                                 )
    

    password_1 = forms.CharField(label=gettext("password(replay)"),
                                 min_length = 7,
                                 max_length = 12,
                                # required=False,
                                 help_text=gettext("password must same as twice"),
                                 widget=forms.PasswordInput(attrs={'class':'text'}),
                                 error_messages={
                                           'required': '请输入密码，密码长度不少于7个字符，至少包含一个字母或数字',
                                           'invalid': '密码长度不少于7个字符，至少包含一个字母或数字',
                                           'min_length':'密码长度不少于7个字符，至少包含一个字母或数字',
                                           },
                                validators=[RegexValidator(re.compile(r'[^a-zA-Z+]|^.{1,6}$')),RegexValidator(re.compile(r'[^0-9+]|^.{1,6}$'))],
                                    )


    accept = forms.BooleanField(label=gettext("accept privacy"),
                                error_messages={'required': gettext('must accept privacy')},
                                help_text="<a href='/about/privacy/' target='_blank'>privacy</a>",
                                
                                
                                
                                )
    
    def clean_password_1(self):
        pw0 = self.cleaned_data['password_0']
        pw1 = self.cleaned_data['password_1']
        if not re.search('^[a-zA-Z]+$',pw0) and re.search('^[0-9]+$',pw0):
            raise forms.ValidationError(gettext('error password format'))
            
        if pw0 != pw1 or len(pw0) == 0 is True:
            raise forms.ValidationError(gettext('password must same as twice'))
        
        return pw1
        
    class Meta:
        model = User
        fields = ('name',  'email','phone','title','password_0', 'password_1')
        
        

class PasswordResetForm(forms.Form):
    email = forms.EmailField(label=gettext("E-mail"), max_length=75)

    def clean_email(self):
        email = self.cleaned_data["email"]
        self.cache_user = q_get(User, email__iexact=email,
                                 status=consts.USER_ENABLE)

        if self.cache_user is None:
            raise forms.ValidationError(gettext("That e-mail address doesn't have an associated user account. Are you sure you've registered?"))
        return email
    
    
    

class AuthenticationForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
    username = forms.CharField(label='',
                                max_length=40,
                                widget=forms.TextInput(attrs={'class':'name-text','placeholder':u'用户名'})
                                )
    password = forms.CharField(label='',
                                widget=forms.PasswordInput(attrs={'class':'password-text','placeholder':u'密码'})
                                )

    error_messages = {
        'invalid_login': _("Please enter a correct username and password. "
                           "Note that both fields are case-sensitive."),
        'no_cookies': _("Your Web browser doesn't appear to have cookies "
                        "enabled. Cookies are required for logging in."),
        'inactive': _("This account is inactive."),
    }


    def __init__(self, request=None, *args, **kwargs):
        """
        If request is passed in, the form will validate that cookies are
        enabled. Note that the request (a HttpRequest object) must have set a
        cookie with the key TEST_COOKIE_NAME and value TEST_COOKIE_VALUE before
        running this validation.
        """
        self.request = request
        self.user_cache = None
        super(AuthenticationForm, self).__init__(*args, **kwargs)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'])
            elif not self.user_cache.is_active:
                raise forms.ValidationError(self.error_messages['inactive'])
        self.check_for_test_cookie()
        return self.cleaned_data

    def check_for_test_cookie(self):
        if self.request and not self.request.session.test_cookie_worked():
            raise forms.ValidationError(self.error_messages['no_cookies'])

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache


    

