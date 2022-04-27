import django
import django_filters
from django_filters import NumericRangeFilter

from .models import *
class ProductFilter(django_filters.FilterSet):
    
    class Meta:
        model=Product
        fields='__all__'