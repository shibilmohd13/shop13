from msilib.schema import CustomAction
import re
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
        email = request.POST['email']
        password = request.POST['password']

        if CustomUser.objects.filter(phone=phone).exists():
            messages.error(request, 'Phone number is taken')
            return redirect('signup')
        elif CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email is taken')
            return redirect('signup')
        else:
            request.session['fullname'] = fullname
            request.session['phone'] = phone
            request.session['email'] = email
            request.session['password'] = password
            return redirect('send_otp')


    return render(request,'userlogin/signup.html')

def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            print(user.fullname)
            request.session['fullname'] = user.fullname
            return redirect('home')
        else:
            return redirect('signin')
    return render(request,'userlogin/index.html')

def otp(request):
    if request.method == 'POST':
        entered_otp = request.POST['otp']
        if entered_otp == request.session['otp']:
            user = CustomUser.objects.create_user(username=request.session['email'], phone=request.session['phone'], email=request.session['email'], password=request.session['password'],fullname=request.session['fullname'])
            user.save()
            return redirect('home')
        else:
            messages.error(request, 'Invalid otp')
            return redirect('otp')
    return render(request,'userlogin/otp.html')

def landing(request):
    return render(request, 'userlogin/homepage.html')

def send_otp(request):
    otp_sent = random.randint(100000,999999)
    request.session['otp'] = str(otp_sent)
    print(otp_sent)
    sender_email = "shop13ecommerce@gmail.com"
    sender_pass = 'vqor ejqp zexj omko'
    connection = smtplib.SMTP('smtp.gmail.com', 587)
    connection.starttls()
    connection.login(user=sender_email, password=sender_pass)
    connection.sendmail(from_addr=sender_email, to_addrs=request.session['email'],msg=f'Subject: OTP for register \n\n Here is your OTP for create account in SHOP13\n OTP:- {otp_sent}')
    connection.close()
    return redirect('otp')


