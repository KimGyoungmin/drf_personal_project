from rest_framework import serializers
from .models import Products, Category, HashTag
from accounts.models import CustomUser


class ProductsSerializers(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Category.objects.all(),
        required=False
    )
    class Meta:
        model = Products
        fields = ['seller', 'title',
                  'content', 'product_img', 'category',]
        read_only_fields = ("seller",)

    def validate_category(self, value):
        if value and not Category.objects.filter(name=value).exists():
            raise serializers.ValidationError("카테고리가 존재하지 않습니다.")
        return value

    def validate(self, attrs):
        if attrs['product_img'] is None:
            attrs['product_img'] = "products_imgs/default_product.png"
        return attrs
    
class ProductsListSerializers(ProductsSerializers):
    hashtag = serializers.StringRelatedField(many = True)
    seller = serializers.StringRelatedField()
    class Meta:
        model = Products
        fields = ['seller', 'title',
                  'content', 'product_img', 'category','hashtag']
        read_only_fields = ("seller",)