from rest_framework import serializers
from exchange.models import Product, Category
from user.serializers import UserViewSerializer

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer(read_only=True)
    owner = UserViewSerializer(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
