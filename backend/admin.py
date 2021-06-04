from django.contrib import admin
from .models.user import User
from .models.group import Group
from .models.queue import Queue

admin.site.register(User)
admin.site.register(Group)
admin.site.register(Queue)
