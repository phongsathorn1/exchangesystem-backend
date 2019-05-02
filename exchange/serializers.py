from rest_framework import serializers
from exchange.models import Product, Category
from user.serializers import UserViewSerializer

class CategoriesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'url', 'name')

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    category = CategoriesSerializer(read_only=True)
    owner = UserViewSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ('__all__')
