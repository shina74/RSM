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

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Object(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=False, default='')
    description = models.TextField(blank=True, default='')
    owner = models.ForeignKey('auth.User', related_name='object', on_delete=models.CASCADE)
    category = TreeForeignKey(Category, blank=True, null=True, on_delete=models.PROTECT, 
        related_name='object', verbose_name='Категория')

    class Meta:
        ordering = ['name']
        verbose_name = 'Вещь'
        verbose_name_plural = 'Вещи'


    def __str__(self):
        return self.name


class Picture(models.Model):
    name = models.CharField(max_length=100, blank=True, default='pic', null=True)
    image = models.ImageField(upload_to='%Y/%m/%d/')
    obj = models.ForeignKey(Object, related_name='Picture', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'