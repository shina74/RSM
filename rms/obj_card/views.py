import json
import os
from rest_framework import generics, permissions

from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from django.shortcuts import render

from . import serializers
from .permisisions import IsOwnerOrReadOnly
from .models import Object, Picture, Category


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
