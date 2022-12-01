from rest_framework import generics, permissions

from django.views.generic import ListView
from django.contrib.auth.models import User

from . import serializers
from .permisisions import IsOwnerOrReadOnly
from .models import Object, Picture, Category


class CategoryListView(ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'object/category_list.html'


class PostByCategoryView(ListView):
    context_object_name = 'posts'
    template_name = 'object/post_list.html'

    def get_queryset(self):
        self.category = Category.objects.get(slug=self.kwargs['slug'])
        queryset = Object.objects.filter(category=self.category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.category
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
