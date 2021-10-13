
from django import forms
from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

from useraccount.forms import EditUserForm, LoginForm, SignupForm, AddPersonForm, EditPersonForm
from useraccount.models import UserAccount

from familystructure.models import Person, Relation, FamilyCircle

from django.views.generic import View

from website.base_views import GenericFormView, PrefilledFormView

from socialmedia.models import Chat

from functools import reduce

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
            raw_form.add_error('email', 'This email address is already in use.')
            raw_form.add_error('password', '')
            raw_form.add_error('confirm_password', '')
                
        if user:
            login(request, user)
            return redirect('claim_person')
    
class SignupPerson(GenericFormView):
    FormClass = AddPersonForm
    template_text = {"header":"Tell us About Yourself", "submit":"All Done"}

    def _precheck(self, request, *args, **kwargs):
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

class PersonDetail(View):
    def get(self, request, person_id):
        try:
            person = Person.objects.get(id=person_id)
            return render(request, 'person_detail.html', {
                'person': person,
            })
        except Person.DoesNotExist:
            return redirect('home')

class PersonEdit(PrefilledFormView):
    FormClass = EditPersonForm
    template_text = {"header":"Edit Person", "submit":"Save"}

    def _precheck(self, request, person_id):
        if not request.user.person:
            return redirect('person_detail', person_id)
        try:
            person = Person.objects.get(id=person_id)
            circles = person.family_circles.all().intersection(
                request.user.person.family_circles.all()
            )
            is_not_manager = all(
                request.user not in mgrs for mgrs in
                [fc.managers.all() for fc in circles]
            )
            if (request.user.person != person and is_not_manager):
                return redirect('person_detail', person_id)
        except Person.DoesNotExist:
            return redirect('person_detail', person_id)

    def _get_prefilled_form(self, request, person_id):
        return self.FormClass(vars(Person.objects.get(id=person_id)))
        
    def _handle_submission(self, request, form_data, raw_form, person_id):
        person = Person.objects.get(id=person_id)
        person.profile_photo = form_data['profile_photo']
        person.first_name = form_data['first_name']
        person.nickname = form_data['nickname']
        person.middle_name = form_data['middle_name']
        person.last_name = form_data['last_name']
        person.title = form_data['title']
        person.tagline = form_data['tagline']
        person.birth_date = form_data['birth_date']
        person.death_date = form_data['death_date']
        person.facts = form_data['facts']
        person.save()
        return redirect('person_detail', person.id)
        

class UserEdit(PrefilledFormView):
    FormClass = EditUserForm
    template_text = {"header":"Settings", "submit":"Save"}

    def _get_prefilled_form(self, request):
        return self.FormClass({
            'email': request.user.email,
            'password': 'None',
            'confirm_password': 'None',
        })
    
    def _handle_submission(self, request, form_data, raw_form, *args, **kwargs):
        request.user.email = form_data['email']
        if form_data['password']:
            request.user.set_password(form_data['password'])
        request.user.save()

class AllChats(LoginRequiredMixin, View):
    
    def get(self, request):
        chatobjs = Chat.objects.filter(members__in=[request.user])
        chats = []
        # include only chats that have at least 1 message
        for chat in [c for c in chatobjs if c.messages.count() >= 1]:
            circles = []
            members = chat.members.all()
            # if all members in a chat have people, find the intersection of their family circles
            if all([bool(m.person) for m in members]):
                circles = [set(m.person.family_circles.all()) for m in members]
                circles = reduce(lambda a, b: a & b, circles)
            # serialize chat to object for template
            chats.append({
                "id":chat.id,
                "latestmessage":chat.messages.order_by('sent_at').last(),
                "members":[str(m) for m in chat.members.exclude(id=request.user.id)],
                "circles": circles
            })
        # sort by latest message date first
        chats = reversed(sorted(chats, key=lambda x: x['latestmessage'].sent_at.isoformat()))
        return render(request, 'chats.html', {"chats":chats})

class SingleChat(LoginRequiredMixin, View):

    def get(self, request, chat_id):
        chat = Chat.objects.get(id=chat_id)
        context = {
            "chat":chat,
            "members":", ".join([str(m) for m in chat.members.exclude(id=request.user.id)]),
            }
        return render(request, 'chat.html', context)
