from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
class SignUpForm(UserCreationForm):

    email = forms.EmailField(required=True,
                         label='Email',
                         error_messages={'exists': 'Oops'})
   
    first_name = forms.Field()
    last_name = forms.Field()
    class Meta:
        model = User
        fields = ("first_name", "last_name","email", "password1", "password2")