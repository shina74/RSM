# from slugify import slugify
from django.db import models
from django.urls import reverse

from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    name = models.CharField(max_length=256, unique=False)
    parent = TreeForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='children'
        )
    id_old = models.CharField(max_length=128, blank=True)
    id_parent_old = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return self.name


class Object(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=False, default='')
    description = models.TextField(blank=True, default='')
    owner = models.ForeignKey('auth.User', related_name='object', on_delete=models.CASCADE)
    category = TreeForeignKey(Category, blank=True, null=True, on_delete=models.PROTECT, 
        related_name='object', verbose_name='Категория')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'


class Picture(models.Model):
    name = models.CharField(max_length=100, blank=True, default='pic')
    image = models.ImageField(upload_to='media')
    obj = models.ForeignKey(Object, related_name='Picture', on_delete=models.CASCADE, blank=True, null=True)
