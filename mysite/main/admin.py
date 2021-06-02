from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Address)
admin.site.register(Group)
admin.site.register(CustomFeed)
admin.site.register(Profile)
admin.site.register(Event)
admin.site.register(Post)
admin.site.register(PostComment)
admin.site.register(ReplyComment)

