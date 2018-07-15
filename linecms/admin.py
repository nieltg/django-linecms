from django.contrib import admin

from .models import Message, TextMessageHook


class MessageAdmin(admin.ModelAdmin):
    fields = ['message_type', 'items', 'text']


class TextMessageHookAdmin(admin.ModelAdmin):
    fields = ['keyword', 'case_sensitive', 'task_type', 'message']


admin.site.register(Message, MessageAdmin)
admin.site.register(TextMessageHook, TextMessageHookAdmin)
