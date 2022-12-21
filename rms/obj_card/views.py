import json
import os
from rest_framework import generics, permissions

from django.views.generic import ListView, DetailView
from django.views.generic.edit import DeleteView
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.base import ContentFile
from django.urls import reverse_lazy

from . import serializers
from .permisisions import IsOwnerOrReadOnly
from .models import Object, Picture, Category
from .forms import ObjForm #PicForm


'''Дальше идёт код для загрузки БД. После заливки удалить'''

def set_parent(request):   # заполняем parent
    categoties = Category.objects.all()
    for cat in categoties:
        try:
            id_parent = Category.objects.get(id_old=cat.id_parent_old)
            cat.parent = id_parent
            cat.save()
            print(cat.id, cat.name, cat.id_old, cat.id_parent_old, )
        except:
            print('Нет объекта с id_old', cat.id_parent_old)
    data = Category.objects.all()
    return render(request, "object/index.html", {'data': data})


def load_cat(request):   # выгружаем из json файла и записываем в базу
    print(os.getcwd ())
    loads = ''
    with open('./category-lv-new.json', 'r', encoding='utf-8') as f:
        loads = f.read()
    cat_dict = json.loads(loads)   # получаем словарь {id_old: [<название категории>, id_parent_old]}

    for cat in cat_dict:
        print(cat, '/', cat_dict[cat][0], '/', cat_dict[cat][1])
        Category.objects.create(
            name=cat_dict[cat][0], 
            id_old=cat, 
            id_parent_old=cat_dict[cat][1]
            )
        

    data = Category.objects.all()

    return render(request, "object/index.html", {'data': data})

'''Конец блока для загрузки БД'''


def index(request):
    '''Временная функция для главной'''
    data = 'Сайт личных вещей'
    return render(request, 'object/index.html', {'data': data})


class CategoryListView(ListView):
    '''Строит дерево категорий'''
    model = Category
    template_name = 'object/category_list.html'


class CategoryDetailView(DetailView):
    '''Выводит вещи из выбранной категории'''
    model = Category
    template_name = "object/category_obj.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj_user = Object.objects.filter(owner=self.request.user)
        cat_children = Category.objects.get(pk=self.kwargs['pk']).get_descendants(include_self=True)
        context['things'] = Object.objects.filter(category__in=cat_children)
        context['photos'] = Picture.objects.filter(obj__owner=self.request.user)
        context['cat_user'] = Category.objects.filter(object__in=obj_user).distinct().get_ancestors(include_self=True)
        return context


def obj_add(request):
    '''Добавить вещь'''
    if request.method == 'GET':
        form = ObjForm()
        return render(request, 'object/obj_add.html', {'form': form})
    elif request.method == 'POST':
        form = ObjForm(request.POST, request.FILES)
        if form.is_valid():
            obj = Object.objects.create(owner=request.user,
                                        name=form.cleaned_data['name'],
                                        description=form.cleaned_data['dis'],
                                        category=form.cleaned_data['category'],
                                        )
            print(form.cleaned_data['category'])
                
            for f in request.FILES.getlist('photos'):
                data = f.read()
                photo = Picture(obj=obj)
                photo.image.save(f.name, ContentFile(data))
                photo.save()
            return redirect('obj_detail', pk=obj.pk)
        else:
            return render(request, 'object/obj_add.html', {'form': form})


def obj_detail(request, pk):
    '''Посмотреть вещь'''
    obj = get_object_or_404(Object, pk=pk)
    pic = Picture.objects.filter(obj=pk)
    obj_path = Category.objects.filter(object=obj).get_ancestors(include_self=True)
    return render(request, 'object/obj_detail.html', {
        'obj': obj, 
        'pic': pic,
        'obj_path': obj_path,
        })


def pic_del(request, pk):
    '''Удалить фото'''
    pic = Picture.objects.get(id=pk)
    pk = pic.obj.id
    pic.delete()
    return redirect('obj_detail', pk=pk)


class ObjDeleteView(DeleteView):
    '''Удалить вещь'''
    model = Object
    template_name = 'object/obj_delete.html'
    success_url = reverse_lazy('home')


class ObjListView(ListView):
    '''Список вещей пользователя'''
    model = Object
    template_name = 'object/obj_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj_user = Object.objects.filter(owner=self.request.user)
        context['things'] = Object.objects.filter(owner=self.request.user)
        context['photos'] = Picture.objects.filter(obj__owner=self.request.user)
        context['cat_user'] = Category.objects.filter(object__in=obj_user).distinct().get_ancestors(include_self=True)
        return context