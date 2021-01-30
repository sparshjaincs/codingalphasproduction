from django import forms
from .models import *
class Notes_form(forms.ModelForm):
    
    class Meta:
        model = Note
        fields = ('heading','text')

