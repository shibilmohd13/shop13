from django.urls import path,include
from . import views


urlpatterns = [
    path('',views.cart, name="cart"),

    path('addtocart',views.addtocart, name='addtocart')

]
