from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.admin_login,name='admin_login'),
    path('users',views.users,name='users'),
    path('user_status/<str:id>',views.user_status,name='user_status'),
    path('admin_logout',views.admin_logout, name='admin_logout'),
    path('orders',views.orders, name='admin_orders'),
    path('view_order_details/<str:id>', views.view_order_details,name="view_order_details"),
    path('change_order_status/<str:id>', views.change_order_status,name="change_order_status"),
    path('offers', views.offers, name="offers"),
    path('product_offers', views.product_offers, name="product_offers"),
    path('add_product_offers', views.add_product_offers, name="add_product_offers"),
    path('edit_product_offers/<str:id>', views.edit_product_offers, name="edit_product_offers"),
    path('cancel_product_offers/<str:id>', views.cancel_product_offers, name="cancel_product_offers"),
    path('category_offers', views.category_offers, name="category_offers"),
    path('add_category_offers/<str:id>', views.add_category_offers, name="add_category_offers"),
    path('cancel_category_offers/<str:id>', views.cancel_category_offers, name="cancel_category_offers"),
    path('banners', views.banners, name="banners"),
    path('add_banners', views.add_banners, name="add_banners"),
    path('edit_banners/<str:id>', views.edit_banners, name="edit_banners"),
    path('status_banner/<str:id>', views.status_banner, name="status_banner"),
    

    
    
    
]
