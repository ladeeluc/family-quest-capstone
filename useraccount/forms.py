from django import forms
from familystructure.models import Person, Relation
from useraccount.models import UserAccount
from django.core.validators import validate_email

class LoginForm(forms.Form):
    email = forms.CharField(max_length=50)
    # this widget/plugin '.PasswordInput' hides the chars with '****'
    password = forms.CharField(widget=forms.PasswordInput)

class SignupForm(forms.Form):
    email = forms.CharField(max_length=50)
    # this widget/plugin '.PasswordInput' hides the chars with '****'
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)


    
    def clean(self):
        if self.cleaned_data['password'] != self.cleaned_data['confirm_password']:
            self.add_error('password','')
            self.add_error('confirm_password','Passwords do not match. Please try again.')
        return self.cleaned_data



class AddPersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = [
            'first_name',
            'middle_name',
            'last_name',
            'birth_date',
        ]
    
    birth_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))    