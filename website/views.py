from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.models import User
from familystructure.models import Person
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import LoginForm, PostForm, SignupForm
from useraccount import UserAccount

# Create your views here.
class  UserProfileView (LoginRequiredMixin, View):

    def get(self, request, id):
        template_name = "user_detail.html"
        person = Person.objects.get(id=id)
        context = {"person": person}
        return render(request, template_name, context)

class FamilyCirclePostDetail (LoginRequiredMixin, View):

    def get(self, request, fam_cir_post_id):
        template_name = "fam_cir_post_detail.html"
        post = UserAccount.objects.filter(id=fam_cir_post_id).first()
        context = {"fam_cir_post": post}
        return render(request, template_name, context)