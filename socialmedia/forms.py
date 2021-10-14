from django import forms
from familystructure.models import Person, Relation
from socialmedia.models import Post
from useraccount.models import UserAccount


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title', 
            'content',
            'post_photo',
            'created_at',
            'author ',
            'family_circle' 
        ]
    
    # birth_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))