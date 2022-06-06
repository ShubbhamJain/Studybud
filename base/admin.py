from django.contrib import admin
from .models import Topic, Message, Room, User

admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(Room)
admin.site.register(User)
