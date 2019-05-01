from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from user import views

urlpatterns = [
    path('register/', views.create_user, name='user_register'),
    path('user/<int:pk>/', views.UserDetail.as_view(), name='user')
]

urlpatterns = format_suffix_patterns(urlpatterns)
