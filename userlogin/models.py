from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=50)
    fullname = models.CharField(max_length=100)

    def __str__(self) :
        return self.fullname
