from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.utils import timezone

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=125, null=False)
    last_name = models.CharField(max_length=125, null=False)
    birthday = models.DateField(null=True)

    MALE = 'M'
    FEMALE = 'F'
    OTHER = 'X'

    GENDER = (
        (MALE, 'ชาย'),
        (FEMALE, 'หญิง'),
        (OTHER, 'อื่นๆ')
    )

    gender = models.CharField(choices=GENDER, max_length=1, null=True)
    phone = models.CharField(max_length=225, null=False)
    picture = models.CharField(max_length=225, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

class Categories(models.Model):
    name = models.CharField(max_length=125, null=False)
    detail = models.TextField(null=True)

class Products(models.Model):
    name = models.CharField(max_length=125, null=False)
    detail = models.TextField(null=False)
    quantity = models.IntegerField(null=False)
    created_date = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(Categories, on_delete=models.DO_NOTHING, null=True, blank=False)
    want_product = models.CharField(max_length=125)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

class Product_picture(models.Model):
    picture_path = models.CharField(max_length=125)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)

class Phones(models.Model):
    phone_number = models.CharField(max_length=10)
    is_verification = models.BooleanField()

class Feedback(models.Model):
    title = models.CharField(max_length=125)
    detail = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

class Exchange(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name="product")
    with_product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name="with_product")
    owner_accept = models.BooleanField(null=True)
    created_date = models.DateTimeField(default=timezone.now)
