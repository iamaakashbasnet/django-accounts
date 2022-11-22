from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='Email',
                              max_length=120, unique=True)
    username = models.CharField(
        verbose_name='Username', max_length=30, unique=True)
    first_name = models.CharField(verbose_name='First name', max_length=30)
    last_name = models.CharField(verbose_name='Last name', max_length=30)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(
        verbose_name='Date Joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='Last Login', auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    objects = UserManager()

    def __str__(self) -> str:
        return self.username
