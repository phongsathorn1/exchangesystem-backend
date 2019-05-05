from django.http import request
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from exchange.models import Product, Category, Product_picture, Deal, DealOffer
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

class DealOfferSerializer(serializers.ModelSerializer):
    offer_product = ProductSerializer()

    class Meta:
        model = DealOffer
        fields = '__all__'

class DealSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    deal_offer = DealOfferSerializer(many=True, source='dealoffer_set')

    class Meta:
        model = Deal
        fields = ('id', 'product', 'owner_accept', 'offerer_accept', 'created_date', 'expired_datetime', 'deal_offer')

class DealManagerSerializer(serializers.ModelSerializer):
    Product = ProductSerializer(read_only=True)
