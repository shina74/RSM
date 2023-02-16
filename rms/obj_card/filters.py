from django_filters import FilterSet, CharFilter
# from mptt.forms import MoveNodeForm, TreeNodeChoiceField
from mptt.fields import TreeNodeChoiceField
from .models import Object, Category


class ObjFilter(FilterSet):
    category = TreeNodeChoiceField(
        queryset=Category.objects.all(), 
        label="Выберите категорию",
        )

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
