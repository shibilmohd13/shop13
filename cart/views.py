from django.shortcuts import render,redirect
from userlogin.models import *
from products.models import *
from cart.models import Cart
from orders.models import Orders,OrdersItem
from wallet.models import Wallet
from django.http import JsonResponse,HttpResponse
from django.utils import timezone  # Import timezone module
from datetime import timedelta,datetime
from coupons.models import CouponUsage, Coupons
import razorpay
from decouple import config

# Create your views here.


# View cart
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


# Add Items to Cart
def addtocart(request):
    if request.method == 'POST':
        if 'email' in request.session:
            email = request.session["email"]
            user = CustomUser.objects.get(email=email)
            prod_id = int(request.POST.get('product_id'))
            product_check = ColorVarient.objects.get(id=prod_id)
            
            if (Cart.objects.filter(user= user, product= product_check)):
                return JsonResponse({'status' : "Product already in cart"})
            else:
                prod_qty = 1
                if product_check.quantity >= prod_qty:
                    product = ColorVarient.objects.get(id=prod_id)
                    Cart.objects.create(user=user, product=product, prod_quantity=prod_qty, cart_price=product.discounted_price(), created_at=timezone.now())
                    cart_count = Cart.objects.filter(user=user).count()
                    print(f"Cart s ajax count: {cart_count}")
                    return JsonResponse({'status' : "Product added successfully",'success' : True, "cart_count" : cart_count})
                else:
                    return JsonResponse({'status' : f"Only {str(product_check.quantity)} Quantity available"})

        else:
            return redirect('signin')

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
          
            cart = Cart.objects.get(user=use, product=varient_obj)

            if change == 1:
                if varient_obj.quantity > cart.prod_quantity:
                    cart.prod_quantity += 1
                    cart.save()
                
            else:
                if cart.prod_quantity > 1:
                    cart.prod_quantity -= 1
                    cart.save()
                else:
                    cart.prod_quantity = 1
                    cart.save()

            priceOfInstance = varient_obj.discounted_price()
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


# View checkout page
def checkout(request):
    if 'email' in request.session:
        email = request.session['email']
        user = CustomUser.objects.get(email=email)
        address = Address.objects.filter(user=user,is_present=True)
        cart_items = Cart.objects.filter(user=user)
        total = sum(cart_items.values_list('cart_price',flat=True))
        coupons = Coupons.objects.filter(is_active=True).filter(expiration_date__gte=timezone.now())

        return render(request, "cart/checkout.html" , {'addresses' : address , 'cart_items' : cart_items , 'total' : total , 'coupons': coupons})
    return redirect('signin')


# Add address view in checkout
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


# Edit address view in checkout
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



# Place order
def place_order(request):
    if 'email' in request.session:
        email = request.session.get("email")
        user = CustomUser.objects.get(email=email)
        
        print("!!!!!!!!!!!!!!!!!!!!!!!!!enterd!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        address_id = request.POST.get('selected_address')
        new_address = Address.objects.get(id=address_id)
        print(f'!!!!!!!!!!!!!!!!!!!!!!!!!{new_address}!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        payment_method = request.POST.get("payment")


        cart_items = Cart.objects.filter(user=user)
        for item in cart_items:
            if item.prod_quantity > item.product.quantity :
                return JsonResponse({'success' : False , 'message' : "Some items Out of stock"})



        total_amount_coupon=request.POST.get('total_amount')
        print(f'total_amount_coupon: {total_amount_coupon}')

        print("!!!!!!!!!!!!!!!!!!!!!!! Going to create!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        if cart_items.exists():
            # Create an Orders object
            order = Orders.objects.create(
                user=user,
                address=new_address,
                payment_method=payment_method,
                total_amount=total_amount_coupon,  # You'll calculate the total amount in the next step
                quantity=0,  # You'll calculate the total quantity in the next step

            )
            print("!!!!!!!!!!!!!!!!!!!!!  created  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            order.expected_delivery_date = order.order_date + timedelta(days=7)

            # Initialize total_amount and quantity to 0
            total_amount = 0
            total_quantity = 0

            # Create OrdersItem objects and calculate the total amount and quantity
            for item in cart_items:
                order_item = OrdersItem.objects.create(
                    order=order,
                    variant=item.product,
                    quantity=item.prod_quantity,
                    price=item.product.discounted_price(),
                    status='Order confirmed',  # Set the default status here

                )
                order_item.save()

                # Calculate the total amount and quantity
                total_amount += item.prod_quantity * item.product.discounted_price()
                total_quantity += item.prod_quantity

                # Reduce the quantity of the ColorVariant in the order
                color_variant = item.product
                color_variant.quantity -= item.prod_quantity
                color_variant.save()

            # Update the total_amount and quantity in the Orders object
            order.total_amount = total_amount_coupon
            order.quantity = total_quantity
            order.save()
            print("order sucess")

            # Moving order id into session for future use
            request.session['order_id'] = str(order.order_id)
            

            # Clear the user's cart after the order is placed
            cart_items.delete()

            return JsonResponse({"success": 'Order placed successfully'})
        else:
            return JsonResponse({'success' : False , 'message' : "your cart is empty"})

    return JsonResponse({"error": 'User not authenticated'})


client = razorpay.Client(auth=(config("KEY_ID"), config("KEY_SECRET")))


def place_order_razorpay(request):
    email = request.session['email']
    user = CustomUser.objects.get(email=email)
    print(user)

    cart_items = Cart.objects.filter(user=user)
    for item in cart_items:
            if item.prod_quantity > item.product.quantity :
                return JsonResponse({'success' : False , 'message' : "Some items Out of stock"})

    # cart_total = 0
    # for item in cart :
    #     cart_total += (item.product.discounted_price * item.prod_quantity)

    cart_total = int(float(request.POST.get('total_amount'))) * 100
    print(cart_total)

    print(client)
    data = { "amount": cart_total, "currency": "INR" }
    print(data)
    payment = client.order.create(data=data)
    

    return JsonResponse({
        'total_price' : cart_total, "success" : True, 'payment' : payment,'payment_id': payment['id']
    })

def place_order_wallet(request):
    if 'email' in request.session:
        email = request.session.get("email")
        user = CustomUser.objects.get(email=email)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        address_id = request.POST.get('selected_address')
        print(address_id)
        address = Address.objects.get(id=address_id)
        print(address)

        payment_method = request.POST.get("payment")

        cart_items = Cart.objects.filter(user=user)
        for item in cart_items:
            if item.prod_quantity > item.product.quantity :
                return JsonResponse({'success' : False , 'message' : "Some items Out of stock"})
        
        if cart_items.exists():
            wallet = Wallet.objects.filter(user=user).order_by("-id")

            if wallet:
                balance = wallet.first().balance
            else: 
                balance = 0

            total_cart_price =  sum(cart_items.values_list('cart_price',flat=True))

            total_amount_coupon=int(float(request.POST['total_amount']))
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            if balance >= total_amount_coupon:
                # Create an Orders object
                order = Orders.objects.create(
                    user=user,
                    address=address,
                    payment_method=payment_method,
                    total_amount=total_amount_coupon,  
                    quantity=0,  # calculate the total quantity in the next step

                )
                print("###################################################")
                order.expected_delivery_date = order.order_date + timedelta(days=7)

                # Initialize total_amount and quantity to 0
                total_amount = 0
                total_quantity = 0

                # Create OrdersItem objects and calculate the total amount and quantity
                for item in cart_items:
                    order_item = OrdersItem.objects.create(
                        order=order,
                        variant=item.product,
                        quantity=item.prod_quantity,
                        price=item.product.discounted_price(),
                        status='Order confirmed',  # Set the default status here

                    )
                    order_item.save()

                    # Calculate the total amount and quantity
                    total_amount += item.prod_quantity * item.product.discounted_price()
                    total_quantity += item.prod_quantity

                    # Reduce the quantity of the ColorVariant in the order
                    color_variant = item.product
                    color_variant.quantity -= item.prod_quantity
                    color_variant.save()

                # Update the total_amount and quantity in the Orders object
                order.total_amount = total_amount_coupon
                order.quantity = total_quantity
                order.save()
                print("order sucess")

                # Updating wallet
                
                new_balance = balance - total_amount_coupon
                Wallet.objects.create(
                    user=user,
                    amount=total_amount_coupon,
                    balance=new_balance,
                    transaction_type = "Debit",
                    transaction_details = f"Debited Money through Purchase"
                )

                # Moving order id into session for future use
                request.session['order_id'] = str(order.order_id)
                

                # Clear the user's cart after the order is placed
                cart_items.delete()
            else:
                return JsonResponse({'success' : False , 'message' : "You have no enough balance"})

            return JsonResponse({"success": 'Order placed successfully'})
        else:
            return JsonResponse({'success' : False , 'message' : "your cart is empty"})

    return JsonResponse({"error": 'User not authenticated'})


def apply_coupons(request):
    if request.method == 'POST':
        email = request.session.get("email")
        user = CustomUser.objects.get(email=email)

        coupon_code = request.POST.get('couponCode', '')
        coupen_check = Coupons.objects.filter(code=coupon_code,is_active=True).first()
        if coupen_check:
            if CouponUsage.objects.filter(user=user,coupon=coupen_check).exists():
                return JsonResponse({'error':'Coupon already applied.'})
            else:
                if coupen_check.used_count < coupen_check.usage_limit:

                    cart_total = sum(Cart.objects.filter(user=user).values_list('cart_price',flat=True))

                    if cart_total >= coupen_check.minimum_purchase:
                        print(coupen_check.expiration_date)
                        print(datetime.now().date())
                        if coupen_check.expiration_date < datetime.now().date():
                            return JsonResponse({'error': f'Coupon Expired'})

                        
                        total = cart_total - coupen_check.discount_value 

                        response_data = {'success': 'added', 'total': total, 'coupon_code': coupon_code ,'discount_amount' : coupen_check.discount_value }
                        
                        coupen_check.used_count += 1
                        coupen_check.save()

                        CouponUsage.objects.create(user=user,coupon=coupen_check)

                        return JsonResponse(response_data)
                    else:
                        return JsonResponse({'error': f'Minimum purchase amount of {round(coupen_check.minimum_purchase)} required'})


                else:
                    return JsonResponse({'error':'Sorry! This code has reached its usage limit.'})
                
        else:   
            return JsonResponse({'error': 'invalid coupon'})

    return JsonResponse({'error': 'Invalid request'})

    # views.py

def remove_coupon(request):
    email = request.session.get("email")
    user = CustomUser.objects.get(email=email)

    coupon_code = request.POST.get('couponCode', '')
    coupen_check = Coupons.objects.filter(code=coupon_code,is_active=True).first()
    print(1)
    if coupen_check:
        print(2)
        usage_check = CouponUsage.objects.filter(user=user,coupon=coupen_check).first()
        if usage_check:
            print(3)
            coupen_check.used_count -= 1
            coupen_check.save()
            usage_check.delete()

    print(4)
    # Update the cart total
    total = sum(Cart.objects.filter(user=user).values_list('cart_price', flat=True))

    response_data = {'success': 'removed', 'total': total}
    return JsonResponse(response_data)

