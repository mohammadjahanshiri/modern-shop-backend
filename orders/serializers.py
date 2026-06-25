from rest_framework import serializers
from decimal import Decimal
from django.db import transaction
from products.models import ProductVariant
from .models import *

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="variant.product.name", read_only=True)
    unit_price = serializers.DecimalField(
        source="variant.product.price",
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    subtotal = serializers.SerializerMethodField()
    
    class Meta:
        model = CartItem
        fields = ["id","variant","product_name","quantity","unit_price","subtotal"]

    def get_subtotal(self,obj):
        return obj.variant.product.price * obj.quantity
    

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True,read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["id","user","items","total_price"]

    def get_total_price(self,obj):
        total = Decimal("0.00")
        for item in obj.items.all():
            total += item.variant.price * item.quantity
        return total
    

class AddToCartSerializer(serializers.Serializer):
    variant_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

    def validate(self, data):
        try:
            variant = ProductVariant.objects.get(id=data["variant_id"])
        except ProductVariant.DoesNotExist:
            raise serializers.ValidationError("Invaild variant")
        
        if data["quantity"] > variant.stock:
            raise serializers.ValidationError("Not enogh stock")
        
        data["variant"] = variant
        return data
    
    def save(self, **kwargs):
        user = self.context["request"].user
        variant = self.validated_data["variant"]
        quantity = self.validated_data["quantity"]
        cart , _ = Cart.objects.get_or_create(user=user)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            variant=variant,
            defaults={"quantity":quantity},
        )
        
        if not created:
            new_quantity = cart_item.quantity + quantity
            if new_quantity > variant.stock:
                raise serializers.ValidationError("Not enogh stock")
            cart_item.quantity = new_quantity
            cart_item.save()
        
        return cart_item
    

class UpdateCartItemSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(min_value=1)

    class Meta:
        model = CartItem
        fields = ["quantity"]

    def validate_quantity(self, value):
        variant = self.instance.variant
        if value > variant.stock:
            raise serializers.ValidationError("Not enogh stock")
        return value
    


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="variant.product.name" ,read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id","variant","product_name","price","quantity"]

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True,read_only=True)

    class Meta:
        model = Order
        fields = ["id","user","first_name","last_name","address","postal_code","total_price","status","created_at","items"]


class CheckoutSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    address = serializers.CharField()
    postal_code = serializers.CharField(max_length=20)

    def validate(self, data):
        user = self.context["request"].user

        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            raise serializers.ValidationError("Cart not found.")
        
        if not cart.items.exists():
            raise serializers.ValidationError("Cart is empty") 
        
        for item in cart.items.select_related("variant__product"):
            if item.quantity > item.variant.stock:
                raise serializers.ValidationError(f"Not enogh stock {item.variant.product.name}")
            

        data["cart"] = cart
        return data
    
    def save(self , **kwargs):
        user = self.context["request"].user
        cart = self.validated_data["cart"]

        with transaction.atomic():
            total = Decimal("0.00")
            order = Order.objects.create(
                user=user,
                first_name=self.validated_data["first_name"],
                last_name=self.validated_data["last_name"],
                address=self.validated_data["address"],
                postal_code=self.validated_data["postal_code"],
                total_price=Decimal("0.00"),
                status="pending",
            )

            for item in cart.items.select_related("variant__product"):
                price = item.variant.product.price
                total += price *item.quantity

                OrderItem.objects.create(
                    order=order,
                    variant=item.variant,
                    price=price,
                    quantity=item.quantity,
                )
                item.variant.stock -= item.quantity
                item.variant.save()

            order.total_price = total
            order.save()

            cart.items.all().delete()

        return order