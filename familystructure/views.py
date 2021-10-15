
import re
from django.views.generic import View
from django.shortcuts import redirect,render, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from website.base_views import BaseEndpoint, GenericFormView
from socialmedia.forms import AddPostForm
from familystructure.models import Person
from socialmedia.models import (
    Chat,
    Message,
    MessageNotification,
    CommentNotification,
    Post,
)
#laura code
class FamilyCirclePostView(LoginRequiredMixin, View):
    def get(self, request):
        try:
            posts = Post.objects.all()
            return render(request, 'family_posts.html', {'posts':posts})
        except Post.DoesNotExist:
            return redirect('home')

class FamilyCircleListView(LoginRequiredMixin,View):
     def get(self,request):
         try:
             family_members = Person.objects.all()
             return render(request, 'family_members.html', {'family_members':family_members})
         except Person.DoesNotExist:
             return redirect ('home')
        



