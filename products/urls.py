from django.urls import path
from . import views


urlpatterns = [
    path('',views.products, name='products'),
    path('categories', views.categories, name='categories'),
    path('brands', views.brands, name='brands'),
    path('product_status/<str:id>',views.product_status, name='product_status'),
    path('product_status_unlist/<str:id>',views.product_status_unlist, name='product_status_unlist'),
    path('category_status/<str:id>', views.category_status, name='category_status'),
    path('brand_status/<str:id>', views.brand_status, name='brand_status'),
    path('add_products', views.add_products,name='add_products'),
    path('add_categories', views.add_categories,name='add_categories'),
    path('add_brands', views.add_brands,name='add_brands'),
    path('edit_products/<str:id>', views.edit_products,name='edit_products'),
    path('edit_categories/<str:id>', views.edit_categories,name='edit_categories'),
    path('edit_brands/<str:id>', views.edit_brands,name='edit_brands'),
    path('unlisted_products',views.unlisted_products,name="unlisted_products"),
    path('varient_details/<str:id>',views.varient_details, name='varient_details'),
    path('add_varients/<str:id>',views.add_varients, name='add_varients'),
    path('varient_status/<str:id>',views.varient_status, name="varient_status"),
    path('edit_varients/<str:id>',views.edit_varients, name='edit_varients'),


]
