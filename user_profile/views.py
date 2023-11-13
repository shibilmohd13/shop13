from django.shortcuts import render, redirect
from userlogin.models import *
from django.contrib import messages
from django.contrib.auth import authenticate

# Create your views here.


# View for user profile
def profile(request):
    email = request.session['email']
    user = CustomUser.objects.get(email=email)
    user_data = Address.objects.filter(user=user,is_present=True)
    return render(request, 'user_profile/profile.html',{'user_data' : user_data})


# Update profile details
import re

def update_profile(request):
    if request.method == 'POST':
        email = request.session['email']
        user = CustomUser.objects.get(email=email)
        
        # Validate Full Name
        new_fullname = request.POST.get('fullname')
        if not re.match(r'^[a-zA-Z]{3,}(?: [a-zA-Z]+)*$', new_fullname):
            messages.error(request, "Invalid full name.")
            return redirect('profile')

        # Validate Phone Number
        new_phone = request.POST.get('phone')
        if not re.match(r'^\+91[1-9]\d{9}$', new_phone):
            messages.error(request, "Invalid phone number. Please enter a valid Indian phone number.")
            return redirect('profile')

        # Check if phone number already exists
        if CustomUser.objects.exclude(id=user.id).filter(phone=new_phone).exists():
            messages.error(request, "Phone number already exists in the database.")
            return redirect('profile')
        
        user.fullname = new_fullname
        user.phone = new_phone
        user.save()
        
        messages.success(request, "Updated successfully")

    return redirect('profile')


# change the password
def change_password(request):
    if request.method == 'POST':
        email = request.session['email']
        user = CustomUser.objects.get(email=email)

        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        new_password_confirm = request.POST.get('password_confirm')
        
        new_user = authenticate(username=email, password=current_password)
        
        if user == new_user:
            if new_password == new_password_confirm:
                user.set_password(new_password)
                user.save()
                print('Profile changed') 
                return redirect('profile')
            else:
                messages.error(request, "Passwords does not match")
                return redirect('profile')
        else:
            messages.error(request, "Current Password is not Correct")
            return redirect('profile')


# Add address from the User profile
def add_address(request):
    email = request.session['email']
    user = CustomUser.objects.get(email=email)
    name = request.POST['name']
    phone = request.POST['phone']
    street_address = request.POST['street_address']
    city = request.POST['city']
    state = request.POST['state']
    pincode = request.POST['pincode']

    new_address = Address(
        user = user,
        name = name,
        phone = phone,
        street_address = street_address,
        city = city,
        state = state,
        pin_code = pincode
    )
    new_address.save()
                
    return redirect('profile')


# Edit address from the user Profile
def edit_address(request, id):
    address = Address.objects.get(id=id)

    name = request.POST.get('name')
    phone = request.POST.get('phone')
    street_address = request.POST.get('street_address')
    city = request.POST.get('city')
    state = request.POST.get('state')
    pincode = request.POST.get('pincode')

    address.name = name
    address.phone = phone
    address.street_address = street_address
    address.city = city
    address.state = state
    address.pin_code = pincode

    address.save()

    return redirect('profile')

def delete_address(request, id):
    address = Address.objects.get(id=id)
    address.is_present = False
    address.save()
    return redirect('profile')