from website.base_views import BaseEndpoint
from socialmedia.models import (
    Chat,
    Message,
    MessageNotification,
)

from json import (
    loads as hydrate_json,
)

class ChatEndpoint(BaseEndpoint):

    def get(self, request, chat_id):
        """
        Get all messages in this chat
        """
        try:
            chat = Chat.objects.get(id=chat_id)        
            if request.user not in chat.members.all():
                return self.no_perms()
            return self.ok(request, chat.json_serialize())
        except Chat.DoesNotExist:
            return self.not_found()
    
    def post(self, request, chat_id):
        """
        Send a new message to this chat, making the necessary notifications
        Needs `X-CSRFToken` header set
        """
        json = hydrate_json(request.body)
        try:
            chat = Chat.objects.get(id=chat_id)
            members = chat.members.all()
            if request.user not in members:
                return self.no_perms()
            
            message = Message.objects.create(
                content=json['content'],
                author=request.user,
                chat=chat,
            )
            for user in members:
                if user != request.user:
                    MessageNotification.objects.create(
                        target_user=user,
                        target_message=message,
                    )
            return self.done(request, chat.json_serialize())
        except Chat.DoesNotExist:
            return self.not_found()
        except KeyError:
            return self.not_ok()