
from django import forms
from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

from useraccount.forms import LoginForm, SignupForm, AddPersonForm
from useraccount.models import UserAccount

from familystructure.models import Person, Relation

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

    def _handle_submission(self, request, form, raw_form):
        user = authenticate(request, email=form.get('email'), password=form.get('password'))
        if user:
            login(request, user)
            return redirect('home')
        else:
            raw_form.add_error(None, 'Incorrect email or password')
            raw_form.add_error('email', '')
            raw_form.add_error('password', '')

class Signup(GenericFormView):
    FormClass = SignupForm
    template_text = {"header":"Sign Up to Family Quest", "submit":"Get Started"}

    def _handle_submission(self, request, form_data, raw_form):
        user = None
        try:
            UserAccount.objects.create_user(
                email=form_data.get('email'),
                password=form_data.get('password'),
            )

            user = authenticate(request,
                email=form_data.get('email'),
                password=form_data.get('password')
            )
    
        except IntegrityError:
            raw_form.add_error('email', 'This email address is already in use.')
            raw_form.add_error('password', '')
            raw_form.add_error('confirm_password', '')
                
        if user:
            login(request, user)
            return redirect('claim_person')
    
class SignupPerson(GenericFormView):
    FormClass = AddPersonForm
    template_text = {"header":"Tell us About Yourself", "submit":"All Done"}

    def _precheck(self, request):
        if request.user.person is not None:
            return redirect('home')

    def _handle_submission(self, request, form_data, raw_form):
        # Find a matching person, or make a new one
        try:
            person = Person.objects.get(
                first_name=form_data['first_name'],
                middle_name=form_data['middle_name'],
                last_name=form_data['last_name'],
                birth_date=form_data['birth_date'],
            )
        except Person.DoesNotExist:
            person = Person.objects.create(**form_data)
        
        person.is_claimed = True
        person.save()
        request.user.person = person
        request.user.save()
        
        return redirect('home')