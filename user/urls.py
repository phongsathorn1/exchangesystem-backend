from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from user import views

urlpatterns = [
    path('register/', views.create_user, name='user-register'),
    path('auth/', obtain_jwt_token),
    path('auth/refresh/', refresh_jwt_token),
    path('auth/verify/', verify_jwt_token),
    path('me/', views.get_me, name='user-me'),
    path('user/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
    path('phone-check/', views.check_phone, name='phone-check')
]

urlpatterns = format_suffix_patterns(urlpatterns)
