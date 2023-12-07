from django.shortcuts import render, redirect
from products.models import *
from userlogin.models import CustomUser
from wishlist.models import Wishlist
from django.http import JsonResponse

# Create your views here.


# show wishlist
def wishlist(request):
    if "email" in request.session:
        email = request.session["email"]
        user = CustomUser.objects.get(email=email)
        wishlist = Wishlist.objects.filter(user=user).order_by("-id")
        return render(request, "home/wishlist.html", {"wishlist": wishlist})

    return redirect("signin")


# Remove wishlist
def remove_wishlist(request, id):
    item = Wishlist.objects.get(id=id)
    item.delete()
    return redirect("wishlist")


# Add to wishlist
def addtowishlist(request):
    if request.method == "POST":
        if "email" in request.session:
            email = request.session["email"]
            user = CustomUser.objects.get(email=email)
            prod_id = int(request.POST.get("product_id"))
            product_check = ColorVarient.objects.get(id=prod_id)
            if Wishlist.objects.filter(user=user, variant=product_check):
                return JsonResponse({"status": "Product already in Wishlist"})
            else:
                Wishlist.objects.create(user=user, variant=product_check)

                return JsonResponse(
                    {"status": "Product added successfully", "success": True}
                )
        else:
            return redirect("signin")

    return render(request, "home/details.html")
