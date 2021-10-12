
from django import forms
from django.views.generic import View
from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

from useraccount.forms import LoginForm, SignupForm, AddPersonForm
from useraccount.models import UserAccount

from familystructure.models import Person, Relation

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

    def _handle_submission(self, request, form):
        user = authenticate(request, email=form.get('email'), password=form.get('password'))
        if user:
            login(request, user)
            return redirect('home')
        else:
            self.add_error(None, 'Incorrect email or password')

class Signup(GenericFormView):
    FormClass = SignupForm
    template_text = {"header":"Sign Up to Family Quest", "submit":"Get Started"}

    def _handle_submission(self, request, form_data,raw_form):
        # Make sure the database error when email is in use is caught
        # Tell the user what happened
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
           raw_form.add_error('email','This email address is already in use.')
                
        if user:
            login(request,user)
            return redirect('home')
            
        

    
class SignupPerson(GenericFormView):
    pass

# @login_required # will go to log in page if not logged in 
# def add_member(request):
#     if request.method == "POST":
#         form = AddProfileForm(request.POST)
#         if form.is_valid():
#             data = form.cleaned_data
#             member: Person = Person.objects.create( 
#                 first_name = data['first_name'],
#                 nickname = data['nickname'],    
#                 middle_name = data['middle_name'],
#                 last_name = data['last_name'],  
#                 title = data['title'],
#                 tagline = data['tagline'],
#                 birth_date = data['birth_date'],
#                 death_date = data['death_date'],
#                 is_claimed = data['is_claimed'],
#                 facts = data['facts'],
#             )
#         if form.is_valid():
#             form.save()
#         return HttpResponseRedirect(reverse('profile_view', args=(id,)))
#     form = AddProfileForm()

#     return render(request, "generic_form.html", {"form": form})