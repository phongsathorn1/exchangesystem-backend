from rest_framework import serializers
from exchange.models import Product, Category
from user.serializers import UserViewSerializer

class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'url', 'name')

class ProductSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(many=False, queryset=Category.objects.all(), source='category', write_only=True)
    owner = UserViewSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'url', 'name', 'detail', 'quantity', 'category', 'category_id', 'want_product', 'owner')

