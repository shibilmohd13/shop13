from django.shortcuts import render,redirect
from products.models import *
import smtplib

# Create your views here.
def home(request):
    obj = Product.objects.all()[:8]
    return render(request, 'home/home.html', {'obj': obj})

def shop(request):
    obj = Product.objects.all()
    clr = Color.objects.all()
    return render(request, 'home/shop.html', {'obj': obj , 'colors_nav': clr})

def product_details(request,id):
    obj = Product.objects.filter(id=id)[0]
    return render(request, 'home/details.html', {'item': obj})

def logout(request):
    request.session.flush()
    return redirect('home')

def about(request):
    return render(request, 'home/about.html')


def contact(request):
    if request.method == "POST":
        email = request.POST['email']
        message = f"Subject: Enquiry SHOP13 \n\n From :- {request.POST['first_name']} {request.POST['last_name']} | Email :- {email}\n\n{request.POST['message']}"
        sender_email = "shop13ecommerce@gmail.com"
        sender_pass = 'vqor ejqp zexj omko'
        connection = smtplib.SMTP('smtp.gmail.com', 587)
        connection.starttls()
        connection.login(user=sender_email, password=sender_pass)
        connection.sendmail(from_addr=sender_email, to_addrs="shibilmhdjr13@gmail.com", msg=message)
        connection.close()
        return redirect("contact")
    return render(request, 'home/contact.html')
