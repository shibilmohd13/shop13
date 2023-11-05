from django.shortcuts import render,redirect
from userlogin.models import *
from products.models import *
from cart.models import Cart
from django.http import JsonResponse,HttpResponse
from django.utils import timezone  # Import timezone module



# Create your views here.
def cart(request):
    if 'email' in request.session:
        email = request.session["email"]
        user = CustomUser.objects.get(email=email)
        cart_items = Cart.objects.filter(user=user)
        subPrice = cart_items.values_list('cart_price',flat=True)
        total = sum(subPrice)
        print(subPrice)
        print(total)
        context = {
            'cart_items' : cart_items,
            'total' : total
        }
        return render(request, "cart/cart.html" ,context)
    return redirect('signin')

def addtocart(request):
    
    if request.method == 'POST':
        if 'email' in request.session:
            email = request.session["email"]
            user = CustomUser.objects.get(email=email)
            prod_id = int(request.POST.get('product_id'))
            product_check = ColorVarient.objects.get(id=prod_id)
            if (product_check):
                if (Cart.objects.filter(user= user, product= product_check)):
                    return JsonResponse({'status' : "Product already in cart"})
                else:
                    prod_qty = 1
                    
                    if product_check.quantity >= prod_qty:
                        product = ColorVarient.objects.get(id=prod_id)
                        Cart.objects.create(user=user, product=product, prod_quantity=prod_qty, cart_price=product.discounted_price, created_at=timezone.now())
                        return JsonResponse({'status' : "Product added successfully",'success' : True})
                    else:
                        return JsonResponse({'status' : f"Only {str(product_check.quantity)} Quantity available"})

            else:
                return JsonResponse({'status' : "No such product"})
        else:
            return redirect('signin')
            # return JsonResponse({'status' : "login to continue"})

    return render(request, "home/details.html")

#function for removing the item from cart
def remove_item_from_cart(request):
    if 'email' in request.session:
        if request.method == 'POST':
            item_id = request.POST.get('item_id')
            try:
                cart_item = Cart.objects.get(id=item_id)
                print(cart_item)
                cart_item.delete()
                return JsonResponse({'message': 'Item removed successfully'})
            except Cart.DoesNotExist:
                return JsonResponse({'message': 'Item not found'}, status=400)
        else:
            return JsonResponse({'message': 'Invalid request method'}, status=405)
    else:
        return redirect('signin')


#function for updating the cart details like price, quantity and other info    
def update_cart(request):
    if request.method == 'POST':
        if 'email' in request.session:
            user = request.session['email']
            use = CustomUser.objects.filter(email=user).first()
            change = int(request.POST.get('change'))
            variant_id = request.POST.get('variantId')
            varient_obj = ColorVarient.objects.get(id=variant_id)
            quantity = request.POST.get('quantity')
            print(varient_obj)
            print(user)            
            cart = Cart.objects.get(user=use, product=varient_obj)
            

            if change == 1:

                if varient_obj.quantity > cart.prod_quantity:
                    if cart.prod_quantity < 10:
                        cart.prod_quantity += 1
                        cart.save()
                    else:
                        cart.prod_quantity = 10
                        cart.save()
                else:
                    pass
            else:
                if cart.prod_quantity > 1:
                    cart.prod_quantity -= 1
                    cart.save()
                else:
                    cart.prod_quantity = 1
                    cart.save()

            priceOfInstance = varient_obj.discounted_price
            prodtotal = cart.prod_quantity * priceOfInstance
            cart.cart_price = prodtotal
            cart.save()
            cart_items = Cart.objects.filter(user=use)
            print(cart_items)
            total = sum(cart_items.values_list('cart_price',flat=True))
            print(total)

            
        response_data = {'updatedQuantity': cart.prod_quantity , 'prodtotal' : prodtotal, 'total' : total}
        return JsonResponse(response_data)

    return HttpResponse(status=200)

def checkout(request):
    email = request.session['email']
    user = CustomUser.objects.get(email=email)
    address = Address.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    total = sum(cart_items.values_list('cart_price',flat=True))


    return render(request, "cart/checkout.html" , {'addresses' : address , 'cart_items' : cart_items , 'total' : total})


def add_address_checkout(request):
    email = request.session['email']
    user = CustomUser.objects.get(email=email)
    
    name = request.POST['name']
    phone = request.POST['phone']
    street_address = request.POST['street_address']
    city = request.POST['city']
    state = request.POST['state']
    pincode = request.POST['pincode']

    new_address = Address(
        user = user,
        name = name,
        phone = phone,
        street_address = street_address,
        city = city,
        state = state,
        pin_code = pincode
    )
    new_address.save()
                
    return redirect('checkout')

def edit_address_checkout(request, id):
    address = Address.objects.get(id=id)

    name = request.POST.get('name')
    phone = request.POST.get('phone')
    street_address = request.POST.get('street_address')
    city = request.POST.get('city')
    state = request.POST.get('state')
    pincode = request.POST.get('pincode')

    address.name = name
    address.phone = phone
    address.street_address = street_address
    address.city = city
    address.state = state
    address.pin_code = pincode

    address.save()

    return redirect('checkout')



