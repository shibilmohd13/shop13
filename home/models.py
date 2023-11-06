from django.db import models
import smtplib
from django.db.models.signals import post_save
from django.dispatch import receiver
import os
# Create your models here.

# Model for saving enquiry from about section
class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.CharField(max_length=50)
    message = models.TextField()


# signal for sending mail when a new data added to the Contact model
@receiver(post_save, sender=Contact)
def send_contact(sender,instance, **kwargs):
    message = f"Subject: Enquiry SHOP13 \n\n From :- {instance.first_name} {instance.last_name} | Email :- {instance.email}\n\n{instance.message}"
    sender_email = os.environ.get("SENDER_EMAIL")
    sender_pass = os.environ.get("SENDER_PASS")
    connection = smtplib.SMTP('smtp.gmail.com', 587)
    connection.starttls()
    connection.login(user=sender_email, password=sender_pass)
    connection.sendmail(from_addr=sender_email, to_addrs="shibilmhdjr13@gmail.com", msg=message)
    connection.close()
    



