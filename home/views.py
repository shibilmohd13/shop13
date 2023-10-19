from django.shortcuts import render,redirect
from products.models import *

# Create your views here.
def home(request):
    obj = Product.objects.all()[:8]
    try: 
        user = request.session['fullname']
        return render(request, 'home/home.html', {'user' : user, 'obj': obj})
    except:
        return render(request, 'home/home.html', {'user' : 'Login Now', 'obj': obj})

def shop(request):
    obj = Product.objects.all()
    try: 
        user = request.session['fullname']
        return render(request, 'home/shop.html', {'user' : user, 'obj': obj})
    except:
        return render(request, 'home/shop.html', {'user' : 'Login Now', 'obj': obj})

def product_details(request,id):
    obj = Product.objects.filter(id=id)[0]
    context = {'item' : obj}
    return render(request, "home/details.html",context)

def logout(request):
    request.session.flush()
    return redirect('home')
