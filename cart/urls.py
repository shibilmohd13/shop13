from django.urls import path
from . import views


urlpatterns = [
    path('',views.cart, name="cart"),
    path('addtocart',views.addtocart, name='addtocart'),
    path('remove_item_from_cart/', views.remove_item_from_cart, name='remove_item_from_cart'),
    path('update_cart', views.update_cart, name="update_cart"),
    path('checkout', views.checkout ,name="checkout"),
    path('add_address_checkout',views.add_address_checkout, name='add_address_checkout'),
    path('edit_address_checkout/<str:id>',views.edit_address_checkout, name='edit_address_checkout'),
    path('place_order',views.place_order,name='place_order'),
    path('place_order_razorpay',views.place_order_razorpay,name='place_order_razorpay'),
    path('place_order_wallet',views.place_order_wallet,name='place_order_wallet'),
    path('apply_coupons', views.apply_coupons, name='apply_coupons'),
    path('remove_coupon', views.remove_coupon, name='remove_coupon'),

    
]
