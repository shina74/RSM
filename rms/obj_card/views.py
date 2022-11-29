from rest_framework import generics, permissions
from . import serializers
from .permisisions import IsOwnerOrReadOnly
from django.contrib.auth.models import User
from .models import Object, Picture


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
