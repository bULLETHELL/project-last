from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("feed/<int:feed_id>", views.custom_feed, name="feed"),
    path("new_custom_feed", views.new_custom_feed, name="new_custom_feed"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("delete_custom_feed", views.delete_custom_feed, name="delete_custom_feed"),
    path("register", views.register, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name="logout"),
]
