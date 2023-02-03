from django import forms

from mptt.forms import MoveNodeForm, TreeNodeChoiceField

from .models import Object, Picture, Category, Storage


class ObjForm(forms.Form):

    name = forms.CharField(label=u'Название')
    dis = forms.CharField(label=u'Описание')
    # storage = forms.CharField(label=u'Места хранения')
    storage = forms.ModelChoiceField(
        queryset=Storage.objects.all(),
        label=u'Место хранения',
        ) 
    category = TreeNodeChoiceField(
        queryset=Category.objects.all(), 
        label="Выберите категорию",
        )
    photos = forms.ImageField(
        label=u'Фотографии', 
        widget=forms.FileInput(attrs={'multiple': 'multiple'})
        )


class PicForm(forms.Form):
    photos = forms.ImageField(
        label=u'Фотографии',
        widget=forms.FileInput(attrs={'multiple': 'multiple'})
        )

# class ObjForm(forms.ModelForm):
#
#     class Meta:
#         model = Object
#         fields = ('name', 'description',)
#
#
