from django.db import models
import smtplib
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.CharField(max_length=50)
    message = models.TextField()

@receiver(post_save, sender=Contact)
def send_contact(sender,instance, **kwargs):
    message = f"Subject: Enquiry SHOP13 \n\n From :- {instance.first_name} {instance.last_name} | Email :- {instance.email}\n\n{instance.message}"
    sender_email = "shop13ecommerce@gmail.com"
    sender_pass = 'vqor ejqp zexj omko'
    connection = smtplib.SMTP('smtp.gmail.com', 587)
    connection.starttls()
    connection.login(user=sender_email, password=sender_pass)
    connection.sendmail(from_addr=sender_email, to_addrs="shibilmhdjr13@gmail.com", msg=message)
    connection.close()
    



