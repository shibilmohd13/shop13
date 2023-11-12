from django.db import models
from userlogin.models import CustomUser
# Create your models here.

class Wallet(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    transaction_type = models.CharField( max_length=50,null=True)
    transaction_details = models.CharField( max_length=50,null=True)
    amount = models.PositiveIntegerField(default=0)
    balance = models.PositiveIntegerField(default=0)
