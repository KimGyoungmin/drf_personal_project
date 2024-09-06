from django.db import models
from django.conf import settings

class Products(models.Model):
    seller = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name = "products")
    title = models.CharField(max_length=100)
    content = models.TextField()
    product_img = models.ImageField(upload_to='products_imgs/', blank=True, null=True, default="default_product.png")
    likes = models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name="like_products")
    
    def __str__(self):
        return f"판매자: {self.seller} 상품제목: {self.title}"
    
    
    def update_like_count(self):
        self.like_count = self.likes.count()
        self.save()
