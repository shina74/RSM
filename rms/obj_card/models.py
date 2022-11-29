from django.db import models


class Object(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=False, default='')
    description = models.TextField(blank=True, default='')
    owner = models.ForeignKey('auth.User', related_name='object', on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']


class Picture(models.Model):
    name = models.CharField(max_length=100, blank=True, default='pic')
    image = models.ImageField(upload_to='media')
    obj = models.ForeignKey(Object, related_name='Picture', on_delete=models.CASCADE)
