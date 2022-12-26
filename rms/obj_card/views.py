import json
import os
from rest_framework import generics, permissions

from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.base import ContentFile
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

from . import serializers
from .permisisions import IsOwnerOrReadOnly
from .models import Object, Picture, Category
from .forms import ObjForm, PicForm



class AccountIndex(LoginRequiredMixin, TemplateView):
    '''Личный кабинет'''
    template_name = 'object/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count_obj'] = Object.objects.filter(owner=self.request.user).count()
        return context


@login_required
def index(request):
    '''Временная функция для главной'''
    data = 'Сайт'
    return render(request, 'object/index.html', {
        'data': data,
        'count_obj': Object.objects.filter(owner=request.user).count(),
        })


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


class ObjUpdateView(UpdateView):
    model = Object
    template_name = 'object/obj_edit.html'
    fields = ['name', 'description', 'category']
    success_url = reverse_lazy('home')

@login_required
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


def add_pic(request, pk):
    '''Кнопка добавления картинки'''
    if request.method == 'POST':
        form = PicForm(request.POST, request.FILES)
        if form.is_valid():
            for f in request.FILES.getlist('photos'):
                data = f.read()
                photo = Picture(obj=Object.objects.get(id=pk))
                photo.image.save(f.name, ContentFile(data))
                photo.save()
            return redirect('obj_detail', pk=pk)
    else:
        form = PicForm()
    return redirect('obj_detail', pk=pk)
