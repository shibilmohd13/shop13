from django.urls import path
from . import views

urlpatterns = [
    path('',views.orders,name='orders'),
    path('view_order',views.view_orders,name='view_order'),
    
]
