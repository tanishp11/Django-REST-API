from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import UserManager
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    is_active = models.BooleanField(default=False, null=True)  # Status to mark if the category is active
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for creation
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Category'


class Sub_category(models.Model):
    name = models.CharField(max_length=50, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')  # Unique related_name
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    image = models.ImageField(upload_to='media/category_image', null=True, blank=True)
    is_active = models.BooleanField(default=False, null=True)  # Status to mark if the category is active
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for creation
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Sub-category'


class Users(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=40)
    password = models.CharField(max_length=100, null=True)
    email = models.EmailField(verbose_name='email', max_length=200, unique=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='user_categories')  # Unique related_name
    sub_category = models.ForeignKey(Sub_category, on_delete=models.CASCADE, related_name='user_subcategories')  # Unique related_name

    ADD_TYPE = (
        ('home', 'home'),
        ('office', 'office')
    )

    address = models.CharField(max_length=20, choices=ADD_TYPE, null=True)
    create_at = models.DateTimeField(auto_now=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    objects = UserManager()

    class Meta:
        db_table = 'User'
