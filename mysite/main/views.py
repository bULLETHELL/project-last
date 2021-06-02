from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import NewUserForm, RegisterProfileForm, AddressForm

# Create your views here.
def homepage(request):
    return render(request = request,
                  template_name = "homepage.html",
                  context= {'register_user_form': NewUserForm,
                            'register_profile_form': RegisterProfileForm,
                            'address_form': AddressForm})

def profile(request):
    return render(request = request,
                  template_name = 'profile.html',)

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
