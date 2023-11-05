from unicodedata import category
from django.shortcuts import render,redirect
from products.models import *
from userlogin.models import CustomUser
import smtplib
from . models import Contact
from django.contrib.auth import logout
from django.http import JsonResponse
from django.db.models import Q



# Create your views here.
def home(request):
    obj = Product.objects.prefetch_related('colorvarient_set__productimage_set').filter(is_listed=True).order_by('id')
    return render(request, 'home/home.html', {'obj': obj})

def shop(request):
    obj = Product.objects.prefetch_related('colorvarient_set__productimage_set').filter(is_listed=True).order_by('id')
    return render(request, 'home/shop.html', {'obj': obj })

def product_details(request,id):
    # obj = Product.objects.prefetch_related('colorvarient_set__productimage_set').filter(is_listed=True, id=id).first()

    obj = ColorVarient.objects.prefetch_related('productimage_set').get(id=id)
    all_variants = ColorVarient.objects.filter(product=obj.product).prefetch_related('productimage_set').filter(is_listed=True).order_by("color")

    return render(request, 'home/details.html', {'item': obj, 'all_varients': all_variants })


def get_color_variant_details(request, id):
    try:
        color_variant = ColorVarient.objects.get(id=id)
        image_urls = [img.image.url for img in color_variant.productimage_set.all()] # Get image URLs
        image_urls.reverse()
        data = {
            'discounted_price': color_variant.discounted_price,
            'price': color_variant.price,
            'color': color_variant.color,
            'quantity': color_variant.quantity,
            'id': color_variant.id,
            'image_urls': image_urls # Get image URLs

            
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
    search_query = request.GET.get('search', '')  # Get the search query from the request

    # Create a Q object for searching through product names
    name_query = Q(name__icontains=search_query)

    # Create a Q object for searching through category names
    category_query = Q(category__name__icontains=search_query)

    # Create a Q object for searching through brand names
    brand_query = Q(brands__name__icontains=search_query)

    # Combine the three Q objects using the OR operator (|)
    combined_query = name_query | category_query | brand_query

    # Use the combined query to filter the Product objects
    products_match = Product.objects.filter(
        combined_query, is_listed=True
    )

    print(products_match)
    return render(request, "home/shop.html", {'obj': products_match})


