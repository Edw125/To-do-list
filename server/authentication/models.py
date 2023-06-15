from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone = models.CharField(max_length=15, null=True, unique=True)
    telegram_id = models.CharField(max_length=15, null=True, unique=True)
