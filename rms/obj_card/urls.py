from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

<<<<<<< HEAD

urlpatterns = [
    path('users/', views.UserList.as_view()),
    path('users/<int:id>/', views.UserDetail.as_view()),
    path('obj/', views.ObjList.as_view()),
    path('obj/<int:id>/', views.ObjDetail.as_view()),
    path('pic/', views.PicList.as_view()),
    path('cat/', views.CategoryListView.as_view(), name='categories'),
    path('cat/<int:pk>/', views.CategoryDetailView.as_view()),

    path('', views.index),
    path('load_cat/', views.load_cat),   # удалить
    path('set_parent/', views.set_parent),   # удалить
]
=======
>>>>>>> a99e489e6242aef092b076497a754fbd8306d6a5

urlpatterns = [
    #path('users/', views.UserList.as_view()),
    #path('users/<int:id>/', views.UserDetail.as_view()),
    #path('obj/', views.ObjList.as_view()),
    #path('obj/<int:id>/', views.ObjDetail.as_view()),
    #path('pic/', views.PicList.as_view()),
    #path('obj/<int:pk>/', views.pic_add, name='pic_add'),
    path('obj_add', views.obj_add, name='obj_add'),
    path('obj/<int:pk>/', views.obj_detail, name='obj_detail'),
    path('obj/<int:pk>/delete', views.pic_del, name='delete'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
 