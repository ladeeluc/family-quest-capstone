from django import forms
from django.db.models import fields
from .models import Comment

class BasePostForm(forms.Form):
    title = forms.CharField(max_length=50)

class TextPostForm(BasePostForm):
    content = forms.CharField(widget=forms.Textarea)

class ImagePostForm(BasePostForm):
    post_photo = forms.FileField()

class AddCommentForm(forms.Form):
    body = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Comment...'}), label="Leave a comment")
    class Meta:
        model = Comment
        fields = ['body']