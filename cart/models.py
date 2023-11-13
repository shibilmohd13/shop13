from django.db import models
from userlogin.models import *
from products.models import *

# Create your models here.


# Cart Model
class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(ColorVarient, on_delete=models.CASCADE)
    prod_quantity = models.IntegerField(null=False, blank=False,default=1)
    cart_price = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=False)



    def __str__(self):
        return f"{self.user.fullname}'s Cart - Prod : {self.product.product.name} {self.product.color} , Quantity : {self.prod_quantity}"







