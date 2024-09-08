from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class HashTag(models.Model):
    tags = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.tags

class Products(models.Model):
    seller = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="products")
    title = models.CharField(max_length=100)
    content = models.TextField()
    product_img = models.ImageField(
        upload_to='products_imgs/', blank=True, null=True, default="default_product.png")
    likes = models.ManyToManyField(
        to=settings.AUTH_USER_MODEL, related_name="like_products")
    category = models.ForeignKey(
        to=Category, on_delete=models.SET_NULL, null=True, related_name="products")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    hashtag = models.ManyToManyField(to = HashTag, related_name="hash_product")

    def __str__(self):
        return f"판매자: {self.seller} 상품제목: {self.title}"

    def update_like_count(self):
        self.like_count = self.likes.count()
        self.save()
