from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.admin_login,name='admin_login'),
    path('admin_dash',views.admin_dash, name='admin_dash'),
    path('users',views.users,name='users'),
]
