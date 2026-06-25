from django.urls import path
from .views import *


urlpatterns = [
    path("cart/",CartDetailView.as_view(),name="cart-detail"),
    path("cart/add/",AddToCartView.as_view(),name="add-to-cart"),
    path("cart/items/<int:pk>/update/",UpdateCartItemView.as_view(),name="update-cart-item"),
    path("cart/items/<int:pk>/remove/",RemoveCartItemView.as_view(),name="remove-cart-item"),
    path("checkout/" , CheckoutView.as_view(),name="checkout"),
    path("orders/", OrderListView.as_view(), name="order-list"),
    path("orders/<int:pk>/" , OrderDetailView.as_view(), name="order-detail")
]