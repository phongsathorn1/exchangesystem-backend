import datetime

from rest_framework import serializers
from django.contrib.auth import get_user_model

class UserPictureSerializer(serializers.ModelSerializer):
    picture = serializers.ImageField(required=False)

    class Meta:
        model = get_user_model()
        fields = ('picture',)

class UserSerializer(serializers.ModelSerializer):
    picture = serializers.ImageField(required=False)
    phone = serializers.CharField(max_length=10, required=True)
    password = serializers.CharField(max_length=225, required=True, write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'birthday', 'gender',
                  'picture', 'phone', 'firebase_uid', 'picture')

    def validate_birthday(self, value):
        if value > datetime.datetime.now().date():
            raise serializers.ValidationError("วันเกิดต้องไม่มากกว่าปัจจุบัน")
        if value > datetime.datetime.now().date() - datetime.timedelta(days=365*18):
            raise serializers.ValidationError("ต้องมีอายุตั้งแต่ 18 ปีขึ้นไป")
        return value

class UserViewSerializer(serializers.ModelSerializer):
    picture = serializers.ImageField(required=False)

    class Meta:
        model = get_user_model()
        fields = ('id', 'url', 'email', 'first_name', 'last_name', 'birthday', 'gender', 'picture', 'phone')
