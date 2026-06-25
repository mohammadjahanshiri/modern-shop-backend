from django.db import models
from django.utils.text import slugify
from products.models import ProductVariant
from django.conf import settings



class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE , related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart of {self.user.username}"
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart , on_delete=models.CASCADE ,related_name="items")
    variant = models.ForeignKey(ProductVariant , on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} * {self.variant}"
    

class Order(models.Model):
    STATUS_CHOICES =(
        ("pending" ,"Pending"),
        ("paid","Paid"),
        ("shipped","Shipped"),
        ("canceled","Cancelled"),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="orders")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.TextField()
    postal_code = models.CharField(max_length=20)
    total_price = models.DecimalField(max_digits=10,decimal_places=2)
    status = models.CharField(max_length=20 , choices=STATUS_CHOICES,default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order , on_delete=models.CASCADE,related_name="items")
    variant = models.ForeignKey(ProductVariant , on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Item {self.id} in Order {self.order.id}"