from django.http import request
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from exchange.models import Product, Category, Product_picture, Deal
from user.models import User
from user.serializers import UserViewSerializer

class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'url', 'name')

class ProductPictureUploadSerializer(serializers.ModelSerializer):
    user = UserViewSerializer(read_only=True)

    class Meta:
        model = Product_picture
        fields = ('id', 'picture_path', 'user')

class ProductPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product_picture
        fields = ('picture_path',)

class ProductSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(many=False, queryset=Category.objects.all(), source='category', write_only=True)
    owner = UserViewSerializer(read_only=True)
    product_picture = ProductPictureSerializer(many=True, read_only=True, source='product_picture_set')

    class Meta:
        model = Product
        fields = ('id', 'url', 'name', 'detail', 'quantity', 'category',
                  'category_id', 'want_product', 'owner', 'product_picture')

class DealSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    with_product = ProductSerializer()

    class Meta:
        model = Deal
        fields = '__all__'

class DealManagerSerializer(serializers.ModelSerializer):
    Product = ProductSerializer(read_only=True)
