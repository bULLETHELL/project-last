from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("profile", views.profile, name="profile"),
    path("register", views.register, name="register"),
]