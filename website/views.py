
from django import forms
from django.db.models.query_utils import Q
from django.views.generic import View
from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

from useraccount.forms import ChooseRelatedPersonForm, EditUserForm, LoginForm, SignupForm, AddPersonForm, EditPersonForm
from useraccount.models import UserAccount

from familystructure.models import Person, Relation, FamilyCircle

from django.views.generic import View

from website.base_views import GenericFormView, PrefilledFormView

from socialmedia.models import Chat, Post, Comment, CommentNotification

from functools import reduce

from familystructure.mixins import PersonRequiredMixin
from socialmedia.forms import TextPostForm, ImagePostForm, AddCommentForm
from familystructure.models import FamilyCircle

from familystructure.forms import CreateFamilyCircleForm

class Home(PersonRequiredMixin, View):

    def get(self, request):
        return redirect('person_detail', request.user.person.id)
        # return render(request, 'index.html')

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
            return HttpResponseRedirect(request.GET.get('next', reverse('home')))
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
    
class SignupPerson(LoginRequiredMixin, GenericFormView):
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
            if person.is_claimed:
                raw_form.add_error(None, 'Your identity already exists in our database and has already been claimed by another user. Please contact an administrator if this is unexpected.')
                return
        except Person.DoesNotExist:
            person = Person.objects.create(**form_data)
        
        person.is_claimed = True
        person.save()
        request.user.person = person
        request.user.save()
        
        return HttpResponseRedirect(request.GET.get('next', reverse('person_detail', args=[person.id])))

class PersonDetail(LoginRequiredMixin, View):
    def get(self, request, person_id):
        try:
            person = Person.objects.get(id=person_id)
            return render(request, 'person_detail.html', {
                'person': person,
            })
        except Person.DoesNotExist:
            return redirect('home')

class PersonEdit(PersonRequiredMixin, PrefilledFormView):
    FormClass = EditPersonForm
    template_text = {"header":"Edit Person", "submit":"Save"}

    def _precheck(self, request, person_id):
        try:
            person = Person.objects.get(id=person_id)
            if (request.user.person != person and request.user not in person.query_managers()):
                return redirect('person_detail', person_id)
        except Person.DoesNotExist:
            return redirect('person_detail', person_id)

    def _get_prefilled_form(self, request, person_id):
        initial = vars(Person.objects.get(id=person_id))
        initial['facts'] = "\r\n".join(initial['facts'] or [])
        return self.FormClass(initial=initial)
        
    def _handle_submission(self, request, form_data, raw_form, person_id):
        person = Person.objects.get(id=person_id)
        if form_data['profile_photo']:
            person.profile_photo = form_data['profile_photo']
        person.first_name = form_data['first_name']
        person.nickname = form_data['nickname']
        person.middle_name = form_data['middle_name']
        person.last_name = form_data['last_name']
        person.title = form_data['title']
        person.tagline = form_data['tagline']
        person.birth_date = form_data['birth_date']
        person.death_date = form_data['death_date']
        person.facts = form_data['facts'].split("\r\n") if len(form_data['facts']) > 0 else ""
        person.save()
        return redirect('person_detail', person.id)

class PersonAddSpouse(PersonEdit):
    FormClass = ChooseRelatedPersonForm
    template_text = {"header":"Add Spouse", "submit":"Add"}

    def _get_prefilled_form(self, request, person_id):
        person = Person.objects.get(id=person_id) # exists by _precheck

        shared_circles = FamilyCircle.objects.filter(Q(members=request.user.person.id) | Q(members=person.id)).distinct()
        try:
            spouse_rels = person.relations_in.filter(is_upward=False).union(person.relations_out.filter(is_upward=False))
        except AttributeError:
            spouse_rels = Relation.objects.none()
        spouses = list(set(rel.target.id if rel.target != self else rel.source.id for rel in spouse_rels))
        choices = (
            Person.objects
                .filter(family_circles__in=shared_circles)
                .exclude(id__in=spouses)
                .distinct()
        )
        form = self.FormClass()
        form.fields['person'].queryset = choices
        self.template_text['header'] = f"Add Spouse to {person}"
        return form
        
    def _handle_submission(self, request, form_data, raw_form, person_id):
        person = Person.objects.get(id=person_id) # exists by _precheck
        Relation.objects.create(source=person, target=form_data['person'], is_upward=False)
        return redirect('family_navigator', person_id)

class PersonAddParent(PersonEdit):
    FormClass = ChooseRelatedPersonForm
    template_text = {"header":"Add Parent", "submit":"Add"}

    def _get_prefilled_form(self, request, person_id):
        person = Person.objects.get(id=person_id) # exists by _precheck

        shared_circles = FamilyCircle.objects.filter(Q(members=request.user.person.id) | Q(members=person.id)).distinct()
        try:
            parent_rels = person.relations_out.filter(is_upward=True)
        except AttributeError:
            parent_rels = Relation.objects.none()
        parents = list(set(rel.target.id if rel.target != self else rel.source.id for rel in parent_rels))
        choices = (
            Person.objects
                .filter(family_circles__in=shared_circles)
                .exclude(id__in=parents)
                .distinct()
        )
        form = self.FormClass()
        form.fields['person'].queryset = choices
        self.template_text['header'] = f"Add Parent to {person}"
        return form
        
    def _handle_submission(self, request, form_data, raw_form, person_id):
        person = Person.objects.get(id=person_id) # exists by _precheck
        Relation.objects.create(source=person, target=form_data['person'], is_upward=True)
        return redirect('family_navigator', person_id)

class FamilyCircles(PersonRequiredMixin, View):

    def get(self, request):
        return render(request, 'family_circles.html')

class FamilyCircleDetail(PersonRequiredMixin, View):

    def get(self, request, circle_id):
        circle = FamilyCircle.objects.get(id=circle_id)
        if request.user.person not in circle.members.all():
            return redirect('home')
        return render(request, 'circle_detail.html', {"circle":circle})

class FamilyCircleManage(LoginRequiredMixin, View):

    def get(self, request, circle_id):
        circle = FamilyCircle.objects.get(id=circle_id)
        if request.user not in circle.managers.all():
            return redirect('home')
        return render(request, 'circle_manage.html', {"circle":circle})

class FamilyCircleAddPerson(LoginRequiredMixin, GenericFormView):
    FormClass = AddPersonForm
    template_text = {"header":"Add Someone to Your Circle", "submit":"Add"}

    def _precheck(self, request, circle_id, *args, **kwargs,):
        try:
            circle = FamilyCircle.objects.get(id=circle_id)
            self.template_text['header'] = f'Add Someone to {circle.name}'
        except FamilyCircle.DoesNotExist:
            return redirect('home')

        if request.user.person is None or request.user.person.family_circles is None:
            return redirect('home')

    def _handle_submission(self, request, form_data, raw_form, circle_id):
        circle = FamilyCircle.objects.get(id=circle_id) # covered by _precheck
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
        
        if person not in circle.members.all():
            circle.members.add(person)
            return redirect('circle_manage', circle_id)
        else:
            raw_form.add_error(None, 'This person is already in the family circle')
            raw_form.add_error('first_name', '')
            raw_form.add_error('middle_name', '')
            raw_form.add_error('last_name', '')
            raw_form.add_error('birth_date', '')

class CreateFamilyCircle(PersonRequiredMixin, GenericFormView):
    FormClass = CreateFamilyCircleForm
    template_text = {"header":"Create a Family Circle", "submit":"Create"}

    def _handle_submission(self, request, form_data, raw_form, *args, **kwargs):
        family = FamilyCircle.objects.create(**form_data)

        family.managers.add(
            request.user
        )
        family.members.add(
            request.user.person
        )
        return redirect('circle_detail', family.id)

class UserEdit(LoginRequiredMixin, PrefilledFormView):
    FormClass = EditUserForm
    template_text = {"header":"Settings", "submit":"Save"}

    def _get_prefilled_form(self, request):
        return self.FormClass(initial={
            'email': request.user.email,
            'password': 'None',
            'confirm_password': 'None',
        })
    
    def _handle_submission(self, request, form_data, raw_form, *args, **kwargs):
        try:
            request.user.email = form_data['email']
            if form_data['password']:
                request.user.set_password(form_data['password'])
            request.user.save()
            user = authenticate(request, email=form_data['email'], password=form_data['password'])
            if user:
                login(request, user)
        except IntegrityError:
            raw_form.add_error('email', 'This email address is already in use.')
            raw_form.add_error('password', '')
            raw_form.add_error('confirm_password', '')

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
        if request.user not in chat.members.all():
            return redirect('home')
        context = {
            "chat":chat,
            "members":", ".join([str(m) for m in chat.members.exclude(id=request.user.id)]),
            }
        return render(request, 'chat.html', context)

class CreatePost(PersonRequiredMixin, View):
    
    def get(self, request, circle_id):
        return self._render_template(request, circle_id, None, "text")
    
    def _render_template(self, request, circle_id, form, post_type):
        circle = FamilyCircle.objects.get(id=circle_id)
        if request.user.person not in circle.members.all():
            return redirect('home')
        return render(request, 'create_post.html', {
            "text_form":form or TextPostForm() if post_type == "text" else TextPostForm(),
            "image_form":form or ImagePostForm() if post_type == "image" else ImagePostForm(),
            f"{post_type}_link_class":"active",
            f"{post_type}_form_class":"show active",
            "family_circle":circle
        })
    
    def post(self, request, circle_id):
        post_type = request.GET.get("type")
        
        if post_type == "text":
            form = TextPostForm(request.POST)
        elif post_type == "image":
            form = ImagePostForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            post = Post.objects.create(
                title=data.get("title"),
                content=data.get("content"),
                post_photo=data.get("post_photo"),
                author=request.user,
                family_circle=FamilyCircle.objects.get(id=circle_id)
            )
            return redirect(reverse('post_detail', args=[post.id]))
        return self._render_template(request, circle_id, form, post_type)
        
class PostDetail(PersonRequiredMixin, View):

    def get(self, request, post_id):
        try:
            template_name = "post_detail.html"
            #Get post from post id
            post = Post.objects.get(id=post_id)
           #Get comments from post
            context = {
                'post': post,
                'comments': post.comments.all(),
                'form': AddCommentForm()
            }
            return render(request, template_name, context)
        except Post.DoesNotExist:
            return redirect('home')

    def post(self, request, post_id):
        try:
            template_name = "post_detail.html"
            #Get post from post id
            post = Post.objects.get(id=post_id)
            form = AddCommentForm(request.POST)
            if form.is_valid():
                comment = Comment.objects.create(
                    **form.cleaned_data,
                    author=request.user,
                    commented_on=post,
                )
                CommentNotification.objects.create(
                    target_user=post.author,
                    target_comment=comment
                )

            return redirect('post_detail', post_id)
        except Post.DoesNotExist:
            return redirect('home')

class FamilyNavigator(PersonRequiredMixin, View):
    
    def get(self, request, person_id):
        person = Person.objects.get(id=person_id)
        return render(request, 'family_navigator.html', {
            "person":person,
        })