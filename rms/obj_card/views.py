from rest_framework import generics, permissions
from . import serializers
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Object, Picture
from .forms import ObjForm, PicForm


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


"""
def obj_add(request):
    if request.method == "POST":
        form = ObjForm(request.POST)
        if form.is_valid():
            Obj = form.save(commit=False)
            Obj.owner = request.user
            Obj.save()
            return redirect('obj_card/ok')
    else:
        form = ObjForm()
    return render(request, 'obj_card/obj_add.html', {'form': form})
"""
def obj_add(request):
    if request.method == "POST":
        form = PicForm(request.POST, request.FILES)
        if form.is_valid():
            Obj = form.save()
            Obj.save()
            return redirect('obj_card/ok')
    else:
        form = PicForm()
    return render(request, 'obj_card/obj_add.html', {'form': form})


def ok(request):
    return render(request, 'obj_card/ok.html')
