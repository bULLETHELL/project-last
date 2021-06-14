from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import NewUserForm, RegisterProfileForm, AddressForm, LoginForm, NewCustomFeedForm, NewPostForm
from .models import *

# Create your views here.
def homepage(request):
    default_feed_posts = []
    current_user_custom_feeds = []
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
        current_user_custom_feeds = CustomFeed.objects.filter(owner=request.user).exclude(name='default')

        return render(request = request,
                      template_name = "homepage.html",
                      context={'register_user_form': NewUserForm,
                               'register_profile_form': RegisterProfileForm,
                               'address_form': AddressForm,
                               'login_form': LoginForm,
                               'new_custom_feed_form': NewCustomFeedForm(user=request.user),
                               'new_post_form': NewPostForm(initial={'score': 0}, user=request.user),
                               'default_feed_posts': default_feed_posts,
                               'current_user_custom_feeds': current_user_custom_feeds,
                               'current_user': request.user})
    else:
        return render(request = request,
                      template_name='landing_page.html',
                      context={'register_user_form': NewUserForm,
                               'register_profile_form': RegisterProfileForm,
                               'address_form': AddressForm,
                               'login_form': LoginForm})

def custom_feed(request, feed_id):
    custom_feed_posts = []
    current_user_custom_feeds = []
    if request.user.is_authenticated:
        feeds = CustomFeed.objects.filter(id=feed_id)
        for user_query_set in [feed.user_source.all() for feed in feeds]:
            for user in user_query_set:
                user_post = Post.objects.filter(author=user.id)
                custom_feed_posts.append(user_post)
        for group_user_query_set in [feed.group_source.all() for feed in feeds]:
            for user in group_user_query_set:
                user_group_post = Post.objects.filter(author=user.id)
                custom_feed_posts.append(user_group_post)
        current_user_custom_feeds = CustomFeed.objects.filter(owner=request.user).exclude(name='default')
    return render(request = request,
                  template_name = "custom_feed.html",
                  context={'custom_feed_posts': custom_feed_posts,
                           'feeds': feeds,
                           'new_custom_feed_form': NewCustomFeedForm(user=request.user),
                           'current_user_custom_feeds':current_user_custom_feeds})

def new_custom_feed(request):
    if request.method == 'POST' and request.user.is_authenticated:
        new_custom_feed_form = NewCustomFeedForm(request.POST, user=request.user)
        print(new_custom_feed_form.errors.as_data())

        if new_custom_feed_form.is_valid():
            custom_feed = new_custom_feed_form.save()

            return redirect('main:homepage')
        else:
            new_custom_feed_form = NewCustomFeedForm(user=request.user)

    return render(request=request,
                  template_name='homepage.html',
                  context={'new_custom_feed_form': new_custom_feed_form})

def delete_custom_feed(request):
    if request.method == 'POST':
        CustomFeed.objects.filter(id=request.POST.get("custom_feed_to_be_deleted")).delete()

        return redirect(request.META.get('HTTP_REFERER', '/'))

    return render(request=request,
                  template_name='homepage.html')

def new_post(request):
    if request.method == 'POST':
        new_post_form = NewPostForm(request.POST, initial={'score': 0}, user=request.user)
        print(new_post_form.errors.as_data())

        if new_post_form.is_valid():
            new_post = new_post_form.save()

            return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            new_post_form = NewPostForm(initial={'score': 0}, user=request.user)

    return render(request=request,
                  template_name='homepage.html',
                  context={'new_post_form': new_post_form})

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

