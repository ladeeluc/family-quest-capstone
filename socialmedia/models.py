from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone




class Post(models.Model):
    title= models.CharField(max_length=50)
    content= models.TextField()
    pub_date = models.DateTimeField(auto_now_add= True)
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    body = models.TextField(max_length=140)
    date_time = models.DateTimeField(default=timezone.now)
    comment_author= models.ForeignKey('useraccount.UserAccount', related_name='comment', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.body




