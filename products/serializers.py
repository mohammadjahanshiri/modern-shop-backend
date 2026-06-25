from rest_framework import serializers
from .models import *


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ("id","name","slug")


class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ("id","image")

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image and hasattr(obj.image,"url"):
            if request is not None:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

class ProductVariantSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductVariant
        fields = ("id","name","sku","price","stock")

class ProductListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    main_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ("id","name","slug","price","category","main_image")

    def get_main_image(self, obj):
        request = self.context.get("request")
        first_image = obj.images.first()
        if first_image and first_image.image and hasattr(first_image.image,"url"):
            if request is not None:
                return request.build_absolute_uri(first_image.image.url)
            return first_image.image.url
        return None

class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True,read_only=True)
    variants = ProductVariantSerializer(many=True,read_only=True)

    class Meta:
        model = Product
        fields = ("id","name","slug","description","price","category","images","variants")

