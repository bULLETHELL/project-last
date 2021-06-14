from typing import Callable
from django.db import models
from django.db.models import CharField, TextField, ManyToManyField, OneToOneField, ForeignKey, DateField, TimeField, DateTimeField, IntegerField, DecimalField, CASCADE
import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.
class Address(models.Model):
    address = CharField(max_length=100)
    city = CharField(max_length=50)
    postalCode = IntegerField()
    def __str__(self):
        return f"{self.address} {self.city} {self.postalCode}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(profileUser=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Group(models.Model):
    name = CharField(max_length=50)
    description = TextField()
    owner = ForeignKey(User, on_delete=CASCADE, related_name="groupOwner")
    members = ManyToManyField(User)
    def __str__(self):
        return f"{self.name}"

class CustomFeed(models.Model):
    name = CharField(max_length=50)
    owner = ForeignKey(User, on_delete=CASCADE, related_name="feedOwner")
    user_source = ManyToManyField(User, blank=True)
    group_source = ManyToManyField(Group, blank=True)
    def __str__(self):
        return f"{self.name}"


class Profile(models.Model):
    profileUser = OneToOneField(User, on_delete=CASCADE)
    profilePhoneNumber = DecimalField(decimal_places=0, max_digits=8)
    profileAddress = ForeignKey(Address, on_delete=CASCADE)
    friendlist = ManyToManyField(User, related_name="userFriendlist")
    customFeeds = ManyToManyField(CustomFeed)
    def __str__(self):
        return f"{self.profileUser}"

class Event(models.Model):
    name = CharField(max_length=50)
    participants = ManyToManyField (User, related_name="participatingUsers")
    host = ForeignKey(User, on_delete=CASCADE, related_name="hostingUser")
    start_datetime = DateTimeField()
    end_datetime = DateTimeField()
    address = ForeignKey(Address, on_delete=CASCADE)
    description = TextField()
    def __str__(self):
        return f"{self.name}"

class Post(models.Model):
    author = ForeignKey(User, on_delete=CASCADE)
    content = TextField()
    score = IntegerField()
    def __str__(self):
        return f"{self.author}'s post"

class PostComment(models.Model):
    content = TextField()
    author = ForeignKey(User, on_delete=CASCADE)
    score = IntegerField()
    parent_post = ForeignKey(Post, on_delete=CASCADE)

class ReplyComment(models.Model):
    content = TextField()
    author = ForeignKey(User, on_delete=CASCADE)
    score = IntegerField()
    parent_comment = ForeignKey(PostComment, on_delete=CASCADE, related_name="commentParent")
