from datetime import date

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

NULLABLE = {'blank': True, 'null': True}


class UserRoles(models.TextChoices):
    MEMBER = 'member', _('member')


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True, default=None)

    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    country = models.CharField(max_length=50, verbose_name='страна', **NULLABLE)
    profile_image = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    role = models.CharField(max_length=9, verbose_name='статус пользователя', choices=UserRoles.choices, default=UserRoles.MEMBER)
    last_login = models.DateField(default=date.today, verbose_name='дата последнего входа')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []


