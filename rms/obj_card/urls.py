from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.urlpatterns import format_suffix_patterns

from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('account/', views.AccountIndex.as_view(), name='account'),
    path('cat/', views.CategoryListView.as_view(), name='categories'),
    path('cat/<int:pk>/', views.CategoryDetailView.as_view(), name='category_obj'),
    path('obj_add', views.obj_add, name='obj_add'),
    path('obj/<int:pk>/', views.obj_detail, name='obj_detail'),
    path('obj/<int:pk>/delete', views.ObjDeleteView.as_view(), name='obj_delete'),
    path('obj_list/', views.ObjListView.as_view(), name='obl_list'),
    path('add_pic/<int:pk>', views.add_pic, name='add_pic'),
    path('obj/<int:pk>/edit', views.ObjUpdateView.as_view(), name='obj_edit'),    
    path('photo/<int:pk>/delete', views.pic_del, name='photo_delete'),
    path('search/', views.SearchObject.as_view(), name='search'),
    path('public_link/<int:pk>', views.ObjPublic.as_view(), name='public_link'),
    path('storage/', views.StorageList.as_view(), name='storage_list'),
    path('storage/<int:pk>/', views.StorageDetail.as_view(), name='storage_detail'),
    path('storage/<int:pk>/delete', views.StorageDelete.as_view(), name='storage_delete'),
    path('storage/<int:pk>/edit', views.StorageUpdate.as_view(), name='storage_edit'),
    path('storage/create', views.StorageCreate.as_view(), name='storage_create'),

    # Адреса для загрузки каталога
    # path('load_cat/', views.load_cat),
    # path('set_parent/', views.set_parent),

    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns = format_suffix_patterns(urlpatterns)
