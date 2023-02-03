from django.contrib import admin

from mptt.admin import MPTTModelAdmin
from django_mptt_admin.admin import DjangoMpttAdmin

from .models import Object, Picture, Category, Storage


class PictureInline(admin.StackedInline):
    model = Picture

class ObjectAdmin(admin.ModelAdmin):
    inlines = [PictureInline]

admin.site.register(Object, ObjectAdmin)
admin.site.register(Picture)
admin.site.register(Storage)
admin.site.register(Category, DjangoMpttAdmin)
