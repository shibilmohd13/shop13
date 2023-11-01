from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate
from userlogin.models import CustomUser
import random
import smtplib

# Create your views here.
def signup(request):
    if request.method == 'POST':
        fullname = request.POST['fullname']
        phone = request.POST['phone']
        print(type(phone))
        email = request.POST['email']
        password = request.POST['password']

        is_valid = 1

        if CustomUser.objects.filter(phone=phone).exists():
            is_valid = 0
            messages.warning(request, 'Phone number is taken')
            
        if CustomUser.objects.filter(email=email).exists():
            is_valid = 0
            messages.error(request, 'Email is taken')

        if is_valid==0:
            return redirect('signup')

        else:
            otp_sent = str(random.randint(100000,999999))
            user = CustomUser.objects.create_user(username=email, phone=phone, email=email, password=password,fullname=fullname,is_active=False, otp=otp_sent)
            request.session['email'] = email
            request.session['user_id'] = user.id
            return redirect('otp')


    return render(request,'userlogin/signup.html')

def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            print(user.email)
            request.session['email'] = user.email
            return redirect('home')
        else:
            messages.error(request, "Invalid User")
            return redirect('signin')
    return render(request,'userlogin/index.html')

def otp(request):
    if request.method == 'POST':
        user = CustomUser.objects.get(id=request.session['user_id'])
        entered_otp = request.POST['otp']
        if entered_otp == user.otp:
            user.is_active = True
            user.save()
            return redirect('signin')
        else:
            messages.error(request, 'Invalid otp')
            return redirect('otp')
    return render(request,'userlogin/otp.html')

def landing(request):
    return render(request, 'userlogin/homepage.html')

def send_otp(request):
    user = CustomUser.objects.get(id=request.session['user_id'])
    user.otp = otp_sent = str(random.randint(100000,999999))
    user.save()
    return redirect('otp')


