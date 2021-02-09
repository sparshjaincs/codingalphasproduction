from django import forms

from Core.models import *

class Article_form(forms.ModelForm):
    title = forms.Field(widget=forms.TextInput(attrs={'required':True,'placeholder':"Write your title here ...",'style':'font-size:13px;'}))
    tags = forms.Field(widget=forms.TextInput(attrs={'required':True,'placeholder':"Write comma (,) seperated tags here ...",'style':'font-size:13px;'}))
    facebook = forms.Field(widget=forms.TextInput(attrs={'placeholder':"Facebook Link",'style':'font-size:13px;'}))
    medium = forms.Field(widget=forms.TextInput(attrs={'placeholder':"Medium Link",'style':'font-size:13px;'}))
    quora = forms.Field(widget=forms.TextInput(attrs={'placeholder':"Quora Link",'style':'font-size:13px;'}))
    instagram = forms.Field(widget=forms.TextInput(attrs={'placeholder':"Instagram Link",'style':'font-size:13px;'}))
    twitter = forms.Field(widget=forms.TextInput(attrs={'placeholder':"Twitter Link",'style':'font-size:13px;'}))
    other = forms.Field(widget=forms.TextInput(attrs={'placeholder':"Others",'style':'font-size:13px;'}))
   
    class Meta:
        model = Articles
        fields = ('title','image','video','tags','facebook','instagram','quora','medium','twitter','other','content')