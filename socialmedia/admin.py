from django.contrib import admin
from socialmedia.models import (
    Post,
    PostReaction,
    Comment,
    CommentReaction,
    CommentNotification,
    Chat,
    Message,
    MessageReaction,
    MessageNotification,
)

admin.site.register(Post)
admin.site.register(PostReaction)
admin.site.register(Comment)
admin.site.register(CommentReaction)
admin.site.register(CommentNotification)
admin.site.register(Chat)
admin.site.register(Message)
admin.site.register(MessageReaction)
admin.site.register(MessageNotification)

