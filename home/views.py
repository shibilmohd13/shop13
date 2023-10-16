from django.shortcuts import render,redirect

# Create your views here.
def home(request):
    return render(request, 'home/home.html')

def shop(request):
    return render(request, 'home/shop.html')

def product_details(request):
    return render(request, "home/details.html")
