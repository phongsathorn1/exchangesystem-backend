from rest_framework import serializers
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(max_length=10, required=True)
    password = serializers.CharField(max_length=225, required=True)

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'first_name', 'last_name', 'birthday', 'gender', 'picture', 'phone')
