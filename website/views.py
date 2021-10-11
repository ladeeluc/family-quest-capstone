from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.models import User
from familystructure.models import Person
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import LoginForm, PostForm, SignupForm

# Create your views here.
class  UserProfileView (LoginRequiredMixin, View):

    def get(self, request, id):
        template_name = "user_detail.html"
        person = Person.objects.get(id=id)
        context = {"person": person}
        return render(request, template_name, context)