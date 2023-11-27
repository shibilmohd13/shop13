from django.urls import path
from . import views

urlpatterns = [
    path('',views.signin,name='signin'),
    path('signup/',views.signup,name='signup'),
    path('otp/',views.otp, name='otp'),
    path('send_otp',views.send_otp,name='send_otp'),
    path('home/',views.landing, name='landing'),
    path('forget_password/',views.forget_password, name='forget_password'),
    path('reset_password/<token>/',views.reset_password, name='reset_password'),
]
