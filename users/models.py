from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, null=True)
    age = models.PositiveSmallIntegerField(null=True)
    address = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.username

