from django.shortcuts import render,redirect
from userlogin.models import *
from products.models import *
from cart.models import Cart
from django.http import JsonResponse
from django.utils import timezone  # Import timezone module



# Create your views here.
def cart(request):
    email = request.session["email"]
    user = CustomUser.objects.get(email=email)
    cart_items = Cart.objects.filter(user=user)
    context = {
        'cart_items' : cart_items
    }
    return render(request, "cart/cart.html" ,context)

def addtocart(request):
    
    if request.method == 'POST':
        if 'email' in request.session:
            email = request.session["email"]
            user = CustomUser.objects.get(email=email)
            prod_id = int(request.POST.get('product_id'))
            product_check = ColorVarient.objects.get(id=prod_id)
            if (product_check):
                if (Cart.objects.filter(user= user, product_id = prod_id)):
                    return JsonResponse({'status' : "Product already in cart"})
                else:
                    prod_qty = int(request.POST.get('product_qty'))
                    
                    if product_check.quantity >= prod_qty:
                        product = ColorVarient.objects.get(id=prod_id)
                        Cart.objects.create(user=user, product=product, prod_quantity=prod_qty, created_at=timezone.now())
                        return JsonResponse({'status' : "Product added successfully"})
                    else:
                        return JsonResponse({'status' : f"Only {str(product_check.quantity)} Quantity available"})

            else:
                return JsonResponse({'status' : "No such product"})
        else:
            return redirect('signin')
            # return JsonResponse({'status' : "login to continue"})

    return render(request, "home/details.html")


