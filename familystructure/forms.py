from django import forms
from familystructure.models import FamilyCircle

class AddFamilyForm(forms.ModelForm):

    class Meta:
        model = FamilyCircle
        fields = ["name"]