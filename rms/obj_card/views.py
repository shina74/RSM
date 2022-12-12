import json
import os
from rest_framework import generics, permissions

from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from django.shortcuts import render

from . import serializers
<<<<<<< HEAD
from .permisisions import IsOwnerOrReadOnly
from .models import Object, Picture, Category


'''
Дальше идёт код для загрузки БД.
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

'''
Конец блока классов для загрузки БД
'''

def index(request):
    '''
    Временная функция для главной
    '''
    data = 'Привет, мир.'
    return render(request, 'object/index.html', {'data': data})


class CategoryListView(ListView):
    '''
    Строит дерево категорий
    '''
    model = Category
    template_name = 'object/category_list.html'


class CategoryDetailView(DetailView):
    '''
    Выводит вещи из выбранной категории
    '''
    model = Category
    template_name = "object/category.html"
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['things'] = Object.objects.filter(category=self.kwargs['pk'])
        return context

=======
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from .models import Object, Picture
from .forms import ObjForm #PicForm
>>>>>>> a99e489e6242aef092b076497a754fbd8306d6a5


def obj_add(request):
    if request.method == 'GET':
        form = ObjForm()
        return render(request, 'obj_card/obj_add.html', {'form': form})
    elif request.method == 'POST':
        form = ObjForm(request.POST, request.FILES)
        if form.is_valid():
            obj = Object.objects.create(owner=request.user,
                                        name=form.cleaned_data['name'],
                                        description=form.cleaned_data['dis'])
            for f in request.FILES.getlist('photos'):
                data = f.read()
                photo = Picture(obj=obj)
                photo.image.save(f.name, ContentFile(data))
                photo.save()
            return redirect('obj_detail', pk=obj.pk)
        else:
            return render(request, 'obj_card/obj_add.html', {'form': form})


def obj_detail(request, pk):
    post = get_object_or_404(Object, pk=pk)
    pic = Picture.objects.filter(obj=pk)
    return render(request, 'obj_card/obj_detail.html', {'post': post, 'pic': pic})


def pic_del(request, pk):
    pic = Picture.objects.get(id=pk)
    pk = pic.obj.id
    pic.delete()
    return redirect('obj_detail', pk=pk)


# class UserList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = serializers.UserSerializer
#
#
# class UserDetail(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = serializers.UserSerializer
#
#     def get_object(self):
#         queryset = self.filter_queryset(self.get_queryset())
#         obj = queryset.get(pk=self.request.user.id)
#         self.check_object_permissions(self.request, obj)
#         return obj
#
#
# class ObjList(generics.CreateAPIView):
#     queryset = Object.objects.all()
#     serializer_class = serializers.ObjSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)
#
#
# class ObjDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Object.objects.all()
#     serializer_class = serializers.ObjSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#
#
# class PicList(generics.CreateAPIView):
#     queryset = Picture.objects.all()
#     serializer_class = serializers.PictureSerializer
#
#
# class PicDetail(generics.RetrieveAPIView):
#     queryset = Picture.objects.all()
#     serializer_class = serializers.PictureSerializer
#
#
# def obj_add(request):
#     if request.method == "POST":
#         form = ObjForm(request.POST)
#         if form.is_valid():
#             Obj = form.save(commit=False)
#             Obj.owner = request.user
#             Obj.save()
#             return redirect('pic_add', pk=Obj.pk)
#     else:
#         form = ObjForm()
#     return render(request, 'obj_card/obj_add.html', {'form': form})
#
#
# def pic_add(request, pk):
#     if request.method == "POST":
#         form = PicForm(request.POST, request.FILES)
#         if form.is_valid():
#             Obj = form.save()
#             Obj.obj = Object.objects.get(id=pk)
#             Obj.save()
#             return redirect('obj_card/ok')
#     else:
#         post = get_object_or_404(Object, pk=pk)
#         form = PicForm()
#     return render(request, 'obj_card/pic_add.html', {'form': form, 'post': post})
#
#
# def ok(request):
#     return render(request, 'obj_card/ok.html')
