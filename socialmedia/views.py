from website.base_views import BaseEndpoint
from socialmedia.models import (
    Chat,
    Message,
    MessageReaction,
    MessageNotification,
)

from json import (
    loads as hydrate_json,
)

class ChatEndpoint(BaseEndpoint):

    def get(self, request, chat_id):
        """Get all messages in this chat"""
        try:
            return self.ok({
                'messages': [
                {
                    'content': message.content,
                    'sent_at': message.sent_at,
                    'author': message.author,
                    'reactions': [
                        {
                            'reaction_type': reaction.reaction_type,
                            'reactor': reaction.reactor,
                        } for reaction in message.reactions.all()
                    ],
                } for message in Chat.objects.get(id=chat_id).messages.all()
            ],
            })
        except Chat.DoesNotExist:
            return self.not_found()
    
    def post(self, request, chat_id):
        """
        Send a new message to this chat, making the necessary notifications

        Expected JSON:
        ```js
        {
            "content": String,
        }
        ```
        """
        json = hydrate_json(request.body)
        try:
            chat = Chat.objects.get(id=chat_id)
            message = Message.objects.create(
                content=json['content'],
                author=request.user,
            )
            for user in chat.members.all():
                if user != request.user:
                    MessageNotification.objects.create(
                        target_user=user,
                        target_message=message,
                    )
            return self.done()
        except Chat.DoesNotExist:
            return self.not_found()
        
