from django.contrib import admin

from .models import Text


class TextAdmin(admin.ModelAdmin):
    fields = ['text']


admin.site.register(Text, TextAdmin)
