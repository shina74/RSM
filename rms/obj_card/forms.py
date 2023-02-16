from django import forms
from mptt.forms import MoveNodeForm, TreeNodeChoiceField
from .models import Object, Picture, Category, Storage



class FilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.obj_user = kwargs.pop('obj_user', None)
        super(FilterForm, self).__init__(*args, **kwargs)
        self.fields['storage'].queryset = Storage.objects.filter(object__in=self.obj_user).distinct()
        self.fields['category'].queryset = Category.objects.filter(object__in=self.obj_user).distinct()

    storage = forms.ModelChoiceField(
        queryset=None,
        label=u'Место хранения',
        required=False,
        ) 

    category = TreeNodeChoiceField(
        queryset=None, 
        label="Категория",
        required=False,
        )


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
