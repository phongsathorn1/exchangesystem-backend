import os
import uuid

from django.db.models import Q
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, BasePermission
from rest_framework.reverse import reverse
from rest_framework import mixins, generics, status, viewsets, views, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from exchange.models import Product, Category, Product_picture, Deal, DealOffer, Notification, Feedback, Chat
from exchange.serializers import ProductSerializer, CategoriesSerializer, ProductPictureSerializer, \
    ProductPictureUploadSerializer, DealSerializer, DealOfferSerializer, NotificationSerializer, FeedbackSerializer, \
    ChatSerializer
from user.models import User


@api_view(['GET'])
@permission_classes((AllowAny, ))
def api_root(request, format=None):
    return Response({
        'register': reverse('user-register', request=request, format=format),
        'products': reverse('product-list', request=request, format=format)
    })

class IsAuthenticatedOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve']:
            return True
        elif request.user:
            return True
        return False

class ProductViewSet(viewsets.ModelViewSet):

    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        queryset = Product.objects.filter(is_avaliable=True)
        keyword = self.request.query_params.get('q', None)
        category = self.request.query_params.get('category', None)

        if keyword is not None:
            if category is not None:
                queryset = Product.objects.filter(name__icontains=keyword, category__name__contains=category)
            else:
                queryset = Product.objects.filter(name__icontains=keyword)

        # if self.request.user.is_authenticated:
        #     queryset = queryset.exclude(owner=self.request.user)

        return queryset

    def retrieve(self, request , pk=None):
        retrive_queryset = Product.objects.get(pk=pk)
        context = {'request': request}
        serializer_class = ProductSerializer(retrive_queryset, context=context)
        return Response(serializer_class.data, status.HTTP_200_OK)

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

    def get_offer_product(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)
        product_serializer = ProductSerializer(product, context={'request': request})
        context = {
            'product': product_serializer.data,
            'avaliable_offer_products': self.get_list_avaliable_by_user(request, pk=request.user.id)
        }
        return Response(context, status.HTTP_200_OK)

    def list_avaliable_by_user(self, request, pk=None):
        return Response(self.get_list_avaliable_by_user(request, pk=pk), status.HTTP_200_OK)

    def get_list_avaliable_by_user(self, request, pk=None):
        user = User.objects.get(pk=pk)
        if not user:
            return None

        receive_deal = Deal.objects.filter(owner_accept=True).select_related('product').filter(product__owner=user)\
            .values_list('product_id', flat=True)

        offer_deal = DealOffer.objects.select_related('deal').filter(deal__offerer_accept=True)\
            .select_related('offer_product').filter(offer_product__owner=user)\
            .values_list('offer_product_id', flat=True)

        products = Product.objects.filter(owner=user).exclude(pk__in=receive_deal).exclude(pk__in=offer_deal)
        product_serializer = self.serializer_class(products, context={'request': request}, many=True)
        return product_serializer.data

class DealViewSet(viewsets.ModelViewSet):
    serializer_class = DealSerializer
    queryset = Deal.objects.all()
    permission_classes = (IsAuthenticated,)

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

    def delete(self, request, pk=None):
        notification = Notification.objects.get(action="deal:%s" %pk)
        deal = Deal.objects.get(pk=pk)

        notification.delete()
        deal.delete()

        data = {
            'success': True
        }

        return Response(data, status.HTTP_200_OK)

    def create(self, request):
        product = Product.objects.get(pk=request.data.get('product_id'))
        offer_products = []
        for offer_product_req in request.data.get('offer_products'):
            offer_product = Product.objects.get(pk=offer_product_req['id'], owner=request.user)
            if not offer_product:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            offer_products.append({
                'product': offer_product,
                'quantity': offer_product_req['quantity']
            })

        deal = Deal.objects.create(
            product=product
        )

        for offer_product in offer_products:
            DealOffer.objects.create(
                deal=deal,
                offer_product=offer_product['product'],
                quantity=offer_product['quantity']
            )

        notification = Notification.objects.create(
            user=product.owner,
            title="ได้รับข้อเสนอ",
            message="สินค้า %s มีผู้ยื่นข้อเสนอขอแลกเปลี่ยนสิ่งของด้วย" %(product.name),
            action="deal:%s" %(deal.id)
        )

        deal_serializer = DealSerializer(deal, context={'request': request})
        return Response(deal_serializer.data, status.HTTP_200_OK)

    def accept_deal(self, request, pk=None):
        deal = get_object_or_404(Deal, pk=pk)
        product_owner = Product.objects.filter(pk=deal.product.id, owner=request.user)
        if product_owner.exists():
            deal.owner_accept = True
            deal.save()
        else:
            is_deal_offer = DealOffer.objects.select_related('offer_product').filter(
                deal=pk).filter(offer_product__owner=request.user)

            if is_deal_offer.exists():
                deal = Deal.objects.get(pk=pk)
                if deal.owner_accept:
                    deal.offerer_accept = True
                    deal.save()
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)

        deal_serializer = DealSerializer(deal, context={'request': request})
        return Response(deal_serializer.data, status.HTTP_200_OK)

    def give_score(self, request, pk=None):
        deal = get_object_or_404(Deal, pk=pk)
        product_owner = Product.objects.filter(pk=deal.product.id, owner=request.user)
        if product_owner.exists():
            deal.offerer_score = request.data.get('score')
            deal.save()
        else:
            is_deal_offer = DealOffer.objects.select_related('offer_product').filter(
                deal=pk).filter(offer_product__owner=request.user)

            if is_deal_offer.exists():
                deal = Deal.objects.get(pk=pk)
                deal.owner_score = request.data.get('score')
                deal.save()
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        if deal.owner_score is not None and deal.offerer_score is not None:
            deal.product.is_avaliable = False
            deal.product.quantity = 0
            for offer in deal.dealoffer_set.all():
                if offer.offer_product.quantity == offer.quantity:
                    offer.offer_product.is_avaliable = False
                offer.offer_product.quantity -= offer.quantity
                offer.offer_product.save()
            deal.product.save()

        deal_serializer = DealSerializer(deal, context={'request': request})
        return Response(deal_serializer.data, status.HTTP_200_OK)

class ProductPictureViewSet(viewsets.ModelViewSet):

    def retrieve(self, request, pk=None):
        queryset = Product_picture.objects.all()
        product_picture = get_object_or_404(queryset, pk=pk)
        serializer = ProductPictureSerializer(product_picture)
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

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-id')

    def update(self, request, pk=None):
        notification = Notification.objects.get(pk=pk)
        notification.is_readed = True
        notification.save()

        notiSerializer = NotificationSerializer(notification)
        return Response(notiSerializer.data, status.HTTP_200_OK)

class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = (AllowAny,)

class ChatViewSet(viewsets.ModelViewSet):
    serializer_class = ChatSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, pk=None):
        deal = Deal.objects.get(pk=pk)
        chat = Chat.objects.filter(deal=deal)
        chatSerializer = self.serializer_class(chat, many=True, context={'request': request})
        return Response(chatSerializer.data, status.HTTP_200_OK)

    def create(self, request, pk=None):
        deal = Deal.objects.get(pk=pk)
        chatSerializer = self.serializer_class(data={
            'message': request.data.get('message'),
            # 'user': request.user.id,
            # 'deal': deal.pk
        }, context={'request': request})

        if(chatSerializer.is_valid()):
            chatSerializer.save(user=request.user, deal=deal)
            return Response(chatSerializer.data, status.HTTP_200_OK)
        return Response(chatSerializer.errors, status.HTTP_400_BAD_REQUEST)
