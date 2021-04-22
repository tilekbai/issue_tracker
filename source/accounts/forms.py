from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.core.validators import MinLengthValidator
from accounts.models import Profile


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


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "email"]
        labels = {"first_name": "Имя", "last_name": "Фамилия", "email": "Email"}


class ProfileChangeForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ["user"]
