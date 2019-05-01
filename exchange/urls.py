from django.urls import path
from exchange import views

urlpatterns = [
    path('register', views.create_user)
]