from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.cache import cache_control
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.


# Showing the Listed products in the admin side
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u:u.is_superuser, login_url='admin_login')
def products(request):
    prod = Product.objects.prefetch_related('colorvarient_set__productimage_set').filter(is_listed=True).order_by('id')
    context = {
        'products' : prod
    }
    return render(request, 'admin_panel/products.html', context)


# showing Unlisted products
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u:u.is_superuser, login_url='admin_login')
def unlisted_products(request):
    prod = Product.objects.prefetch_related('colorvarient_set__productimage_set').filter(is_listed=False).order_by('id')
    context = {
        'products' : prod
    }
    return render(request, 'admin_panel/unlisted_products.html', context)


# Change status of the product ( Listed / Unlisted )
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


# Change status of the product in the Unlisted products page
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
    

# Add products
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='admin_login')
def add_products(request):
    category_list = Category.objects.all()
    brands_list = Brand.objects.all()
    context = {
        'cat': category_list,
        'bnd': brands_list,
    }

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        brand_id = request.POST.get('brand')

        # Check if a product with the same name exists (case-insensitive)
        try:
            existing_product = Product.objects.get(name__iexact=name)
            messages.error(request, "A product with the same name already exists.")
            return redirect('add_products')
        except ObjectDoesNotExist:
            pass

        category = Category.objects.get(id=category_id)
        brand = Brand.objects.get(id=brand_id)

        product = Product(
            name=name,
            description=description,
            category=category,
            brands=brand,
        )
        product.save()

        messages.success(request, "Product added successfully.")
        return redirect('products')

    return render(request, 'admin_panel/add_products.html', context)



# Edit Products
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
        prod.category_id = request.POST.get('category')
        prod.brands_id = request.POST.get('brand')
        prod.save()


        return redirect('products')
    return render(request, 'admin_panel/edit_products.html',context)


# Add Categories
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u:u.is_superuser, login_url='admin_login')
def add_categories(request):
    if request.method == "POST":
        name = request.POST.get('name')
        try:
            existing_product = Category.objects.get(name__iexact=name)
            messages.error(request, "A Category with the same name already exists.")
            return redirect('add_categories')
        except ObjectDoesNotExist:
            pass
        cat = Category(name=name,is_listed=True)
        cat.save()
        return redirect("categories")
    return render(request, 'admin_panel/add_categories.html')


# Add Brands
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u:u.is_superuser, login_url='admin_login')
def add_brands(request):
    if request.method == "POST":
        name = request.POST.get('name')
        try:
            existing_product = Brand.objects.get(name__iexact=name)
            messages.error(request, "A Brand with the same name already exists.")
            return redirect('add_brands')
        except ObjectDoesNotExist:
            pass
        brand = Brand(name=name,is_listed=True)
        brand.save()
        return redirect("brands")
    return render(request, 'admin_panel/add_brands.html')


# Edit categories
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='admin_login')
def edit_categories(request, id):
    cat = Category.objects.get(id=id)

    if request.method == 'POST':
        new_name = request.POST.get('name')

        # Check if the new name already exists
        if Category.objects.filter(name=new_name).exclude(id=cat.id).exists():
            messages.error(request, 'Category with this name already exists.')
        else:
            cat.name = new_name
            cat.save()
            return redirect('categories')

    return render(request, 'admin_panel/edit_categories.html', {'cat': cat})



# Edit Brands
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='admin_login')
def edit_brands(request, id):
    brand = Brand.objects.get(id=id)

    if request.method == 'POST':
        new_name = request.POST.get('name')

        # Check if the new name already exists
        if Brand.objects.filter(name=new_name).exclude(id=brand.id).exists():
            messages.error(request, 'Brand with this name already exists.')
        else:
            brand.name = new_name
            brand.save()
            return redirect('brands')

    return render(request, 'admin_panel/edit_brands.html', {'brand': brand})



# show all categories
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u:u.is_superuser, login_url='admin_login')
def categories(request):
    cat = Category.objects.all().order_by('id')
    context = {
        'categories' : cat
    }
    return render(request, 'admin_panel/categories.html', context)


# Category status change
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


# Show all Brands
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u:u.is_superuser, login_url='admin_login')
def brands(request):
    brand = Brand.objects.all().order_by('id')
    context = {
        'brands' : brand
    }
    return render(request, 'admin_panel/brands.html', context)


# change status of Brands
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

    prod = Product.objects.filter(id=id).prefetch_related('colorvarient_set__productimage_set').first()
    return render(request, 'admin_panel/varient_details.html', { 'product' : prod })


# Add varients for specific product
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u:u.is_superuser, login_url='admin_login')
def add_varients(request, id):

    product = Product.objects.get(id=id)

    if request.method == "POST":
        color = request.POST.get('color')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')
        variant = ColorVarient(
                product=product,
                color=color,
                quantity=quantity,
                price=price,
            )
        variant.save()
        # Handle image uploads
        for image in request.FILES.getlist('images'):
            ProductImage.objects.create(varient=variant, image=image)
        
        return redirect('varient_details', id=id)

    return render(request, 'admin_panel/add_varients.html', {"product" : product})



# Edit varients
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u:u.is_superuser, login_url='admin_login')
def edit_varients(request, id):
    
    varient = ColorVarient.objects.get(id=id)
    existing_images = ProductImage.objects.filter(varient=varient).order_by('-id')

    if request.method == 'POST':
        color = request.POST.get('color')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')

        # Update the variant with the new data
        varient.color = color
        varient.quantity = quantity
        varient.price = price

        varient.save()

        new_images = request.FILES.getlist('images')

        if new_images:

            ProductImage.objects.filter(varient=varient).delete()

            for image in new_images:
                ProductImage.objects.create(varient=varient, image=image)
        return redirect('varient_details', id=varient.product.id)

    return render(request, 'admin_panel/edit_varients.html', {'variant' : varient , 'product' : varient.product , 'images' : existing_images})


# Change varient Status
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u:u.is_superuser, login_url='admin_login')
def varient_status(request, id):
    varient = ColorVarient.objects.filter(id=id).first()
    prod_id = varient.product.id
    if varient.is_listed == True:
        varient.is_listed = False
        varient.save()
    else:
        varient.is_listed = True
        varient.save()
    return redirect('varient_details', id=prod_id)