from rest_framework.reverse import reverse
from rest_framework import mixins, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from exchange.models import Product, Category
from exchange.serializers import ProductSerializer, CategoriesSerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'register': reverse('user_register', request=request, format=format),
        'products': reverse('product_list', request=request, format=format)
    })

class ProductDetail(mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    generics.GenericAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(self, request, *args, **kwargs)


class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CategoryDetail(mixins.CreateModelMixin,
                     generics.GenericAPIView):

    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer

    def post(self, request, *args, **kwargs):
        return self.create(self, request, *args, **kwargs)

class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
