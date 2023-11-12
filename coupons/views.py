from django.shortcuts import render,redirect
from .models import Coupons
# Create your views here.
def coupons(request):
    coupons = Coupons.objects.all().order_by("id")
    context={'coupons':coupons}
    return render(request,'admin_panel/coupons.html', context)

def add_coupons(request):
    if request.method == "POST":
        name=request.POST['name']
        code=request.POST['code']
        type=request.POST['type']
        discount=request.POST['discount_value']
        min_purchase=request.POST.get('min_purchase',0)
        expiry_date=request.POST['expiry_date']
        usage_limit = request.POST['usage_limit']

        Coupons.objects.create(
            name=name,
            code=code,
            discount_type=type,
            discount_value=discount,
            minimum_purchase=min_purchase,
            expiration_date=expiry_date,
            usage_limit=usage_limit,
        )
        return redirect('coupons')
        
    return render(request,'admin_panel/add_coupons.html')

def edit_coupons(request,id):
    coupon = Coupons.objects.filter(id=id).first()
    if request.method=='POST':
        name=request.POST['name']
        code=request.POST['code']
        type=request.POST['type']
        discount=request.POST['discount_value']
        min_purchase=request.POST.get('min_purchase',0)
        expiry_date=request.POST['expiry_date']
        usage_limit = request.POST['usage_limit']

        coupon.name=name
        coupon.code=code
        coupon.discount_type=type
        coupon.discount_value=discount
        coupon.minimum_purchase=min_purchase
        coupon.expiration_date=expiry_date
        coupon.usage_limit=usage_limit
        coupon.save()
        return redirect('coupons')

    return render(request, 'admin_panel/edit_coupons.html', {'coupon' : coupon})

def coupon_status(request, id):
    coupon = Coupons.objects.filter(id=id).first()
    if coupon.is_active == True:
        coupon.is_active = False
        coupon.save()
    else:
        coupon.is_active = True
        coupon.save()
    return redirect('coupons')
