from rest_framework import generics, permissions
from . import serializers
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from .models import Object, Picture
from .forms import ObjForm #PicForm


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
