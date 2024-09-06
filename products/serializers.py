from rest_framework import serializers
from .models import Products


class ProductsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['seller', 'title',
                  'content', 'product_img']
        read_only_fields = ("seller",)


    def validate(self, attrs):
        if attrs['product_img'] is None:
            attrs['product_img'] = "products_imgs/default_product.png"
        return attrs
