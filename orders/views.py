from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status , generics , permissions
from .models import *
from .serializers import *


class CartDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):
        cart,_ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)
    

class AddToCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self , request):
        serializer = AddToCartSerializer(
            data=request.data,
            context={"request":request},
        )
        serializer.is_valid(raise_exception=True)
        item = serializer.save()
        return Response(CartItemSerializer(item).data , status=status.HTTP_201_CREATED)


class UpdateCartItemView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UpdateCartItemSerializer

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)


class RemoveCartItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self,request,pk):
        item = get_object_or_404(CartItem , id=pk , cart__user=request.user)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class CheckoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):
        serializer = CheckoutSerializer(
            data=request.data,
            context={"request":request},
        )
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response(OrderSerializer(order).data , status=status.HTTP_201_CREATED)
    

class OrderListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by("-created_at")


class OrderDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)