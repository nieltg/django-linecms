from django.contrib import admin

from .models import Text, Group, GroupItem, Image


class TextAdmin(admin.ModelAdmin):
    fields = ['text']


class GroupItemInline(admin.TabularInline):
    model = GroupItem


class GroupAdmin(admin.ModelAdmin):
    inlines = [
        GroupItemInline,
    ]

class ImageAdmin(admin.ModelAdmin):
    fields = ['image']


admin.site.register(Text, TextAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Image, ImageAdmin)
