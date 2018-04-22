from django.contrib import admin

from .models import Message, Postback


class MessageAdmin(admin.ModelAdmin):
    fields = ['text', 'reply', 'reply_text']


class PostbackAdmin(admin.ModelAdmin):
    fields = ['data', 'reply', 'reply_text']


admin.site.register(Message, MessageAdmin)
admin.site.register(Postback, PostbackAdmin)
