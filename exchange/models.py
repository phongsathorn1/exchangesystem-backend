from django.db import models
from django.utils import timezone

class Categories(models.Model):
    name = models.CharField(max_length=125, null=False)
    detail = models.TextField(null=True)

class Products(models.Model):
    name = models.CharField(max_length=125, null=False)
    detail = models.TextField(null=False)
    quantity = models.IntegerField(null=False)
    created_date = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(Categories, on_delete=models.DO_NOTHING, null=True, blank=False)

class Phones(models.Model):
    phone_number = models.CharField(max_length=10)
    is_verification = models.BooleanField()

class Users(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    email = models.EmailField()
    birthday = models.DateField()

    MALE = 'M'
    FEMALE = 'F'
    OTHER = 'X'

    GENDER = (
        (MALE, 'ชาย'),
        (FEMALE, 'หญิง'),
        (OTHER, 'อื่นๆ')
    )

    gender = models.CharField(choices=GENDER, max_length=1)
    phone = models.OneToOneField(Phones, on_delete=models.CASCADE)
    products = models.ForeignKey(Products, on_delete=models.CASCADE)
    picture = models.CharField(max_length=225, null=True)

class Feedback(models.Model):
    title = models.CharField(max_length=125)
    detail = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
