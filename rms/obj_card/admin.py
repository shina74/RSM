from django.contrib import admin

from mptt.admin import MPTTModelAdmin
from django_mptt_admin.admin import DjangoMpttAdmin

from .models import Object, Picture, Category


class CategoryAdmin(DjangoMpttAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Object)
admin.site.register(Picture)
admin.site.register(Category, CategoryAdmin)