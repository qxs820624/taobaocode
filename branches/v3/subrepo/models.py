from django.db import models

"""
from django.utils.translation.trans_real import gettext
from django.db import models
from django.db.models import Q,Count,Sum
from hashlib import md5,sha256
from django.core.urlresolvers import reverse
from taocode2.helper import consts
from django.utils.html import escape


def md5_pwd(pwd):
    return md5('%s'%(pwd)).hexdigest()

def sha_pwd(pwd):
    return sha256(md5_pwd(pwd)).hexdigest()

class User(models.Model):
    name = models.CharField(max_length=40, unique=True)
    #nick = models.CharField(max_length=32, unique=True)
    email = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=128)

    status = models.SmallIntegerField(db_index=True,
                                      choices=[(consts.USER_DISABLE, 'Disable'),
                                               (consts.USER_ENABLE, 'Enable'),
                                               (consts.USER_DELETED, 'Deleted'),
                                               ])
    ctime = models.DateTimeField(auto_now_add=True)
    supper = models.BooleanField(default=False)
    
    title=models.CharField(max_length=200,blank=True)
    phone=models.CharField(max_length=20, blank=True)
    
    #pic = models.CharField(max_length=200)
    sex = models.SmallIntegerField(choices=[(consts.USER_FEMALE, 'Female'),
                                            (consts.USER_MALE, 'Male'),
                                            (consts.USER_UNKNOWN, 'Unknown'),
                                            ])
    
    last_login_ip = models.CharField(max_length=32)
    last_login = models.DateTimeField(auto_now=True)

    openId=models.CharField(max_length=40,blank=True)
    
    openPlatform=models.CharField(max_length=100,blank=True)


    signature=models.CharField(max_length=200,blank=True)


    def natural_key(self):
        return self.name
    
    def __unicode__(self):
        return self.name

    def is_authenticated(self):
        return True
    
    def is_active(self):
        return self.status == consts.USER_ENABLE

    def get_and_delete_messages(self):
        return []

    def check_password(self, raw_password):
        if self.password.startswith('sha:'):
            return self.password[4:] == sha_pwd(raw_password)
        else:
            return self.password == md5_pwd(raw_password)
        
    def set_password(self, new_password):
        self.password = 'sha:'+sha_pwd(new_password)

    def url(self):
        return reverse('apps.user.views.view_user', args=[self.name])

    def is_staff(self):
        return self.supper
    
    def has_perm(self, label):
        return self.supper

    def has_module_perms(self, label):
        return self.supper

class Message(models.Model):
    owner = models.ForeignKey(User)
    sender = models.ForeignKey(User, related_name="sender", null=True)

    is_read = models.BooleanField()
    sender_status = models.SmallIntegerField()
    reader_status = models.SmallIntegerField()
    
    content = models.CharField(max_length=1024)

    send_time = models.DateTimeField(auto_now_add=True)
    read_time = models.DateTimeField(null=True, blank=True)
    
    def json(self):
        return (self.id, self.sender.url(), self.sender.name,
                self.owner.url(), self.owner.name,
                self.is_read, escape(self.content).replace('\n','<br/>'), 
                str(self.send_time), str(self.read_time))


prj_status_consts = [(consts.PROJECT_DISABLE, 'Disable'),
                     (consts.PROJECT_ENABLE, 'Enable'),
                     (consts.PROJECT_MARK_DELETED, 'Mark Deleted'),
                     (consts.PROJECT_TRUE_DELETED, 'True Deleted')]

class ReposPart(models.Model):
    prefix = models.CharField(max_length=128)
    can_new = models.BooleanField(db_index=True)
    count = models.IntegerField(db_index=True)
    ctime = models.DateTimeField(auto_now_add=True)
    mtime = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '%s - can_new(%s) count(%s)'%(self.prefix, self.can_new, self.count)

class Project(models.Model):
    owner = models.ForeignKey(User)

    name = models.CharField(max_length=32, unique=True)
    title = models.CharField(max_length=200, null=True)
    tags = models.TextField(null=True, blank=True)

    status = models.SmallIntegerField(db_index=True,
                                      choices = prj_status_consts)
    ctime = models.DateTimeField(auto_now_add=True)

    license = models.CharField(max_length=255, null=True, blank=True)
    is_public = models.BooleanField()
    language = models.CharField(max_length=40, null=True)
    
    click = models.BigIntegerField(default=0)
    part = models.ForeignKey(ReposPart, null=True)

    def __unicode__(self):
        return self.name

    def url(self):
        return reverse('apps.project.views.view_project', args=[self.name])

class ProjectProfile(models.Model):
    project = models.ForeignKey(Project)
    name = models.CharField(max_length=32, unique=True)
    value = models.CharField(max_length=1024)
    

class ProjectMember(models.Model):
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    member_type = models.SmallIntegerField(choices = [(consts.PM_SEND_INV, 'Send invitation'),
                                                      (consts.PM_ACCEPT_INV,'Accept invitation'),
                                                      (consts.PM_REJECT_INV,'Reject invitation'),
                                                      ])
    join_time = models.DateTimeField(auto_now_add=True)
    mtime = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [("user", "project")]

    
    def get_inv_text(self, inv):
        if inv == consts.PM_SEND_INV:
            return gettext("Sending")
        elif inv == consts.PM_REJECT_INV:
            return gettext("Rejected")
        else:
            return gettext("Accepted")
       
    def json(self):
        return (self.user.url(), self.user.name, 
                self.get_inv_text(self.member_type), str(self.join_time))
    
    def json_join(self):
        return (self.project.url(), self.project.name,
                self.get_inv_text(self.member_type), str(self.join_time))

class ProjectWatcher(models.Model):
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    
    watch_time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = [("user", "project")]
        
class ProjectReportManager(models.Manager):
    def commit_sum(self, keyword):
        return self.filter().aggregate(Sum("committiimes"))
        
class ProjectReport(models.Model):
    project = models.ForeignKey(Project)
    report_cycle=models.IntegerField(blank=False)
    download_times=models.IntegerField(blank=True)
    commit_times=models.IntegerField(blank=True)
    issue_times=models.IntegerField(blank=True) 
    
    ctime = models.DateTimeField(auto_now_add=True)
    mtime = models.DateTimeField(auto_now_add=True)
    objects = ProjectReportManager()
    
    class Meta:
        unique_together = [("project", "report_cycle")]

class Repository(models.Model):
    project = models.ForeignKey(Project)

    repos_type = models.SmallIntegerField()
    vc_type=models.SmallIntegerField() #version control type:svn,git..
    url = models.CharField(max_length=1024)
    auth_user = models.CharField(max_length=128)
    auth_password = models.CharField(max_length=128)

class Issue(models.Model):
    project = models.ForeignKey(Project)
    #tracker = models.ForeignKey("Tracker")
    #version = models.ForeignKey("Version", null=True)
    creator = models.ForeignKey(User, related_name="creator", null=True)
    #assigner = models.ForeignKey(User, related_name="assigner", null=True)

    #tags = models.ManyToManyField(blank=True, "Tag", null=True)

    title = models.CharField(max_length=200)
    content = models.TextField(null=True)
    status = models.SmallIntegerField(db_index=True,
                                      choices = [(consts.ISSUE_OPEN,'Open'),
                                                 (consts.ISSUE_CLOSED,'Closed'),
                                                 (consts.ISSUE_DELETED,'Deleted')])
    #start = models.DateTimeField(blank=True,null=True)
    #end = models.DateTimeField(blank=True,null=True)
    
    vote_count = models.IntegerField(blank=True)
    
    ctime = models.DateTimeField(auto_now_add=True)
    mtime = models.DateTimeField(auto_now=True)
    
    def closed(self):
        return self.status == consts.ISSUE_CLOSED

    def url(self):
        return reverse('apps.issue.views.view_issue',
                       args=[self.project.name, self.id])

    def __unicode__(self):
        return self.title

"-""
class Tracker(models.Model):
    project = models.ForeignKey(Project)
    name = models.CharField(max_length=64, unique=True)

    def __unicode__(self):
        return self.name

class Version(models.Model):
    project = models.ForeignKey(Project)
    name = models.CharField(max_length=64)

    start = models.DateTimeField()
    end = models.DateTimeField()

    def __unicode__(self):
        return self.name


    class Meta:
        unique_together = [("name", "project")]

"-""    
class Tag(models.Model):
    project = models.ForeignKey(Project)
    name = models.CharField(max_length=64)
    color = models.CharField(max_length=12, null=True)

    def __unicode__(self):
        return self.name



class IssueComment(models.Model):
    issue = models.ForeignKey(Issue)
    owner = models.ForeignKey(User)
    content = models.TextField()
    
    status = models.SmallIntegerField(choices = [(consts.COMMENT_ENABLE, 'Enable'),
                                                 (consts.COMMENT_DELETED, 'Deleted')])
    
    ctime = models.DateTimeField(auto_now_add=True)
    mtime = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.content

class IssueVote(models.Model):
    issue = models.ForeignKey(Issue)
    owner = models.ForeignKey(User)
    ctime = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = [("issue", "owner")]


class WikiContent(models.Model):
    project = models.ForeignKey(Project)
    user = models.ForeignKey(User)
    last_user = models.ForeignKey(User, related_name="last_user")

    path = models.CharField(max_length=255, db_index=True)
    content = models.TextField()
    status = models.SmallIntegerField(choices = [(consts.WIKI_ENABLE, 'Enable'),
                                                 (consts.WIKI_DELETED, 'Deleted')])

    ctime = models.DateTimeField(auto_now_add=True)
    mtime = models.DateTimeField(auto_now=True)

    def url(self):
        return reverse('apps.wiki.views.wiki_content',
                       args=[self.project.name, self.path])

    def __unicode__(self):
        return self.path

    class Meta:
        unique_together = [("project", "path")]


class WikiContentLog(models.Model):
    project = models.ForeignKey(Project)
    user = models.ForeignKey(User)
    wiki = models.ForeignKey(WikiContent)

    content = models.TextField(null=True)
    old_content = models.TextField(null=True)    
    ctime = models.DateTimeField(auto_now_add=True)


class ProjectAttachment(models.Model):    
    project = models.ForeignKey(Project)
    ftype = models.CharField(max_length=12)
    ftid = models.IntegerField()
    status = models.SmallIntegerField(choices = [(consts.FILE_ENABLE, 'Enable'),
                                                 (consts.FILE_DELETED, 'Deleted')])
    fname = models.CharField(max_length=1024)
    orig_name = models.CharField(max_length=255)
    size = models.IntegerField()
    owner = models.ForeignKey(User)
    ctime = models.DateTimeField(auto_now_add=True)

    def json(self):
        return [self.id, escape(self.orig_name)]

    def __unicode__(self):
        return self.orig_name

class VerifyTask(models.Model):
    user = models.ForeignKey(User)

    code = models.CharField(max_length=32, unique=True) #md5code
    name = models.CharField(max_length=255, db_index=True)
    data = models.CharField(max_length=255)

    is_done = models.BooleanField()
    ctime = models.DateTimeField(auto_now_add=True, db_index=True)
    expire_time = models.DateTimeField()
    

class UserWatcher(models.Model):
    user = models.ForeignKey(User)
    target = models.ForeignKey(User, related_name="target", db_index=True)

    watch_time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = [("user", "target")]

class Activity(models.Model):
    project = models.ForeignKey(Project)
    user = models.ForeignKey(User, null=True, blank=True)
    act_type = models.CharField(max_length=32, db_index=True)
    content = models.CharField(max_length=255, null=True, blank=True)
    ctime = models.DateTimeField(db_index=True)

class ReposChecker(models.Model):
    project = models.ForeignKey(Project, unique=True)
    last_rev = models.IntegerField()
    last_time = models.DateTimeField(auto_now=True, db_index=True)

class FeatureProject(models.Model):
    project = models.ForeignKey(Project, unique=True)
    desc = models.TextField()
    mtime = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.project.name

class OldProject(models.Model):
    oldid = models.IntegerField(db_index=True)
    name = models.CharField(max_length=32, unique=True)
    
    
    
    
class AliProject(models.Model):
    subject=models.TextField(max_length=200,null=True)
    project_owner = models.TextField(max_length=200,null=True)
    attend_users = models.TextField(max_length=500,null=True)
    content = models.TextField(max_length=2000,null=True)
    svnurl = models.TextField(max_length=200,null=True)
    siteurl=models.TextField(max_length=200,null=True)
    ctime = models.DateTimeField(auto_now_add=True)

   
    def __unicode__(self):
        return self.subject    

class AliProjectUser(models.Model):
    project = models.ForeignKey(AliProject)
    name = models.CharField(max_length=128)
   
    def __unicode__(self):
        return '%s - %s' %(self.name, self.project.subject)
        
"""
