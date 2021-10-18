from django import forms
from familystructure.models import FamilyCircle

class CreateFamilyCircleForm(forms.ModelForm):

    class Meta:
        model = FamilyCircle
        fields = ["name"] 