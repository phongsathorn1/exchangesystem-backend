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

from exchange.models import Product, Category, Product_picture, Deal, DealOffer
from exchange.serializers import ProductSerializer, CategoriesSerializer, ProductPictureSerializer, \
    ProductPictureUploadSerializer, DealSerializer, DealOfferSerializer
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

        receive_deal = Deal.objects.filter(owner_accept=True).select_related('product').filter(product__owner=user)\
            .values_list('product_id', flat=True)

        offer_deal = DealOffer.objects.select_related('deal').filter(deal__offerer_accept=True)\
            .select_related('offer_product').filter(offer_product__owner=user)\
            .values_list('offer_product_id', flat=True)

        products = Product.objects.filter(owner=user).exclude(pk__in=receive_deal).exclude(pk__in=offer_deal)
        product_serializer = self.serializer_class(products, context={'request': request}, many=True)
        return Response(product_serializer.data, status.HTTP_200_OK)

        # receive_deal = Deal.objects.filter(product__in=products)
        # offer_dealoffer = DealOffer.objects.filter(offer_product=product)
        # offer_deal = Deal.objects.filter(dealoffer__in=offer_dealoffer)


        # products_unavaliable = Deal.objects.filter(
        #     Q(product__in=products) | Q(with_product__in=products),
        #     Q(owner_accept=True)
        # )
        # products_unavaliable_ids = products_unavaliable.values_list('product', flat=True)
        # products_avaliable = products.exclude(pk__in=products_unavaliable_ids)
        # print(products_avaliable[0])

        # product_serializer = self.serializer_class(products_avaliable, context={'request': request}, many=True)
        # return Response(product_serializer.data, status.HTTP_200_OK)

    # def perform_create(self, serializer):
    #     print(serializer.data)
    #     serializer.save(owner=self.request.user)

class DealManagerViewSet(viewsets.ModelViewSet):

    def retrieve(self, request):

        pass

class DealViewSet(viewsets.ModelViewSet):
    serializer_class = DealSerializer
    queryset = Deal.objects.all()

    def list(self, request):
        context = []
        products = Product.objects.filter(owner=request.user)

        for product in products:
            data = {}
            receive_deal = Deal.objects.filter(product=product).order_by('pk')
            offer_dealoffer = DealOffer.objects.filter(offer_product=product)
            offer_deal = Deal.objects.filter(dealoffer__in=offer_dealoffer)

            product_serializer = ProductSerializer(product, context={'request': request})
            receive_deals_serializer = DealSerializer(receive_deal, many=True, context={'request': request})
            offer_deals_serializer = DealSerializer(offer_deal, many=True, context={'request': request})

            data["product"] = product_serializer.data
            data["receive_deals"] = receive_deals_serializer.data
            data["offer_deals"] = offer_deals_serializer.data
            context.append(data)

        return Response(context, status.HTTP_200_OK)

    def create(self, request):
        product = Product.objects.get(pk=request.data.get('product_id'))
        offer_products = []
        for offer_product_req in request.data.get('offer_products'):
            offer_product = Product.objects.get(pk=offer_product_req.id, owner=request.user)
            if not offer_product:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            offer_products.append(offer_products)

        deal_serializer = DealSerializer(data={
            'product': product,
            'deal_offer': offer_products,
            'quantity': offer_product_req.quantity
        })

        if deal_serializer.is_valid():
            return Response(deal_serializer.data, status.HTTP_200_OK)
        return Response(deal_serializer.errors, status.HTTP_400_BAD_REQUEST)


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
