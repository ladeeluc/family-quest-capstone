from django.db import models
from django.utils.translation import ugettext_lazy as _

class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    body = models.TextField(max_length=140)
    date_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('useraccount.UserAccount', related_name='author', on_delete=models.CASCADE, null=True)
    post_comment_added = models.ForeignKey('socialmedia.Post', related_name='post_comment_added', on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.body

class Reaction(models.Model):
    class ReactionType(models.TextChoices):
            HEART = 'heart', _('Heart'),
            SMILEY = 'smiley', _('Smiley'),
            THUMBS_UP = 'thumbs_up', _('Thumbs_up')

    reaction_type = models.CharField(
        max_length=12,
        choices=ReactionType.choices,
        default=ReactionType.DEFAULT,
    )


    post_reaction = models.ForeignKey('Post', related_name='post_reaction', on_delete=models.CASCADE, blank=True)

    def __int__(self):
        return self.post_reaction

class CommentNotification(models.Model):
    author_inform = models.ForeignKey('useraccount.UserAccount', related_name='author_inform', on_delete=models.CASCADE)
    post_notify = models.ForeignKey('socialmedia.Post', related_name='post_notify', on_delete=models.CASCADE)

    def __int__(self):
        return self.author_inform

