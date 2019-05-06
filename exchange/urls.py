from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from exchange import views

product_list = views.ProductViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

product_detail = views.ProductViewSet.as_view({
    'get': 'retrieve'
})

product_avaliable_by_user = views.ProductViewSet.as_view({
    'get': 'list_avaliable_by_user'
})

deal_offer_product = views.ProductViewSet.as_view({
    'get': 'get_offer_product'
})

deal_list = views.DealViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

deal_detail = views.DealViewSet.as_view({
    'get': 'retrieve'
})

deal_owner_accept = views.DealViewSet.as_view({
    'post': 'accept_deal'
})

deal_score = views.DealViewSet.as_view({
    'post': 'give_score'
})

urlpatterns = [
    path('', views.api_root),
    path('product/', product_list, name='product-list'),
    path('product/<int:pk>/', product_detail, name='product-detail'),
    path('product/user/<int:pk>/', product_avaliable_by_user),
    path('product-offer/<int:pk>/', deal_offer_product),
    path('category/', views.CategoryList.as_view(), name='category-list'),
    path('category/<int:pk>/', views.CategoryDetail.as_view(), name='category-detail'),
    path('upload/product/', views.ProductImageUploadView.as_view(), name='upload-image'),
    path('deal/', deal_list, name="deal-list"),
    path('deal/<int:pk>/', deal_detail, name="deal-detail"),
    path('deal/accept/<int:pk>', deal_owner_accept),
    path('deal/<int:pk>/score/', deal_score)
]

urlpatterns = format_suffix_patterns(urlpatterns)
