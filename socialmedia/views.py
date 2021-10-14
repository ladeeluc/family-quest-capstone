import re
from django.views.generic import View
from django.shortcuts import redirect,render, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from website.base_views import BaseEndpoint, GenericFormView
from socialmedia.forms import AddPostForm
from socialmedia.models import (
    Chat,
    Message,
    MessageNotification,
    CommentNotification,
    Post,
)

from json import (
    loads as hydrate_json,
)




class ChatEndpoint(BaseEndpoint):

    def get(self, request, chat_id):
        """Get all messages in this chat"""
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

class NotifsEndpoint(BaseEndpoint):
    
    def get(self, request):
        """Get all of the current user's notifications"""
        messages = MessageNotification.objects.filter(target_user=request.user)
        comments = CommentNotification.objects.filter(target_user=request.user)
        return self.ok(request, {
            'notifs': sorted(
                [ m.json_serialize() for m in messages ]
                + [ c.json_serialize() for c in comments ],
                key=lambda n: n['created_at'],
                reverse=True,
            )
        })
    
    def delete(self, request):
        """Clear all of the current user's notifications"""
        MessageNotification.objects.filter(target_user=request.user).delete()
        CommentNotification.objects.filter(target_user=request.user).delete()
        return self.get(request)

class NotifsDetailEndpoint(BaseEndpoint):
    
    def delete(self, request, notif_slug):
        try:
            match = re.search(r'^([a-z]+)\-([0-9]+)$', notif_slug)
            if match is None:
                return self.not_ok()
            
            model, model_id = match.groups()
            model_id = int(model_id)

            if model == 'message':
                notif = MessageNotification.objects.get(id=model_id)
            elif model == 'comment':
                notif = CommentNotification.objects.get(id=model_id)
            
            if request.user == notif.target_user:
                notif.delete()
            else:
                return self.no_perms()

            messages = MessageNotification.objects.filter(target_user=request.user)
            comments = CommentNotification.objects.filter(target_user=request.user)
            return self.ok(request, {
                'notifs': sorted(
                    [ m.json_serialize() for m in messages ]
                    + [ c.json_serialize() for c in comments ],
                    key=lambda n: n['created_at'],
                    reverse=True,
                )
            })
        except MessageNotification.DoesNotExist:
            return self.not_found()
        except CommentNotification.DoesNotExist:
            return self.not_found()





#laura code
class CreatePostView(LoginRequiredMixin,GenericFormView):
    """creates post by user in db"""
    FormClass = AddPostForm
    template_text = {"header":"Create a Post", "submit":"Get Started"}

    def _precheck(self, request):
        if request.user.person is not None:
            return redirect('home')
    
    def _handle_submission(self, request, form_data, raw_form):
        post = Post.objects.create(**form_data, author=request.user )

    def get(self,request,post_id):
        post = Post.objects.filter(id=post_id).first()
        return render(request, 'post_view', {'post':post})

        
           















# class SignupPerson(GenericFormView):
#     FormClass = AddPersonForm
#     template_text = {"header":"Tell us About Yourself", "submit":"All Done"}

#     def _precheck(self, request):
#         if request.user.person is not None:
#             return redirect('home')

#     def _handle_submission(self, request, form_data, raw_form):
#         # Find a matching person, or make a new one
#         try:
#             person = Person.objects.get(
#                 first_name=form_data['first_name'],
#                 middle_name=form_data['middle_name'],
#                 last_name=form_data['last_name'],
#                 birth_date=form_data['birth_date'],
#             )
#         except Person.DoesNotExist:
#             person = Person.objects.create(**form_data)
        
#         person.is_claimed = True
#         person.save()
#         request.user.person = person
#         request.user.save()
        
#         return redirect('home')





# class PostDetailView(View):
#     def get(self,request,post_id):
#         post = Post.objects.filter(id=post_id).first()
#         return render(request, 'post_detail.html', {'post':post})
            # def get(self,request):
            #     form = ()
            # return render(request,"generic_form.html", {'form':form})
    # def post(self,request):
    #     form = GenericFormView(request.POST)
    #         if form_data.is_valid():
    #             data = form_data.cleaned_data
    #             post = Post.objects.create(
    #             body=form_data["body"], 
    #             creator=request.user 
    #             )