from django.contrib import admin
from .models import Orders,OrdersItem
# Register your models here.

admin.site.register(Orders)
admin.site.register(OrdersItem)

