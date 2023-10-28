from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.cache import cache_control
from django.contrib import messages


# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u:u.is_superuser, login_url='admin_login')
def products(request):
    # prod = Product.objects.exclude(is_listed=False).order_by('id')
    # prod = Product.objects.filter(is_listed=True).prefetch_related('productimage_set', 'colorvarient_set').first()
    prod = Product.objects.prefetch_related('colorvarient_set__productimage_set').filter(is_listed=True).order_by('id')
    # print(prod[0].colorvarient_set.first().productimage_set.first().image)

    context = {
        'products' : prod
    }
    return render(request, 'admin_panel/products.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u:u.is_superuser, login_url='admin_login')
def unlisted_products(request):
    prod = Product.objects.prefetch_related('colorvarient_set__productimage_set').filter(is_listed=False).order_by('id')
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
    context = {
        'cat' : category_list,
        'bnd' : brands_list,
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        discount = request.POST.get('discount')
        discounted_price = request.POST.get('discounted_price')
        category_id = request.POST.get('category')
        brand_id = request.POST.get('brand')

        category = Category.objects.get(id=category_id)
        brand = Brand.objects.get(id=brand_id)


        product = Product(
            name=name,
            description=description,
            price=price,
            discount=discount,
            discounted_price=discounted_price,
            category=category,
            brands=brand,
        )
        product.save()
        color_list = ['silver', 'gold', 'black' ,'brown']
        for color in color_list:  
            quantity = request.POST.get(color, 0)  # Use default value 0 if quantity is not provided
            print(quantity, name)
            varient = ColorVarient(product=product, color=color, quantity=quantity)
            varient.save()
            images = request.FILES.getlist(f'images_{color}')
            for image in images:
                ProductImage(varient=varient, image=image).save()

        return redirect('products')

    return render(request, 'admin_panel/add_products.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u:u.is_superuser, login_url='admin_login')
def edit_products(request, id):
    category_list = Category.objects.all()
    brands_list = Brand.objects.all()
    prod = Product.objects.get(id=id)
    colors = ColorVarient.objects.filter(product=prod)
    print(prod)
    context = {
        'cat' : category_list,
        'bnd' : brands_list,
        'prod' : prod,
        'colors' : colors
    }
    if request.method == 'POST':
        prod.name = request.POST.get('name')
        prod.description = request.POST.get('description')
        prod.price = request.POST.get('price')
        prod.discount = request.POST.get('discount')
        prod.discounted_price = request.POST.get('discounted_price')
        prod.category_id = request.POST.get('category')
        prod.brand_id = request.POST.get('brand')
        prod.save()


        color_list = ['silver', 'gold', 'black', 'brown']

        for color in color_list:
            quantity = request.POST.get(color, 0)  # Use default value 0 if quantity is not provided

            # Try to retrieve an existing ColorVariant instance
            try:
                varient = ColorVarient.objects.get(product=prod, color=color)
                varient.quantity = quantity  # Update the quantity
                varient.save()

            except ColorVarient.DoesNotExist:
                # If it doesn't exist, create a new ColorVariant
                varient = ColorVarient(product=prod, color=color, quantity=quantity)
                varient.save()

        # Second loop to handle images
        for color in color_list:
            new_images = request.FILES.getlist(f'images_{color}')

            if new_images:

                # Delete all existing images for this color variant
                varient = ColorVarient.objects.get(product=prod, color=color)
                varient.productimage_set.all().delete()
                
                # Save the new images
                for image in new_images:
                    ProductImage(varient=varient, image=image).save()


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


# function for showing the product variant, image on the product variant page 
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u:u.is_superuser, login_url='admin_login')
def varient_details(request, id):
    # product = Product.objects.filter(pk=id, is_listed=True).prefetch_related('productimage_set', 'colorvarient_set').first()
    # print(product)
    prod = Product.objects.filter(id=id).prefetch_related('colorvarient_set__productimage_set').first()
    return render(request, 'admin_panel/varient_details.html', { 'product' : prod })