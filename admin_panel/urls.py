from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.admin_login,name='admin_login'),
    path('admin_dash',views.admin_dash, name='admin_dash'),
    path('users',views.users,name='users'),
    path('user_status/<str:id>',views.user_status,name='user_status'),
    path('admin_logout',views.admin_logout, name='admin_logout'),
    path('orders',views.orders, name='admin_orders'),
    path('view_order_details/<str:id>', views.view_order_details,name="view_order_details"),
    path('change_order_status/<str:id>', views.change_order_status,name="change_order_status"),
]
