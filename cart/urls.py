from django.urls import path,include
from . import views


urlpatterns = [
    path('',views.cart, name="cart"),

    path('addtocart',views.addtocart, name='addtocart'),
    path('remove_item_from_cart/', views.remove_item_from_cart, name='remove_item_from_cart'),

]
