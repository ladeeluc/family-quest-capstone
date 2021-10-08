from django.contrib import admin
from socialmedia.models import Post, PostReaction, Comment, CommentReaction, CommentNotification

admin.site.register(Post)
admin.site.register(PostReaction)
admin.site.register(Comment)
admin.site.register(CommentReaction)
admin.site.register(CommentNotification)