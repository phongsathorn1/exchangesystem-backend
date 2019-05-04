import os
import uuid

from django.db.models import Q
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.reverse import reverse
from rest_framework import mixins, generics, status, viewsets, views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from exchange.models import Product, Category, Product_picture, Deal
from exchange.serializers import ProductSerializer, CategoriesSerializer, ProductPictureSerializer, \
    ProductPictureUploadSerializer
from user.models import User


@api_view(['GET'])
@permission_classes((AllowAny, ))
def api_root(request, format=None):
    return Response({
        'register': reverse('user-register', request=request, format=format),
        'products': reverse('product-list', request=request, format=format)
    })

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def create(self, request):
        product_serializer = self.serializer_class(data={
            'name': request.data.get('name'),
            'detail': request.data.get('detail'),
            'quantity': request.data.get('quantity'),
            'category_id': request.data.get('category_id'),
            'want_product': request.data.get('want_product')
        }, context={'request': request})

        if product_serializer.is_valid():
            product = product_serializer.save(owner=request.user)
            for image_id in request.data.get('images_id'):
                picture = Product_picture.objects.get(pk=image_id)
                picture.user = request.user
                picture.product = product
                picture.save()

            return Response(product_serializer.data, status.HTTP_200_OK)
        return Response(product_serializer.errors, status.HTTP_400_BAD_REQUEST)

    def list_avaliable_by_user(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        products = Product.objects.filter(owner=user)
        products_unavaliable = Deal.objects.filter(
            Q(product__in=products) | Q(with_product__in=products),
            Q(owner_accept=True)
        )
        products_unavaliable_ids = products_unavaliable.values_list('product', flat=True)
        products_avaliable = products.exclude(pk__in=products_unavaliable_ids)
        print(products_avaliable[0])

        product_serializer = self.serializer_class(products_avaliable, context={'request': request}, many=True)
        return Response(product_serializer.data, status.HTTP_200_OK)


    # def perform_create(self, serializer):
    #     print(serializer.data)
    #     serializer.save(owner=self.request.user)

class ProductPictureViewSet(viewsets.ModelViewSet):

    def retrieve(self, request, pk=None):
        queryset = Product_picture.objects.all()
        product_picture = get_object_or_404(queryset, pk=pk)
        serializer = ProductPictureSerializer(product_picture)
        # serializer.data.picture_path = 'media/'+serializer.data.picture_path
        return Response(serializer.data)


class CategoryDetail(mixins.RetrieveModelMixin,
                     mixins.CreateModelMixin,
                     generics.GenericAPIView):

    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        return self.retrieve(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(self, request, *args, **kwargs)

class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (AllowAny,)

class ProductImageUploadView(views.APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        file = request.FILES['file']
        file_extension = '.%s' % file.name.split('.')[-1]
        file_name = str(uuid.uuid4()) + file_extension
        file.name = file_name

        data = {
            'picture_path': file
        }
        serializer = ProductPictureUploadSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
