from django.shortcuts import render,redirect
import uuid
from userlogin.models import CustomUser
from orders.models import *
from wallet.models import Wallet

# Create your views here.


# View for listing order history of the User
def orders(request):
    if 'email' in request.session:
        email = request.session['email']
        user = CustomUser.objects.get(email=email)
        orders = Orders.objects.filter(user=user)
        order_items = OrdersItem.objects.filter(order__in=orders).order_by('-id')
    return render(request, "home/orders.html", {'order_items': order_items})


# View for providing the Order Confirmed page After placing a Order
def view_orders(request):
    order_id = request.session['order_id']
    current_order = Orders.objects.get(order_id=order_id)
    context= {
        "current_order" : current_order
    }
    return render(request, 'home/order_success.html', context)


def view_invoice(request):
    order_id = request.session['order_id']
    current_order = Orders.objects.get(order_id=order_id)
    context= {
        "current_order" : current_order
    }
    return render(request, 'home/invoice.html',context)


def cancel_order(request, id):
    email = request.session['email']
    user = CustomUser.objects.get(email=email)
    order = OrdersItem.objects.get(id=id)
    order.status = "Cancelled"

    if order.order.payment_method == "COD":
        order.variant.quantity += order.quantity
        order.save()
        order.variant.save()
    else:
        order.variant.quantity += order.quantity
    
        amount = order.price * order.quantity

        user_wallet = Wallet.objects.filter(user=user).order_by('-id').first()

        if not user_wallet:
            balance = 0
        else:
            balance = user_wallet.balance
        
        new_balance = balance+amount
        Wallet.objects.create(
            user=user,
            amount=amount,
            balance=new_balance,
            transaction_type = "Credit",
            transaction_details = f"Recieved Money through Order Cancel"
        )
        order.save()
        order.variant.save()
    return redirect('orders')

def return_order(request, id):
    email = request.session['email']
    user = CustomUser.objects.get(email=email)

    order = OrdersItem.objects.get(id=id)
    order.status = "Returned"
    order.variant.quantity += order.quantity
    
    amount = order.price * order.quantity

    user_wallet = Wallet.objects.filter(user=user).order_by('-id').first()

    if not user_wallet:
        balance = 0
    else:
        balance = user_wallet.balance
    
    new_balance = balance+amount
    Wallet.objects.create(
        user=user,
        amount=amount,
        balance=new_balance,
        transaction_type = "Credit",
        transaction_details = f"Recieved Money through Refund"
    )

    order.save()
    order.variant.save()
    
    return redirect("orders")