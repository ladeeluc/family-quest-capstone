from django.views.generic import View
from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from useraccount.forms import LoginForm, SignupForm
from useraccount.models import UserAccount

from familystructure.models import Person, Relation

from website.base_views import GenericFormView
from website.forms import AddProfileForm

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

class Signup(GenericFormView):
    FormClass = SignupForm
    template_text = {"header":"Sign Up to Family Quest", "submit":"Get Started"}

    def _handle_submission(self, request, form):
        # Add another field to the SignupForm
        # Check those fields are the same

        # Make sure the database error when email is in use is:
        # - Caught
        # - Tell the user what happened
        UserAccount.objects.create_user(
            email=form.get('email'),
            password=form.get('password'),
        )
        user = authenticate(request,
            email=form.get('email'),
            password=form.get('password')
        )
        if user:
            login(request,user)
            return redirect('home')

### ---------------------------------------------------------------------------

@login_required # will go to log in page if not logged in 
def add_member(request):
    if request.method == "POST":
        form = AddProfileForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            member: Person = Person.objects.create( 
                first_name = data['first_name'],
                nickname = data['nickname'],    
                middle_name = data['middle_name'],
                last_name = data['last_name'],  
                title = data['title'],
                tagline = data['tagline'],
                birth_date = data['birth_date'],
                death_date = data['death_date'],
                is_claimed = data['is_claimed'],
                facts = data['facts'],
            )
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse('profile_view', args=(id,)))
    form = AddProfileForm()

    return render(request, "generic_form.html", {"form": form})