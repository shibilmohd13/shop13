from django.urls import path
from . import views

urlpatterns = [
    path('',views.wishlist,name='wishlist'),
    path('remove_wishlist/<str:id>',views.remove_wishlist,name='remove_wishlist'),
    path('addtowishlist',views.addtowishlist,name='addtowishlist'),
    

]
