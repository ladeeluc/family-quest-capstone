from django import forms
from useraccount.models import UserAccount

class LoginForm(forms.ModelForm):
    class Meta:
        model = UserAccount
        fields = ['email', 'password']

class SignupForm(forms.Form):
    email = forms.CharField(max_length=254, label='Email address')
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    def clean(self):
        if self.cleaned_data['password'] != self.cleaned_data['confirm_password']:
            self.add_error('password','')
            self.add_error('confirm_password','Passwords do not match. Please try again.')
        return self.cleaned_data
