from django.shortcuts import render,redirect
from .models import *

# Create your views here.

def products(request):
    prod = Product.objects.all().order_by('id')
    context = {
        'products' : prod
    }
    return render(request, 'admin_panel/products.html', context)

def product_status(request, id):
    prod = Product.objects.filter(id=id).first()
    if prod.is_listed == True:
        prod.is_listed = False
        prod.save()
    else:
        prod.is_listed = True
        prod.save()
    return redirect('products')

def add_products(request):
    # if request.method == 'POST':
    #     prod = Product()
    #     prod.name = request.POST.get('name')
    #     prod.description = request.POST.get('description')
    #     prod.price = request.POST.get('price')
    #     prod.discount = request.POST.get('discount')
    #     prod.quantity = request.POST.get('quantity')
    #     prod.category = request.POST.get('category')
    #     prod.brands = request.POST.get('brand')
    #     prod.color = request.POST.get('color')

    #     if len(request.FILES) != 0 :
    #         prod.image1 = request.FILES['image1']

    #     if len(request.FILES) != 0 :
    #         prod.image2 = request.FILES['image2']
        
    #     if len(request.FILES) != 0 :
    #         prod.image3 = request.FILES['image3']

    #     prod.save()
    #     return redirect('add_products')

    return render(request, 'admin_panel/add_products.html')

def add_categories(request):
    if request.method == "POST":
        name = request.POST.get('name')
        cat = Category(name=name,is_listed=True)
        cat.save()
        return redirect("categories")
    return render(request, 'admin_panel/add_categories.html')

def add_brands(request):
    if request.method == "POST":
        name = request.POST.get('name')
        brand = Brand(name=name,is_listed=True)
        brand.save()
        return redirect("brands")
    return render(request, 'admin_panel/add_brands.html')

def add_colors(request):
    if request.method == "POST":
        name = request.POST.get('name')
        clr = Color(name=name,is_listed=True)
        clr.save()
        return redirect("colors")
    return render(request, 'admin_panel/add_colors.html')


def edit_categories(request, id):
    cat = Category.objects.get(id=id)
    if request.method == 'POST':
        cat.name = request.POST.get('name')
        cat.save()
        return redirect('categories')
    return render(request, 'admin_panel/edit_categories.html',{'cat':cat})

def edit_brands(request,id):
    brand = Brand.objects.get(id=id)
    if request.method == 'POST':
        brand.name = request.POST.get('name')
        brand.save()
        return redirect('brands')
    return render(request, 'admin_panel/edit_brands.html',{'brand': brand})

def edit_colors(request, id):
    clr = Color.objects.get(id=id)
    if request.method == 'POST':
        clr.name = request.POST.get('name')
        clr.save()
        return redirect('colors')
    return render(request, 'admin_panel/edit_colors.html',{'clr':clr})

def categories(request):
    cat = Category.objects.all().order_by('id')
    context = {
        'categories' : cat
    }
    return render(request, 'admin_panel/categories.html', context)

def category_status(request, id):
    cat = Category.objects.filter(id=id).first()
    if cat.is_listed == True:
        cat.is_listed = False
        cat.save()
    else:
        cat.is_listed = True
        cat.save()
    return redirect('categories')


def brands(request):
    brand = Brand.objects.all().order_by('id')
    context = {
        'brands' : brand
    }
    return render(request, 'admin_panel/brands.html', context)

def brand_status(request, id):
    brand = Brand.objects.filter(id=id).first()
    if brand.is_listed == True:
        brand.is_listed = False
        brand.save()
    else:
        brand.is_listed = True
        brand.save()
    return redirect('brands')



def colors(request):
    color = Color.objects.all().order_by('id')
    context = {
        'colors' : color
    }
    return render(request, 'admin_panel/colors.html', context)

def color_status(request, id):
    color = Color.objects.filter(id=id).first()
    if color.is_listed == True:
        color.is_listed = False
        color.save()
    else:
        color.is_listed = True
        color.save()
    return redirect('colors')
