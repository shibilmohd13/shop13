from msilib.schema import CustomAction
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
        username = request.POST['username']
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
            request.session['username'] = username
            request.session['phone'] = phone
            request.session['email'] = email
            request.session['password'] = password
            messages.success(request, 'User created successfully')
            return redirect('otp')


    return render(request,'signup.html')

def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        print(email)
        print(password)
        user = authenticate(request, username=email, password=password)
        print(user)
        if user is not None:
            return redirect('landing')
        else:
            return redirect('signin')
    return render(request,'index.html')

def otp(request):
    if request.method == 'POST':
        entered_otp = request.POST['otp']
        if entered_otp == request.session['otp']:
            CustomUser.objects.create(username=request.session['username'], phone=request.session['phone'], email=request.session['email'], password=request.session['password'])
            return redirect('signin')
        else:
            return redirect('otp')

    otp_sent = random.randint(100000,999999)
    request.session['otp'] = str(otp_sent)
    print(otp_sent)
    sender_email = "shop13ecommerce@gmail.com"
    sender_pass = 'vqor ejqp zexj omko'
    connection = smtplib.SMTP('smtp.gmail.com', 587)
    connection.starttls()
    connection.login(user=sender_email, password=sender_pass)
    connection.sendmail(from_addr=sender_email, to_addrs='shibilmhdjr13@gmail.com',msg=f'Subject: OTP for register \n\n Here is your OTP for create account in SHOP13\n OTP:- {otp_sent}')
    connection.close()
    return render(request,'otp.html')

def landing(request):
    return render(request, 'homepage.html')

