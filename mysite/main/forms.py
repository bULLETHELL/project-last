from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import widgets, ModelForm
from django.forms.widgets import TextInput, PasswordInput, DateInput
from .models import *

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'Password'}))

class RegisterProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('profilePhoneNumber',)

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('address', 'city', 'postalCode')

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user= super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_active = True
        if commit:
            user.save()
        return user
