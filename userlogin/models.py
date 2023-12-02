from django.db import models
from django.contrib.auth.models import AbstractUser
import random
import smtplib
from django.db.models.signals import post_save
from django.dispatch import receiver
import os
import datetime
from decouple import config

# CustomUser inherited from django's User model
class CustomUser(AbstractUser):
    phone = models.CharField(max_length=50)
    fullname = models.CharField(max_length=100)
    otp = models.CharField(max_length=6, blank=True ,null=True)
    otp_expiry = models.DateTimeField()
    referral_code = models.CharField(max_length=6,blank=True,null=True)
    forget_password_token = models.CharField(max_length=100, null=True, blank=True)
    # forget_timeout = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return self.email


# signal for sending otp when a user is create
@receiver(post_save, sender=CustomUser)
def send_otp_signal(sender, instance, **kwargs):
    sender_email = config("SENDER_EMAIL")
    sender_pass =  config("SENDER_PASS")
    connection = smtplib.SMTP('smtp.gmail.com', 587)
    connection.starttls()
    connection.login(user=sender_email, password=sender_pass)
    connection.sendmail(from_addr=sender_email, to_addrs=instance.email,msg=f'Subject: OTP for register \n\n Here is your OTP for create account in SHOP13\n OTP:- {instance.otp}')
    connection.close()


# Address modal
class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    street_address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pin_code = models.IntegerField()
    is_present = models.BooleanField(default=True)

    def __str__(self):
        return f'Address for {self.user.email}'
