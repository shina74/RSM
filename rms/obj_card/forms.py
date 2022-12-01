from django import forms

from .models import Object, Picture


class ObjForm(forms.ModelForm):

    class Meta:
        model = Object
        fields = ('name', 'description',)


class PicForm(forms.ModelForm):

    class Meta:
        model = Picture
        fields = ('image',)
