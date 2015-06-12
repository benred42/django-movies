from django import forms
from Movies.models import Rater
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)


class RaterForm(forms.ModelForm):
    class Meta:
        model = Rater
        fields = ("gender", "age", "occupation",)