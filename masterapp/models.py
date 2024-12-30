from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import UserManager
# Create your models here.



class Users(AbstractBaseUser,PermissionsMixin):

    name=models.CharField(max_length=40)
    password=models.CharField(max_length=100,null=True)
    email=models.EmailField(verbose_name='email',max_length=200,unique=True)

    ADD_TYPE=(       

        ('home','home'),
        ('office','office')
    )

    address=models.CharField(max_length=20,choices=ADD_TYPE,null=True)
    create_at=models.DateTimeField(auto_now=True,blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    objects = UserManager()

    class Meta:
        db_table='User'



