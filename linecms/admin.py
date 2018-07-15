from django.contrib import admin

from .models import Message


class MessageAdmin(admin.ModelAdmin):
    fields = ['message_type', 'items', 'text']


admin.site.register(Message, MessageAdmin)
