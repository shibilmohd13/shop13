from django.urls import path
from . import views


urlpatterns = [
    path('',views.products, name='products'),
    path('product_status/<str:id>',views.product_status, name='product_status'),
    path('categories', views.categories, name='categories'),
    path('category_status/<str:id>', views.category_status, name='category_status'),
    path('brands', views.brands, name='brands'),
    path('brand_status/<str:id>', views.brand_status, name='brand_status'),
    path('colors', views.colors, name='colors'),
    path('color_status/<str:id>', views.color_status, name='color_status'),


]
