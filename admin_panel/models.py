from django.db import models
from datetime import datetime, timedelta
from products.models import ColorVarient
# Create your models here.

class Banners(models.Model):

    subtitle = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    image = models.ImageField(upload_to='banners')
    is_listed = models.BooleanField(default=True)
    variant = models.ForeignKey(ColorVarient, on_delete=models.CASCADE, null=True)
