from email import message
from django.shortcuts import render,redirect
from .models import *
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.cache import cache_control
from django.contrib import messages


# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u:u.is_superuser, login_url='admin_login')
def products(request):
    prod = Product.objects.exclude(is_listed=False).order_by('id')
    context = {
        'products' : prod
    }
    return render(request, 'admin_panel/products.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u:u.is_superuser, login_url='admin_login')
def unlisted_products(request):
    prod = Product.objects.exclude(is_listed=True).order_by('id')
    context = {
        'products' : prod
    }
    return render(request, 'admin_panel/unlisted_products.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u:u.is_superuser, login_url='admin_login')
def product_status(request, id):
    prod = Product.objects.filter(id=id).first()
    if prod.is_listed == True:
        prod.is_listed = False
        prod.save()
    else:
        prod.is_listed = True
        prod.save()
    return redirect('products')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u:u.is_superuser, login_url='admin_login')
def product_status_unlist(request, id):
    prod = Product.objects.filter(id=id).first()
    if prod.is_listed == True:
        prod.is_listed = False
        prod.save()
    else:
        prod.is_listed = True
        prod.save()
    return redirect('unlisted_products')
    

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u:u.is_superuser, login_url='admin_login')
def add_products(request):
    category_list = Category.objects.all()
    brands_list = Brand.objects.all()
    color_list = Color.objects.all()
    context = {
        'cat' : category_list,
        'bnd' : brands_list,
        'clr' : color_list
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        discount = request.POST.get('discount')
        quantity = request.POST.get('quantity')
        category_id = request.POST.get('category')
        brand_id = request.POST.get('brand')
        color_id = request.POST.get('color')
        image1 = request.FILES.get('image1')
        image2 = request.FILES.get('image2')
        image3 = request.FILES.get('image3')


        category = Category.objects.get(id=category_id)
        brand = Brand.objects.get(id=brand_id)
        color = Color.objects.get(id=color_id)

        product = Product(
            name=name,
            description=description,
            price=price,
            discount=discount,
            quantity=quantity,
            category=category,
            brands=brand,
            color=color,
            # image1=image1,
            # image2=image2,
            # image3=image3,
        )
        product.save()

        # Function to save an uploaded image to the 'media' directory
        def save_image(image, filename):
            path = default_storage.save(filename, ContentFile(image.read()))
            return path

        # Save the uploaded images
        if image1:
            product.image1 = save_image(image1,f'{image1.name}')
        if image2:
            product.image2 = save_image(image2,f'{image2.name}')
        if image3:
            product.image3 = save_image(image3,f'{image3.name}')

        product.save()

        return redirect('products')

    return render(request, 'admin_panel/add_products.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u:u.is_superuser, login_url='admin_login')
def edit_products(request, id):
    category_list = Category.objects.all()
    brands_list = Brand.objects.all()
    color_list = Color.objects.all()
    prod = Product.objects.get(id=id)
    context = {
        'cat' : category_list,
        'bnd' : brands_list,
        'clr' : color_list,
        'prod' : prod
    }
    if request.method == 'POST':
        prod.name = request.POST.get('name')
        prod.description = request.POST.get('description')
        prod.price = request.POST.get('price')
        prod.discount = request.POST.get('discount')
        prod.quantity = request.POST.get('quantity')
        prod.category_id = request.POST.get('category')
        prod.brand_id = request.POST.get('brand')
        prod.color_id = request.POST.get('color')
        prod.save()

        image1 = request.FILES.get('image1')
        image2 = request.FILES.get('image2')
        image3 = request.FILES.get('image3')

        # Function to save an uploaded image to the 'media' directory
        def save_image(image, filename):
            path = default_storage.save(filename, ContentFile(image.read()))
            return path

        # Save the uploaded images
        if image1:
            prod.image1 = save_image(image1,f'{image1.name}')
        if image2:
            prod.image2 = save_image(image2,f'{image2.name}')
        if image3:
            prod.image3 = save_image(image3,f'{image3.name}')

        prod.save()
        return redirect('products')
    return render(request, 'admin_panel/edit_products.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u:u.is_superuser, login_url='admin_login')
def add_categories(request):
    if request.method == "POST":
        name = request.POST.get('name')
        if Category.objects.filter(name=name).exists():
            messages.error(request, "This Category already exists")
            return redirect('add_categories')
        cat = Category(name=name,is_listed=True)
        cat.save()
        return redirect("categories")
    return render(request, 'admin_panel/add_categories.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u:u.is_superuser, login_url='admin_login')
def add_brands(request):
    if request.method == "POST":
        name = request.POST.get('name')
        if Brand.objects.filter(name=name).exists():
            messages.error(request, "This Brand already exists")
            return redirect('add_brands')
        brand = Brand(name=name,is_listed=True)
        brand.save()
        return redirect("brands")
    return render(request, 'admin_panel/add_brands.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u:u.is_superuser, login_url='admin_login')
def add_colors(request):
    if request.method == "POST":
        name = request.POST.get('name')
        if Color.objects.filter(name=name).exists():
            messages.error(request, "This Color already exists")
            return redirect('add_colors')
        clr = Color(name=name,is_listed=True)
        clr.save()
        return redirect("colors")
    return render(request, 'admin_panel/add_colors.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u:u.is_superuser, login_url='admin_login')
def edit_categories(request, id):
    cat = Category.objects.get(id=id)
    if request.method == 'POST':
        cat.name = request.POST.get('name')
        cat.save()
        return redirect('categories')
    return render(request, 'admin_panel/edit_categories.html',{'cat':cat})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u:u.is_superuser, login_url='admin_login')
def edit_brands(request,id):
    brand = Brand.objects.get(id=id)
    if request.method == 'POST':
        brand.name = request.POST.get('name')
        brand.save()
        return redirect('brands')
    return render(request, 'admin_panel/edit_brands.html',{'brand': brand})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u:u.is_superuser, login_url='admin_login')
def edit_colors(request, id):
    clr = Color.objects.get(id=id)
    if request.method == 'POST':
        clr.name = request.POST.get('name')
        clr.save()
        return redirect('colors')
    return render(request, 'admin_panel/edit_colors.html',{'clr':clr})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u:u.is_superuser, login_url='admin_login')
def categories(request):
    cat = Category.objects.all().order_by('id')
    context = {
        'categories' : cat
    }
    return render(request, 'admin_panel/categories.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u:u.is_superuser, login_url='admin_login')
def category_status(request, id):
    cat = Category.objects.filter(id=id).first()
    if cat.is_listed == True:
        cat.is_listed = False
        cat.save()
    else:
        cat.is_listed = True
        cat.save()
    return redirect('categories')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u:u.is_superuser, login_url='admin_login')
def brands(request):
    brand = Brand.objects.all().order_by('id')
    context = {
        'brands' : brand
    }
    return render(request, 'admin_panel/brands.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u:u.is_superuser, login_url='admin_login')
def brand_status(request, id):
    brand = Brand.objects.filter(id=id).first()
    if brand.is_listed == True:
        brand.is_listed = False
        brand.save()
    else:
        brand.is_listed = True
        brand.save()
    return redirect('brands')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u:u.is_superuser, login_url='admin_login')
def colors(request):
    color = Color.objects.all().order_by('id')
    context = {
        'colors' : color
    }
    return render(request, 'admin_panel/colors.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u:u.is_superuser, login_url='admin_login')
def color_status(request, id):
    color = Color.objects.filter(id=id).first()
    if color.is_listed == True:
        color.is_listed = False
        color.save()
    else:
        color.is_listed = True
        color.save()
    return redirect('colors')
