import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price" , lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="price" , lookup_expr="lte")

    variant_name = django_filters.CharFilter(field_name="variants__name" , lookup_expr="icontains")
    variant_sku = django_filters.CharFilter(field_name="variants__sku" , lookup_expr="iexact")

    in_stock = django_filters.BooleanFilter(method="filter_in_stock")

    class Meta:
        model = Product
        fields = ["category"]

    def filter_in_stock(self , queryset , name , value):
        if value:
            return queryset.filter(variants__stock__gt=0).distinct()
        return queryset