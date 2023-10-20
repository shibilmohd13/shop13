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
    try: 
        user = request.session['fullname']
        return render(request, 'home/details.html', {'user' : user, 'item': obj})
    except:
        return render(request, 'home/details.html', {'user' : 'Login Now', 'item': obj})


def logout(request):
    request.session.flush()
    return redirect('home')

def about(request):
    try: 
        user = request.session['fullname']
        return render(request, 'home/about.html', {'user' : user})
    except:
        return render(request, 'home/about.html', {'user' : 'Login Now'})

def contact(request):
    try: 
        user = request.session['fullname']
        return render(request, 'home/contact.html', {'user' : user})
    except:
        return render(request, 'home/contact.html', {'user' : 'Login Now'})
