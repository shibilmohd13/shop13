from django.shortcuts import render,redirect
from products.models import *
from userlogin.models import CustomUser
import smtplib
from . models import Contact
from django.contrib.auth import logout
from django.http import JsonResponse


# Create your views here.
def home(request):
    obj = Product.objects.prefetch_related('colorvarient_set__productimage_set').filter(is_listed=True).order_by('id')
    return render(request, 'home/home.html', {'obj': obj})

def shop(request):
    obj = Product.objects.prefetch_related('colorvarient_set__productimage_set').filter(is_listed=True).order_by('id')
    return render(request, 'home/shop.html', {'obj': obj })

def product_details(request,id):
    # obj = Product.objects.prefetch_related('colorvarient_set__productimage_set').filter(is_listed=True, id=id).first()

    obj = ColorVarient.objects.prefetch_related('productimage_set').filter(id=id).first()
    all_variants = ColorVarient.objects.filter(product=obj.product).prefetch_related('productimage_set').filter(is_listed=True)

    return render(request, 'home/details.html', {'item': obj, 'all_varients': all_variants })


def get_color_variant_details(request, id):
    try:
        color_variant = ColorVarient.objects.get(id=id)
        data = {
            'discounted_price': color_variant.discounted_price,
            'price': color_variant.price,
            'color': color_variant.color,
        }
        return JsonResponse(data)
    except ColorVarient.DoesNotExist:
        return JsonResponse({'error': 'ColorVariant not found'}, status=404)




def logout_view(request):
    request.session.flush()
    return redirect('home')

def about(request):
    return render(request, 'home/about.html')


def contact(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone = request.POST['phone']
        email = request.POST['email']
        user_message = request.POST['message']
        Contact.objects.create(first_name=first_name, last_name=last_name, phone=phone, email=email, message=user_message)
        return redirect("contact")
    return render(request, 'home/contact.html')

def search(request):
    search_query = request.GET['search']
    products_match = Product.objects.filter(name__icontains=search_query,is_listed=True)
    print(products_match)
    return render(request, "home/shop.html" , {'obj': products_match})

