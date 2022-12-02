import json
import os
from rest_framework import generics, permissions

from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from django.shortcuts import render

from . import serializers
from .permisisions import IsOwnerOrReadOnly
from .models import Object, Picture, Category


'''
Дальше идут классы для загрузки БД.
После заливки удалить 
'''

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
    # print(os.getcwd ())
    loads = ''
    with open('category-lv.json', 'r', encoding='utf-8') as f:
        loads = f.read()
    cat_dict = json.loads(loads)   # получаем словарь {"имя категории": ["id категори, id родителя"]}

    for cat in cat_dict:
        print(cat, '/' ,cat_dict[cat][0], '/', cat_dict[cat][1])
        Category.objects.create(name=cat, id_old=cat_dict[cat][0], id_parent_old=cat_dict[cat][1])
    data = Category.objects.all()

    return render(request, "object/index.html", {'data': data})


def index(request, **kwargs):
    data = Category.objects.all()
    print(kwargs)
    return render(request, "object/index.html", {"data": data})

'''
Конец блока классов для загрузки БД
'''

class CategoryListView(ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'object/category_list.html'


class PostByCategoryView(ListView):
    context_object_name = 'posts'
    template_name = 'object/object_list.html'

    def get_queryset(self):
        print('Принт:', self)
        self.category = Category.objects.get(id=1)
        queryset = Object.objects.filter(category=self.category)
        return queryset

    def get_context_data(self, **kwargs):
        print('Принт:', self.request)
        print('Принт2:', kwargs)
        context = super().get_context_data(**kwargs)
        context['title'] = 'Категория 309' # self.category
        return context


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.get(pk=self.request.user.id)
        self.check_object_permissions(self.request, obj)
        return obj


class ObjList(generics.CreateAPIView):
    queryset = Object.objects.all()
    serializer_class = serializers.ObjSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ObjDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Object.objects.all()
    serializer_class = serializers.ObjSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class PicList(generics.CreateAPIView):
    queryset = Picture.objects.all()
    serializer_class = serializers.PictureSerializer


class PicDetail(generics.RetrieveAPIView):
    queryset = Picture.objects.all()
    serializer_class = serializers.PictureSerializer
