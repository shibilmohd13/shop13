from django.db import models

from userlogin.models import CustomUser
# Create your models here.

class Coupons(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=50, unique=True)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    minimum_purchase = models.DecimalField(max_digits=10, decimal_places=2,default=0, null=True, blank=True)
    expiration_date = models.DateField()
    usage_limit = models.PositiveIntegerField(default=1)
    used_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
        

class CouponUsage(models.Model):
    coupon = models.ForeignKey(Coupons, on_delete=models.SET_NULL, related_name='usage', null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name="coupon", null=True)
    total_amount = models.PositiveIntegerField(null=True)
    applied_on = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.coupon.name} of {self.user.fullname}'
