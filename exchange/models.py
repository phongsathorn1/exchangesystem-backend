from django.db import models
from django.utils import timezone
from user.models import User

class Category(models.Model):
    name = models.CharField(max_length=125, null=False)
    detail = models.TextField(null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=125, null=False)
    detail = models.TextField(null=False)
    quantity = models.IntegerField(null=False)
    created_date = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, null=True, blank=False)
    want_product = models.CharField(max_length=125)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Product_picture(models.Model):
    picture_path = models.CharField(max_length=125)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.picture_path

class Phone(models.Model):
    phone_number = models.CharField(max_length=10)
    is_verification = models.BooleanField()

    def __str__(self):
        return self.phone_number

class Feedback(models.Model):
    title = models.CharField(max_length=125)
    detail = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class Exchange(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product")
    with_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="with_product")
    owner_accept = models.BooleanField(null=True)
    created_date = models.DateTimeField(default=timezone.now)
