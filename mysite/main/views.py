from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import NewUserForm, RegisterProfileForm, AddressForm, LoginForm
from .models import *

# Create your views here.
def homepage(request):
    default_feed_posts = []
    if request.user.is_authenticated:
        default_feed = CustomFeed.objects.filter(owner=request.user).filter(name='default')
        for user_query_set in [feed.user_source.all() for feed in default_feed]:
            for user in user_query_set:
                user_post = Post.objects.filter(author=user.id)
                default_feed_posts.append(user_post)
        for group_user_query_set in [feed.group_source.all() for feed in default_feed]:
            for user in group_user_query_set:
                user_group_post = Post.objects.filter(author=user.id)
                default_feed_posts.append(user_group_post)

    return render(request = request,
                  template_name = "homepage.html",
                  context={'register_user_form': NewUserForm,
                            'register_profile_form': RegisterProfileForm,
                            'address_form': AddressForm,
                            'login_form': LoginForm,
                            'default_feed_posts': default_feed_posts})

def profile(request):
    return render(request = request,
                  template_name = 'profile.html',
                  context={'register_user_form': NewUserForm,
                            'register_profile_form': RegisterProfileForm,
                            'address_form': AddressForm,
                            'login_form': LoginForm})

def register(request):
    if request.method == 'POST':
        new_user_form = NewUserForm(request.POST)
        register_profile_form = RegisterProfileForm(request.POST)
        address_form = AddressForm(request.POST)
        print(new_user_form.errors.as_data())
        print(register_profile_form.errors.as_data())
        print(address_form.errors.as_data())

        if new_user_form.is_valid() and register_profile_form.is_valid() and address_form.is_valid():
            user = new_user_form.save()
            address = address_form.save()
            user.profile.profilePhoneNumber = request.POST['profilePhoneNumber']
            user.profile.profileAddress = address

            user.save()
            username = new_user_form.cleaned_data.get('username')
            login(request, user)

            return redirect('main:homepage')

    user_creation_form = UserCreationForm

    return render(request=request,
                  template_name='homepage.html',
                  context={'user_creation_form': user_creation_form})

def login_request(request):
    if request.method == 'POST':
        login_form = LoginForm(request=request, data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
    return redirect('main:homepage')

def logout_request(request):
    logout(request)
    return redirect('main:homepage')

