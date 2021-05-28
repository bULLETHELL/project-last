from typing import Callable
from django.db import models
from django.db.models import CharField, TextField, ManyToManyField, OneToOneField, ForeignKey, DateField, TimeField, DateTimeField, IntegerField, DecimalField, CASCADE
import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.
class address(models.Model):
    profileAddress = CharField(max_length=100)
    profileCity = CharField(max_length=50)
    profilePostalCode = IntegerField()

class Group(models.Model):
    description = TextField()
    owner = ForeignKey(User, on_delete=CASCADE)
    members = ManyToManyField(User)

class CustomFeed(models.Model):
    user_source = ForeignKey(User, on_delete=CASCADE)
    group_source = ForeignKey(Group, on_delete=CASCADE)


class Profile(models.Model):
    profileUser = OneToOneField(User, on_delete=CASCADE)
    profilePhoneNumber = DecimalField(decimal_places=0, max_digits=8)
    profileAddress = ForeignKey(address, on_delete=CASCADE)
    friendlist = ManyToManyField(User)
    customFeeds = ManyToManyField(CustomFeed)
    def __str__(self):
        return f"{self.profileUser}"

class Event(models.Model):
    participants = ManyToManyField (User)
    host = ForeignKey(User, on_delete=CASCADE)
    start_datetime = DateTimeField()
    end_datetime = DateTimeField()
    address = ForeignKey(address, on_delete=CASCADE)
    description = TextField()

class Post(models.Model):
    author = ForeignKey(User, on_delete=CASCADE)
    content = TextField()
    score = IntegerField()

class Comment(models.Model):
    content = TextField()
    author = ForeignKey(User, on_delete=CASCADE)
    score = IntegerField()

class PostComment(Comment):
    parent_post = ForeignKey(Post, on_delete=CASCADE)
class CommentComment(Comment):
    parent_comment = ForeignKey(Comment, on_delete=CASCADE)
