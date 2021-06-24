from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import widgets, ModelForm, ModelMultipleChoiceField
from django.forms.widgets import TextInput, PasswordInput, DateInput, HiddenInput, Textarea
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

class NewCustomFeedForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user')
        super(NewCustomFeedForm, self).__init__(*args, **kwargs)
        self.fields['owner'].widget = HiddenInput()
        self.fields['owner'].required = False
        self.fields['user_source'] = ModelMultipleChoiceField(queryset=Profile.objects.filter(profileUser=self._user).first().friendlist, required=False)
        self.fields['group_source'] = ModelMultipleChoiceField(queryset=Group.objects.filter(members=self._user), required=False)

    def save(self, commit=True):
        inst = super(NewCustomFeedForm, self).save(commit=False)
        inst.owner = self._user
        if commit:
            inst.save()
            self.save_m2m()
        return inst

    class Meta:
        model = CustomFeed
        fields = '__all__'

class NewPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user')
        super(NewPostForm, self).__init__(*args, **kwargs)
        self.fields['author'].widget = HiddenInput()
        self.fields['author'].required = False
        self.fields['score'].widget = HiddenInput()
        self.fields['content'].widget = Textarea(attrs={'class':'materialize-textarea', 'data-length':'500'})

    def save(self, commit=True):
        inst = super(NewPostForm, self).save(commit=False)
        inst.author = self._user
        if commit:
            inst.save()
        return inst

    class Meta:
        model = Post
        fields = '__all__'

class NewPostCommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user')
        self._parent_post = kwargs.pop('parent_post')
        super(NewPostCommentForm, self).__init__(*args, **kwargs)
        self.fields['author'].widget = HiddenInput()
        self.fields['author'].required = False
        self.fields['score'].widget = HiddenInput()
        self.fields['content'].widget = Textarea(attrs={'class':'materialize-textarea', 'data-length':'500'})
        self.fields['parent_post'].widget = HiddenInput()
        self.fields['parent_post'].required = False

    def save(self, commit=True):
        inst = super(NewPostCommentForm, self).save(commit=False)
        inst.author = self._user
        inst.parent_post = self._parent_post
        if commit:
            inst.save()
        return inst

    class Meta:
        model = PostComment
        fields = '__all__'
