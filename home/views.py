from django.shortcuts import render,redirect

# Create your views here.
def home(request):
    try: 
        user = request.session['fullname']
        return render(request, 'home/home.html', {'user' : user})
    except:
        return render(request, 'home/home.html', {'user' : 'Login Now'})

def shop(request):
    try: 
        user = request.session['fullname']
        return render(request, 'home/shop.html', {'user' : user})
    except:
        return render(request, 'home/shop.html', {'user' : 'Login Now'})

def product_details(request):
    return render(request, "home/details.html")

def logout(request):
    request.session.flush()
    return redirect('home')
