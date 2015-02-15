from django.contrib import admin
from taocode2.models import *

class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'last_login_ip', 'last_login')
    list_filter = ('sex', 'status', 'last_login')
    ordering = ('ctime',)
    search_fields = ('name', 'email',)



class ProjectAdmin(admin.ModelAdmin):
    search_fields = ('name', 'title')
    list_display = ('name', 'is_public', 'title', 'status', 'owner', 'ctime')
    ordering = ('ctime',)
    list_filter = ('is_public', 'status', 'ctime', 'license')
    fields = ('name', 'title', 'status', 'license', 'is_public', 'language', 'click')
    
class AliProjectAdmin(admin.ModelAdmin):
    search_fields = ('subject', 'project_owner')
    list_display = ('subject', 'project_owner', 'attend_users', 'content', 'svnurl', 'siteurl')
    ordering = ('ctime',)
    list_filter = ('ctime', )


class AliProjectUserAdmin(admin.ModelAdmin):
    search_fields = ('project__subject', 'name')


class WikiContentAdmin(admin.ModelAdmin):
    search_fields = ('path', 'project__name')
    list_display = ('project', 'path', 'user', 'status', 'mtime', 'ctime')
    ordering = ('mtime',)
    list_filter = ('mtime', )
    fields = ('path', 'status', 'content')
    
class ProjectMemberAdmin(admin.ModelAdmin):
    search_fields = ('user__name', 'project__name')
    list_display = ('user', 'project', 'member_type', 'join_time', 'mtime')
    ordering = ('mtime',)
    list_filter = ('mtime', 'member_type')

class FeatureProjectAdmin(admin.ModelAdmin):
    search_fields = ('project__name', )
    list_display = ('project', 'mtime')
    ordering = ('mtime',)
    list_filter = ('mtime', )

class IssueAdmin(admin.ModelAdmin):
    search_fields = ('creator__name', 'project__name', 'title')
    list_display = ('project', 'creator', 'title', 'status', 'ctime', 'mtime')
    ordering = ('mtime',)
    list_filter = ('mtime', 'status')


class ProjectAttachmentAdmin(admin.ModelAdmin):
    search_fields = ('project__name', 'orig_name')
    list_display = ('ftype', 'fname', 'orig_name', 'status', 'size', 'ctime')
    ordering = ('ctime',)
    list_filter = ('ctime', 'status')
    exclude = ('project', 'owner')

class IssueCommentAdmin(admin.ModelAdmin):
    search_fields = ('issue__title', 'owner__name')
    list_display = ('issue','issue', 'owner', 'status', 'mtime', 'ctime')
    ordering = ('ctime',)
    list_filter = ('ctime', 'status')



admin.site.register(User, UserAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectMember, ProjectMemberAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(IssueComment, IssueCommentAdmin)
admin.site.register(WikiContent, WikiContentAdmin)
admin.site.register(ProjectAttachment, ProjectAttachmentAdmin)
admin.site.register(FeatureProject, FeatureProjectAdmin)
admin.site.register(AliProject, AliProjectAdmin)
admin.site.register(AliProjectUser, AliProjectUserAdmin)
admin.site.register(ReposPart)
