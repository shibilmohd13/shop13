from django.urls import path,include
from . import views


urlpatterns = [
    path('',views.home, name='home'),
    path('shop/',views.shop, name='shop'),
    path('shop/product_details/<str:id>',views.product_details, name='product_details'),
    path('about/',views.about, name='about'),
    path('contact/',views.contact, name='contact'),
    path('logout/',views.logout, name='logout'),

]
