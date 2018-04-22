from django.contrib import admin

from .models import Message, InvalidMessage, Postback


class MessageAdmin(admin.ModelAdmin):
    fields = ['text', 'reply', 'reply_text', 'reply_group']


class InvalidMessageAdmin(admin.ModelAdmin):
    fields = ['reply', 'reply_text', 'reply_group']


class PostbackAdmin(admin.ModelAdmin):
    fields = ['data', 'reply', 'reply_text', 'reply_group']


admin.site.register(Message, MessageAdmin)
admin.site.register(InvalidMessage, InvalidMessageAdmin)
admin.site.register(Postback, PostbackAdmin)
