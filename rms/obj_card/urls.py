from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.urlpatterns import format_suffix_patterns

from . import views


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
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns = format_suffix_patterns(urlpatterns)
