from django import forms
from familystructure.models import Person, Relation

class LoginForm(forms.Form):
    email = forms.EmailField()
    # this widget/plugin '.PasswordInput' hides the chars with '****'
    password = forms.CharField(widget=forms.PasswordInput)

class SignupForm(forms.Form):
    email = forms.EmailField()
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

class EditPersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = [
            'profile_photo',
            'first_name',
            'nickname',
            'middle_name',
            'last_name',
            'title',
            'tagline',
            'birth_date',
            'death_date',
            'facts',
        ]
    
    birth_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    death_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=False)

class EditUserForm(forms.Form):
    
    email = forms.EmailField()
    # this widget/plugin '.PasswordInput' hides the chars with '****'
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=False)
    
    def clean(self):
        if self.cleaned_data['password'] != self.cleaned_data['confirm_password']:
            self.add_error('password','')
            self.add_error('confirm_password','Passwords do not match. Please try again.')
        return self.cleaned_data
