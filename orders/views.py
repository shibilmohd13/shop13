from multiprocessing import reduction
from django.shortcuts import render
import uuid
from userlogin.models import CustomUser
from orders.models import *

# Create your views here.

def orders(request):
    if 'email' in request.session:
        email = request.session['email']
        user = CustomUser.objects.get(email=email)
        orders = Orders.objects.filter(user=user)
        order_items = OrdersItem.objects.filter(order__in=orders)

    return render(request, "home/orders.html", {'order_items': order_items})

def view_orders(request):
    order_id = uuid.UUID(request.session['order_id'])
    current_order = Orders.objects.get(order_id=order_id)
    context= {
        "current_order" : current_order
    }
    return render(request, 'home/view_order.html', context)