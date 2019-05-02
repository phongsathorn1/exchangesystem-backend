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

urlpatterns = [
    path('', views.api_root),
    path('product/', product_list, name='product-list'),
    path('product/<int:pk>/', product_detail, name='product-detail'),
    path('category/', views.CategoryList.as_view(), name='category-list'),
    path('category/<int:pk>/', views.CategoryDetail.as_view(), name='category-detail'),
    path('upload/product/', views.ProductImageUploadView.as_view(), name='upload-image')
]

urlpatterns = format_suffix_patterns(urlpatterns)
