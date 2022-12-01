from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


urlpatterns = [
    path('users/', views.UserList.as_view()),
    path('users/<int:id>/', views.UserDetail.as_view()),
    path('obj/', views.ObjList.as_view()),
    path('obj/<int:id>/', views.ObjDetail.as_view()),
    path('pic/', views.PicList.as_view()),
    path('cat/', views.CategoryListView.as_view(), name='category-list'),
    path('<str:slug>/', views.PostByCategoryView.as_view(), name='category'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
