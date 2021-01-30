from django import forms
from .models import *
class Quora_Form(forms.ModelForm):
    tags = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Tags (eg : Facebook, Interview, Queries etc.)','style':'height:40px; font-size:13px;'}), label=False)
    class Meta:
        model = Quora
        fields = ('title','tags')

class Other_Form(forms.ModelForm):
    title2= forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Write Your Title Here.','style':'height:40px; font-size:13px;'}), label=False)
    tags = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Tags (eg : Facebook, Interview, Queries etc.)','style':'height:40px; font-size:13px;'}), label=False)
    class Meta:
        model = Quora
        fields = ('title2','title','tags')

class Anwser_Form(forms.ModelForm):
    class Meta:
        model = Anwsers
        fields = ('anwser',)