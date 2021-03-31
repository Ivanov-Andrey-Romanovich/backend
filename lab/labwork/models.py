from django.db.models import *
from django.contrib.auth.models import User
class Blog(Model):
    title = CharField('Title',max_length = 80)
    created_at = DateTimeField('creation time',auto_now_add = True)
    author = ForeignKey(User, on_delete = CASCADE, default = 1)
    def __str__(self):
        return str(self.title)

class Post(Model):
    blog = ForeignKey(Blog,on_delete = CASCADE)
    subject = CharField('Subject',max_length = 80)
    text = TextField(max_length = 4096)
    created_at = DateTimeField('creation time',auto_now_add = True)
    updated_at = DateTimeField('update time',auto_now = True)
    def __str__(self):
        return str(self.subject)
