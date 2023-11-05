from django.urls import path,include
from . import views


urlpatterns = [
    path('',views.cart, name="cart"),

    path('addtocart',views.addtocart, name='addtocart'),
    path('remove_item_from_cart/', views.remove_item_from_cart, name='remove_item_from_cart'),
    path('update_cart', views.update_cart, name="update_cart"),
    path('checkout', views.checkout ,name="checkout"),
    path('add_address_checkout',views.add_address_checkout, name='add_address_checkout'),
    path('edit_address_checkout/<str:id>',views.edit_address_checkout, name='edit_address_checkout')

]
