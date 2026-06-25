from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True,blank=True)

    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True,blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10 , decimal_places=2)
    category = models.ForeignKey(Category , on_delete=models.CASCADE ,related_name="products")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="images")
    image = models.ImageField(upload_to="products/")
    alt_text = models.CharField(max_length=255,blank=True)

    def __str__(self):
        return f"Image for {self.product.name}"
    
class ProductVariant(models.Model):
    product = models.ForeignKey(Product , on_delete=models.CASCADE,related_name="variants")
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=100 ,unique=True)
    price = models.DecimalField(max_digits=10 , decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.product.name} - {self.name}"