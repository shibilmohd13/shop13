from django.shortcuts import render,redirect
from products.models import *

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
    return render(request, 'home/contact.html')
