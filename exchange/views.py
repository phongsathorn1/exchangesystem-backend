import os
import uuid

from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.reverse import reverse
from rest_framework import mixins, generics, status, viewsets, views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from exchange.models import Product, Category
from exchange.serializers import ProductSerializer, CategoriesSerializer


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

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


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
    SAVE_DIR = os.path.abspath('static/product_images')
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        file_obj = request.FILES['file']
        file_extension = '.%s' %file_obj.name.split('.')[-1]
        self.handle_file_upload(file_obj, file_extension)

        return Response(status=204)

    def handle_file_upload(self, file, file_extension):
        with open(os.path.join(self.SAVE_DIR, '%s.%s' %(str(uuid.uuid4()), file_extension)), 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
