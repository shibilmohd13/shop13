from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from userlogin.models import CustomUser
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.cache import cache_control
from orders.models import *

# Create your views here.


# Admin Login view
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_login(request):
    if request.method == 'POST':
        email = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            if user.is_superuser:
                login(request, user)
                return redirect('admin_dash')
            else:
                messages.error(request, "User has No access to Admin panel")
                return redirect('admin_login')
        else:
            messages.error(request, "Invalid user")
            return redirect('admin_login')
    return render(request, 'admin_panel/admin_login.html')


# Dashboard with Sales report
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u:u.is_superuser, login_url='admin_login')
def admin_dash(request):
    return render(request, 'admin_panel/admin_dash.html')


# List Users
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u:u.is_superuser, login_url='admin_login')
def users(request):
    users = CustomUser.objects.all().exclude(is_superuser=True).order_by('id')
    context = { 'users' : users }
    return render(request, 'admin_panel/users.html', context)


# Change User status Block / Unbloak
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u:u.is_superuser, login_url='admin_login')
def user_status(request, id):
    user = CustomUser.objects.filter(id=id).first()
    if user.is_active == True:
        user.is_active = False
        user.save()
    else:
        user.is_active = True
        user.save()
    return redirect('users')


# Admin Logout
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u:u.is_superuser, login_url='admin_login')
def admin_logout(request):
    request.session.flush()
    return redirect('admin_login')


# List Orders
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='admin_login')
def orders(request):
    order_items = OrdersItem.objects.all().order_by("order_id")
    return render(request, 'admin_panel/orders.html' , {'items' : order_items})


# Detiled view of each Order
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='admin_login')
def view_order_details(request, id):
    obj = OrdersItem.objects.get(id=id)
    print(obj)
    return render(request,'admin_panel/order_details.html',{'obj':obj})



# Change order status
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='admin_login')
def change_order_status(request, id):
    order = OrdersItem.objects.get(id=id)
    status = request.POST.get('btnradio')
    if status == "Cancelled":
        order.status = status
        order.variant.quantity += order.quantity
        order.save()
        order.variant.save() 
    else:
        order.status = status
        order.save()
    return redirect('view_order_details',id=id)
