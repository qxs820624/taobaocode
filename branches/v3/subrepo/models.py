from django.db import models

USER_DISABLE = 0
USER_ENABLE = 1
USER_DELETED = 2

PROJECT_DISABLE = 0
PROJECT_ENABLE = 1
PROJECT_MARK_DELETED = 2
PROJECT_TRUE_DELETED = 3

ISSUE_OPEN = 0
ISSUE_CLOSED = 1
ISSUE_DELETED = 2

COMMENT_ENABLE = 1
COMMENT_DELETED = 0

FILE_ENABLE = 1
FILE_DELETED = 0

WIKI_ENABLE = 1
WIKI_DELETED = 0

PM_SEND_INV = 0
PM_ACCEPT_INV = 1
PM_REJECT_INV = 2

MSG_INBOX = 1
MSG_OUTBOX = 2
MSG_TRASH = 3

MSG_SENDER_OUTBOX = 1
MSG_SENDER_TRASHBOX = 2

MSG_READER_INBOX = 3
MSG_READER_TRASHBOX = 4
MSG_DELETED = 5


class User(models.Model):
    name = models.CharField(max_length=40, unique=True)
    email = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=128)

    status = models.SmallIntegerField(db_index=True, choices=[
        (USER_DISABLE, 'Disable'),
        (USER_ENABLE, 'Enable'),
        (USER_DELETED, 'Deleted'),
    ])
    ctime = models.DateTimeField(auto_now_add=True)
    last_login_ip = models.CharField(max_length=32)
    last_login = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.status == USER_ENABLE

    def get_and_delete_messages(self):
        return []

    def is_staff(self):
        return self.supper

    def has_perm(self, label):
        return self.supper

    def has_module_perms(self, label):
        return self.supper


class Message(models.Model):
    owner = models.ForeignKey(User)
    sender = models.ForeignKey(User,
                               related_name="sender",
                               null=True)

    is_read = models.BooleanField()
    sender_status = models.SmallIntegerField()
    reader_status = models.SmallIntegerField()

    content = models.CharField(max_length=1024)

    send_time = models.DateTimeField(auto_now_add=True)
    read_time = models.DateTimeField(null=True, blank=True)


class ReposPart(models.Model):
    prefix = models.CharField(max_length=128)
    can_new = models.BooleanField(db_index=True)
    count = models.IntegerField(db_index=True)
    ctime = models.DateTimeField(auto_now_add=True)
    mtime = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '%s - can_new(%s) count(%s)' % (self.prefix,
                                               self.can_new,
                                               self.count)


class Project(models.Model):
    owner = models.ForeignKey(User)

    name = models.CharField(max_length=32, unique=True)
    title = models.CharField(max_length=200, null=True)
    status = models.SmallIntegerField(db_index=True, choices=[
        (PROJECT_DISABLE, 'Disable'),
        (PROJECT_ENABLE, 'Enable'),
        (PROJECT_MARK_DELETED, 'Mark Deleted'),
        (PROJECT_TRUE_DELETED, 'True Deleted')
    ])
    ctime = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField()
    part = models.ForeignKey(ReposPart, null=True)

    def __unicode__(self):
        return self.name


class ProjectProfile(models.Model):
    project = models.ForeignKey(Project)
    name = models.CharField(max_length=32, unique=True)
    value = models.CharField(max_length=1024)


class ProjectMember(models.Model):
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    member_type = models.SmallIntegerField(choices=[
        (PM_SEND_INV, 'Send invitation'),
        (PM_ACCEPT_INV, 'Accept invitation'),
        (PM_REJECT_INV, 'Reject invitation'),
    ])
    join_time = models.DateTimeField(auto_now_add=True)
    mtime = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [("user", "project")]


class ProjectWatcher(models.Model):
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    watch_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("user", "project")]


class Issue(models.Model):
    project = models.ForeignKey(Project)
    creator = models.ForeignKey(User,
                                related_name="creator",
                                null=True)
    title = models.CharField(max_length=200)
    content = models.TextField(null=True)
    status = models.SmallIntegerField(db_index=True, choices=[
        (ISSUE_OPEN, 'Open'),
        (ISSUE_CLOSED, 'Closed'),
        (ISSUE_DELETED, 'Deleted')
    ])
    vote_count = models.IntegerField(blank=True)
    ctime = models.DateTimeField(auto_now_add=True)
    mtime = models.DateTimeField(auto_now=True)

    def closed(self):
        return self.status == ISSUE_CLOSED

    def __unicode__(self):
        return self.title


class IssueComment(models.Model):
    issue = models.ForeignKey(Issue)
    owner = models.ForeignKey(User)
    content = models.TextField()
    status = models.SmallIntegerField(choices=[
        (COMMENT_ENABLE, 'Enable'),
        (COMMENT_DELETED, 'Deleted')
    ])
    ctime = models.DateTimeField(auto_now_add=True)
    mtime = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.content


class WikiContent(models.Model):
    project = models.ForeignKey(Project)
    user = models.ForeignKey(User)
    last_user = models.ForeignKey(User, related_name="last_user")

    path = models.CharField(max_length=255, db_index=True)
    content = models.TextField()
    status = models.SmallIntegerField(choices=[
        (WIKI_ENABLE, 'Enable'),
        (WIKI_DELETED, 'Deleted')])

    ctime = models.DateTimeField(auto_now_add=True)
    mtime = models.DateTimeField(auto_now=True)

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
    status = models.SmallIntegerField(choices=[
        (FILE_ENABLE, 'Enable'),
        (FILE_DELETED, 'Deleted')])
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
    code = models.CharField(max_length=32, unique=True)  # md5code
    name = models.CharField(max_length=255, db_index=True)
    data = models.CharField(max_length=255)

    is_done = models.BooleanField()
    ctime = models.DateTimeField(auto_now_add=True, db_index=True)
    expire_time = models.DateTimeField()


class UserWatcher(models.Model):
    user = models.ForeignKey(User)
    target = models.ForeignKey(User,
                               related_name="target",
                               db_index=True)

    watch_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("user", "target")]


class Activity(models.Model):
    project = models.ForeignKey(Project)
    user = models.ForeignKey(User, null=True, blank=True)
    act_type = models.CharField(max_length=32, db_index=True)
    content = models.CharField(max_length=255, null=True, blank=True)
    ctime = models.DateTimeField(db_index=True)


class FeatureProject(models.Model):
    project = models.ForeignKey(Project, unique=True)
    desc = models.TextField()
    mtime = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.project.name
