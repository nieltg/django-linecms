from django.contrib import admin

from .models import Message, InvalidMessage, Postback


class MessageAdmin(admin.ModelAdmin):
    fields = ['text', 'reply', 'reply_text']


class InvalidMessageAdmin(admin.ModelAdmin):
    fields = ['reply', 'reply_text']


class PostbackAdmin(admin.ModelAdmin):
    fields = ['data', 'reply', 'reply_text']


admin.site.register(Message, MessageAdmin)
admin.site.register(InvalidMessage, InvalidMessageAdmin)
admin.site.register(Postback, PostbackAdmin)
