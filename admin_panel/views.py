from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login
from userlogin.models import CustomUser
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.cache import cache_control
from orders.models import *
from wallet.models import Wallet
from admin_panel.models import Banners

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
    order_items = OrdersItem.objects.all().order_by("-id")
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
    if status == "Cancelled" or status == "Returned":
        if order.order.payment_method != "COD":
            order.status = status
            order.variant.quantity += order.quantity

            wallet = Wallet.objects.filter(user=order.order.user).order_by("-id")

            if wallet:
                balance = wallet.first().balance
            else: 
                balance = 0

            new_balance = balance + order.total_price()

            Wallet.objects.create(
                user=order.order.user,
                amount=order.total_price(),
                balance=new_balance,
                transaction_type = "Credit",
                transaction_details = f"Recieved money through Order {status} By Seller"
            )
        order.status = status
        order.variant.quantity += order.quantity
        order.save()
        order.variant.save()
        return redirect('view_order_details',id=id)

    else:
        order.status = status
        order.save()
    return redirect('view_order_details',id=id)


# Display Product/Category offers in admin side
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u:u.is_superuser, login_url='admin_login')
def offers(request):
    return render(request, 'admin_panel/offers.html')


# Display all Product offers in admin side
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u:u.is_superuser, login_url='admin_login')
def product_offers(request):
    products = ColorVarient.objects.filter(product_offer__gt=0)
    return render(request, 'admin_panel/offers_product.html',{'products':products})


# Add product offers in admin side
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u:u.is_superuser, login_url='admin_login')
def add_product_offers(request):

    products = ColorVarient.objects.all().order_by('id')

    if request.method == 'POST':

        product = request.POST.get('product')
        product_discount = request.POST.get('discount')

        variant = ColorVarient.objects.get(id=product)
        variant.product_offer = product_discount
        variant.save()
        return redirect('product_offers')

    return render(request, 'admin_panel/add_offers_product.html',{'products':products})


# Edit product offers
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u:u.is_superuser, login_url='admin_login')
def edit_product_offers(request, id):
    products = ColorVarient.objects.all().order_by('id')
    item = ColorVarient.objects.get(id=id)
    if request.method == 'POST':
        product_discount = request.POST.get('discount')

        item.product_offer = product_discount
        item.save()
        return redirect('product_offers')

    return render(request, 'admin_panel/edit_offers_product.html',{'item':item,'products':products})


# Cancel Product offers
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u:u.is_superuser, login_url='admin_login')
def cancel_product_offers(request,id):
    item = ColorVarient.objects.get(id=id)
    item.product_offer = 0
    item.save()
    return redirect('product_offers')


# Display all Category offers
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u:u.is_superuser, login_url='admin_login')
def category_offers(request):
    category = Category.objects.all()
    return render(request, 'admin_panel/offers_category.html',{'category':category})


# Add category offer
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u:u.is_superuser, login_url='admin_login')
def add_category_offers(request,id):

    category = Category.objects.get(id=id)

    if request.method == 'POST':

        category_offer_value = request.POST.get('category_offer', 0)
        print(category_offer_value)
        color_varients = ColorVarient.objects.filter(product__category=category)
        color_varients.update(category_offer=category_offer_value)
        print(color_varients.values())

        return redirect('category_offers')  
    return render(request, 'admin_panel/add_offers_category.html',{'category':category})


# Cancel catetory Offers
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u:u.is_superuser, login_url='admin_login')
def cancel_category_offers(request,id):

    category = Category.objects.get(id=id)
    color_varients = ColorVarient.objects.filter(product__category=category)
    color_varients.update(category_offer=0)

    return redirect('category_offers')


# Display Banners
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u:u.is_superuser, login_url='admin_login')
def banners(request):
    banners = Banners.objects.all().order_by("id")
    return render(request, 'admin_panel/banners.html',{'banners' : banners})


# Add Banners
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u:u.is_superuser, login_url='admin_login')
def add_banners(request):
    products = ColorVarient.objects.filter(is_listed=True).order_by("id")
    if request.method == 'POST':
        subtitle = request.POST.get('subtitle')
        title = request.POST.get('title')
        description = request.POST.get('description')
        product = request.POST.get('product')
        image = request.FILES.get('image')
        variant = get_object_or_404(ColorVarient, pk = product)
        print(product)

        Banners.objects.create(
            subtitle=subtitle,
            title=title,
            description=description,
            variant=variant,
            image=image
        )
        return redirect('banners')
    return render(request, 'admin_panel/add_banners.html',{'products' : products})


# Edit banners
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u:u.is_superuser, login_url='admin_login')
def edit_banners(request, id):
    banner = get_object_or_404(Banners, pk=id)
    products = ColorVarient.objects.filter(is_listed=True).order_by("id")

    if request.method == 'POST':
        subtitle = request.POST.get('subtitle')
        title = request.POST.get('title')
        description = request.POST.get('description')
        product = request.POST.get('product')
        image = request.FILES.get('image')
        variant = get_object_or_404(ColorVarient, pk=product)

        # Update the fields of the existing banner
        banner.subtitle = subtitle
        banner.title = title
        banner.description = description
        banner.variant = variant

        if image:
            banner.image = image

        banner.save()

        return redirect('banners')

    return render(request, 'admin_panel/edit_banners.html', {'banner': banner, 'products': products})


# Change status of a banner
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u:u.is_superuser, login_url='admin_login')
def status_banner(request, id):
    banner = Banners.objects.filter(id=id).first()

    if banner.is_listed == True:
        banner.is_listed = False
        banner.save()

    else:
        banner.is_listed = True
        banner.save()

    return redirect("banners")