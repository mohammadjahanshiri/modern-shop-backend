from rest_framework.generics import ListAPIView , RetrieveAPIView
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter , OrderingFilter
from .models import Product
from .serializers import ProductListSerializer , ProductDetailSerializer
from .filters import ProductFilter


class ProductListView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductListSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ["name","description"]
    ordering_fields = ["price" , "created_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        return(
            Product.objects
            .select_related("category")
            .prefetch_related("images")
            .all()
            .order_by("-created_at")
        )
    
class ProductDetailView(RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductDetailSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return(
            Product.objects
            .select_related("category")
            .prefetch_related("images","variants")
            .all()
        )