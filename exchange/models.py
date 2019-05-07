import uuid

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
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, null=False, blank=False)
    want_product = models.CharField(max_length=125)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ('created_date',)

    def __str__(self):
        return self.name

class Product_picture(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    picture_path = models.ImageField(upload_to='product_images')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_date = models.DateTimeField(default=timezone.now)

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
#
# class Exchange(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product")
#     with_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="with_product")
#     owner_accept = models.BooleanField(null=True)
#     created_date = models.DateTimeField(default=timezone.now)

class Deal(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    owner_accept = models.BooleanField(null=True)
    offerer_accept = models.BooleanField(null=True)
    created_date = models.DateTimeField(default=timezone.now)
    expired_datetime = models.DateTimeField(null=True)
    is_cancel = models.BooleanField(null=True)
    owner_score = models.IntegerField(null=True)
    offerer_score = models.IntegerField(null=True)

class DealOffer(models.Model):
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE)
    offer_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=225)
    message = models.TextField()
    action = models.CharField(max_length=100)
    is_readed = models.BooleanField(default=False)
