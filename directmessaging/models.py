from django.db import models

from django.utils.translation import ugettext_lazy as _

class Chat(models.Model):
    """
    | Field    | Details         |
    | :------- | :-------------- |
    | members  | mtm UserAccount |
    | messages | mtm Message    |
    """
    members = models.ManyToManyField(
        'useraccount.UserAccount',
        verbose_name=_('members'),
    )

    messages = models.ManyToManyField(
        'directmessaging.Message',
        verbose_name=_('messages'),
        blank=True,
    )

    def __str__(self):
        return f"{' + '.join(str(u.person) for u in self.members.all())} ({len(self.messages.all())} messages)"

class Message(models.Model):
    """
    | Field    | Details         |
    | :------- | :-------------- |
    | content  | Textfield       |
    | sent_at  | DateTime        |
    | author   | fk UserAccount  |
    """
    content = models.TextField(
        _('content'),
        null=False,
        blank=False,
    )

    sent_at = models.DateTimeField(
        _('sent_at'),
        auto_now_add=True,
    )

    author = models.ForeignKey(
        'useraccount.UserAccount',
        verbose_name=_('author'),
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'[{self.sent_at.ctime()}] {self.author}: {self.content}'
