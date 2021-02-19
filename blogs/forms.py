from django import forms

from Core.models import *

class Article_form(forms.ModelForm):
    title = forms.Field(widget=forms.TextInput(attrs={'required':True,'placeholder':"Write your title here ...",'style':'font-size:13px;'}))
    tags = forms.Field(widget=forms.TextInput(attrs={'required':True,'placeholder':"Write comma (,) seperated tags here ...",'style':'font-size:13px;'}))
    
    class Meta:
        model = Articles
        fields = ('title','image','video','tags','facebook','instagram','quora','medium','twitter','other','content')