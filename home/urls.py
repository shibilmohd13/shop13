from django.urls import path,include
from . import views


urlpatterns = [
    path('',views.home, name='home'),
    path('shop/',views.shop, name='shop'),
    path('product_details/<str:id>',views.product_details, name='product_details'),
    path('about/',views.about, name='about'),
    path('contact/',views.contact, name='contact'),
    path('logout/',views.logout_view, name='logout'),
    path('search/',views.search, name='search'),
    path('get_color_variant_details/<str:id>',views.get_color_variant_details,name='get_color_variant_details')
    

]
