from django.db import models
from django.utils.translation import ugettext_lazy as _

class BaseNotification(models.Model):
    """
    To extend:
    Assign a model string to `TARGET_MODEL`

    Paste in:
    ```
    target = models.ForeignKey(
        TARGET_MODEL,
        related_name='target',
        on_delete=models.CASCADE,
    )
    ```
    """
    TARGET_MODEL = None
    target_author = models.ForeignKey(
        'useraccount.UserAccount',
        related_name='target_author',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        t = self.TARGET_MODEL.split('.')[1]
        return f'Notif for {self.target_author.person} about {t} {self.target}'

class BaseReaction(models.Model):
    """
    To extend:
    Assign a model string to `TARGET_MODEL`

    Paste in:
    ```
    target = models.ForeignKey(
        TARGET_MODEL,
        related_name='target',
        on_delete=models.CASCADE,
    )
    ```
    """

    class ReactionType(models.TextChoices):
            HEART = 'heart', _('Heart'),
            SMILEY = 'smiley', _('Smiley'),
            THUMBS_UP = 'thumbs_up', _('Thumbs_up')

    reaction_type = models.CharField(
        max_length=12,
        choices=ReactionType.choices,
        default=ReactionType.THUMBS_UP,
    )
    reactor = models.ForeignKey(
        'useraccount.UserAccount',
        related_name='reactor',
        on_delete=models.CASCADE,
    )
    

    def __str__(self):
        t = self.TARGET_MODEL.split('.')[1]
        return f'{self.reactor.person} reacted to a {t} with a {self.reaction_type}'