from django.contrib import admin

from .models import Text, Group, GroupItem


class TextAdmin(admin.ModelAdmin):
    fields = ['text']


class GroupItemInline(admin.TabularInline):
    model = GroupItem


class GroupAdmin(admin.ModelAdmin):
    inlines = [
        GroupItemInline,
    ]


admin.site.register(Text, TextAdmin)
