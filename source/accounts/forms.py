from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.core.validators import MinLengthValidator


class MyUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2',
                  'first_name', 'last_name', 'email')
        field_classes = {'username': UsernameField}

    def clean(self):     
        cleaned_data = super().clean()   
        if cleaned_data.get('last_name') == "" and cleaned_data.get('first_name') ==  "":
            raise forms.ValidationError ("Хотя бы одно поле имени или фамилии должно быть заполненным")
