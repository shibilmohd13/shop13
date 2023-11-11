from django.urls import path
from . import views

urlpatterns = [
    path('',views.wallet,name='wallet'),
    path('add_to_wallet',views.add_to_wallet, name="add_to_wallet"),
    path('update_wallet', views.update_wallet,name="update_wallet")
    
]
