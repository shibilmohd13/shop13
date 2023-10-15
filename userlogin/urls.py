from django.urls import path
from . import views

urlpatterns = [
    path('',views.signin,name='signin'),
    path('signup/',views.signup,name='signup'),
    path('otp/',views.otp, name='otp'),
    path('home/',views.landing, name='landing'),
    # path('admin_panel/')
]
