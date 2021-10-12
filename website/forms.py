from django import forms
from django.forms import fields
from familystructure.models import Person,Relation
from useraccount.models import UserAccount


class AddProfileForm(forms.ModelForm):# creating form for user decide waht user can do
    class Meta:
        model = Person
        fields = [
            'first_name',
            'nickname',
            'middle_name',
            'last_name',
            'title',
            'tagline',
            'birth_date',
            'death_date',
            'is_claimed',
            'facts'
        ]