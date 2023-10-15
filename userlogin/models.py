from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=50)
    email = models.EmailField(unique=True)

    def __str__(self) :
        return self.username
