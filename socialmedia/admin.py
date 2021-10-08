from django.contrib import admin
from socialmedia.models import Post, Comment, Reaction, CommentNotification

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Reaction)
admin.site.register(CommentNotification)