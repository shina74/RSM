from django_filters import FilterSet, CharFilter
from .models import Object


class ObjFilter(FilterSet):
    class Meta:
        model = Object
        fields = ['category', 'storage']

# class ProductFilter(FilterSet):
#    class Meta:
#         name = CharFilter(lookup_expr='iexact')
#         model = Product
#         fields = {
#             'name': ['icontains'],
#             'quantity': ['gt'],
#             'price': [
#                 'lt',  # цена должна быть меньше или равна указанной
#                 'gt',  # цена должна быть больше или равна указанной
#             ],
#         }
