from django.db import models

from django.utils.translation import ugettext_lazy as _

class Chat(models.Model):
    """
    | Field    | Details         |
    | :------- | :-------------- |
    | members  | mtm Useraccount |
    | messages | mtm Message    |
    """
    members = models.ManyToManyField(
        'useraccount.UserAccount',
        verbose_name=_('members'),
    )

    messages = models.ManyToManyField(
        'directmessaging.Message',
        verbose_name=_('messages'),
    )

class Message(models.Model):
    """
    | Field    | Details         |
    | :------- | :-------------- |
    | content  | Textfield       |
    | author   | fk Useraccount  |
    """
    content = models.TextField(
        _('content'),
        null=False,
        blank=False,
    )

    author = models.ForeignKey(
        'useraccount.Useraccount',
        verbose_name=_('author'),
        on_delete=models.CASCADE,
    )
