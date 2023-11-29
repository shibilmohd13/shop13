from django.urls import path
from . import views

urlpatterns = [
    path('',views.orders,name='orders'),
    path('view_order',views.view_orders,name='view_order'),
    path('cancel_order/<str:id>',views.cancel_order,name='cancel_order'),
    path('return_order/<str:id>',views.return_order,name='return_order'),
    path('view_invoice',views.view_invoice,name='view_invoice'),

    

    
]
