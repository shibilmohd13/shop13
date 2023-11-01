from django.contrib import admin
from .models import Address, CustomUser

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Address)