from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin

from useraccount.forms import LoginForm, SignupForm
from useraccount.models import UserAccount

from django.views.generic import View
from website.base_views import GenericFormView



class Home(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'index.html')

class Logout(View):

    def get(self, request):
        logout(request)
        return redirect('home')

class Login(GenericFormView):
    FormClass = LoginForm
    template_text = {"header":"Log In to Family Quest", "submit":"Log In"}

    def _handle_submission(self, request, data):
        user = authenticate(request, email=data.get('email'), password=data.get('password'))
        if user:
            login(request, user)
            return redirect('home')

class Signup(GenericFormView):
    FormClass = SignupForm
    template_text = {"header":"Sign Up to Family Quest", "submit":"Get Started"}

    def _handle_submission(self, request, data):
        UserAccount.objects.create_user(
            email=form.cleaned_data.get('email'),
            password=form.cleaned_data.get('password'),
        )
        user = authenticate(request,
            email=form.cleaned_data.get('email'),
            password=form.cleaned_data.get('password')
        )
        if user:
            login(request,user)
            return redirect('home')