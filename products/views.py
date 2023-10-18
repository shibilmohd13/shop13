from django.shortcuts import render,redirect

# Create your views here.

def products(request):
    return render(request, 'admin_panel/products.html')
