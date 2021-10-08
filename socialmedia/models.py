from django.db import models
from django.utils.translation import ugettext_lazy as _
from socialmedia.base_models import BaseReaction, BaseNotification

class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        'useraccount.UserAccount',
        verbose_name=_('author'),
        on_delete=models.CASCADE,
    )
    family_circle = models.ForeignKey(
        'familystructure.FamilyCircle',
        verbose_name=_('family circle'),
        on_delete=models.CASCADE,
    )
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    body = models.TextField(max_length=140)
    date_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        'useraccount.UserAccount',
        related_name='comments_made',
        on_delete=models.CASCADE,
        null=True,
    )
    commented_on = models.ForeignKey(
        'socialmedia.Post',
        related_name='comments',
        on_delete=models.CASCADE,
        blank=True,
    )

    def __str__(self):
        return self.body

class PostReaction(BaseReaction):
    TARGET_MODEL = 'socialmedia.Post'
    target_post = models.ForeignKey(
        TARGET_MODEL,
        related_name='post_reactions',
        on_delete=models.CASCADE,
    )

class CommentReaction(BaseReaction):
    TARGET_MODEL = 'socialmedia.Comment'
    target = models.ForeignKey(
        TARGET_MODEL,
        related_name='comment_reactions',
        on_delete=models.CASCADE,
    )

class CommentNotification(BaseNotification):
    TARGET_MODEL = 'socialmedia.Comment'
    target = models.ForeignKey(
        TARGET_MODEL,
        related_name='comment_notifications',
        on_delete=models.CASCADE,
    )
