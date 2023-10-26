from django.db import models
from django.contrib.auth.models import AbstractUser
import random
import smtplib
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=50)
    fullname = models.CharField(max_length=100)
    otp = models.CharField(max_length=6, blank=True ,null=True)

    def __str__(self) :
        return self.fullname

@receiver(post_save, sender=CustomUser)
def send_otp_signal(sender, instance, **kwargs):
    sender_email = "shop13ecommerce@gmail.com"
    sender_pass = 'vqor ejqp zexj omko'
    connection = smtplib.SMTP('smtp.gmail.com', 587)
    connection.starttls()
    connection.login(user=sender_email, password=sender_pass)
    connection.sendmail(from_addr=sender_email, to_addrs=instance.email,msg=f'Subject: OTP for register \n\n Here is your OTP for create account in SHOP13\n OTP:- {instance.otp}')
    connection.close()

    
