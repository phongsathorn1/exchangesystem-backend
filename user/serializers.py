from rest_framework import serializers
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(max_length=10, required=True)
    password = serializers.CharField(max_length=225, required=True, write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'birthday', 'gender', 'picture', 'phone', 'firebase_uid')

class UserViewSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('url', 'email', 'first_name', 'last_name', 'birthday', 'gender', 'picture', 'phone')
