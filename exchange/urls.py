from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from exchange import views

urlpatterns = [
    path('', views.api_root),
    path('product/', views.ProductList.as_view(), name='product_list'),
    path('product/<int:pk>/', views.ProductDetail.as_view(), name='product'),
    path('category/', views.CategoryList.as_view(), name='category_list'),
    path('category/', views.CategoryDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
