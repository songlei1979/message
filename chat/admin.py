from django.contrib import admin

from chat.models import Message, ChatRoom

# Register your models here.
admin.site.register(Message)
admin.site.register(ChatRoom)
