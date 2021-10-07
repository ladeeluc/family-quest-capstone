from django.contrib import admin
from socialmedia.models import CommentNotification, Post,Comment,Reaction,CommentNotification

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Reaction)
admin.site.register(CommentNotification)