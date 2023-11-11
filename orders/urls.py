from django.urls import path
from . import views

urlpatterns = [
    path('',views.orders,name='orders'),
    path('view_order',views.view_orders,name='view_order'),
    path('cancel_order/<str:id>',views.cancel_order,name='cancel_order'),

    
]
