from django.db import models
from userlogin.models import CustomUser
from products.models import ColorVarient


# Create your models here.

class Wishlist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    variant = models.ForeignKey(ColorVarient,on_delete=models.CASCADE, related_name='wishlist')

    def __str__(self):
        return f"{self.user.fullname}'s Wishlist item - {self.variant.product.name} - {self.variant.color}"