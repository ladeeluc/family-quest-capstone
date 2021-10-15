from django import forms

class BasePostForm(forms.Form):
    title = forms.CharField(max_length=50)

class TextPostForm(BasePostForm):
    content = forms.CharField(widget=forms.Textarea)

class ImagePostForm(BasePostForm):
    post_photo = forms.FileField()