from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate
from userlogin.models import CustomUser
from wallet.models import Wallet
import random
import string
from datetime import datetime,timezone,timedelta
from django.core.mail import send_mail
import uuid
import os

# Create your views here.


# Create user
def signup(request):
    if request.method == 'POST':
        fullname = request.POST['fullname']
        phone = request.POST['phone']
        email = request.POST['email']
        password = request.POST['password']
        referred_code = request.POST['referred_code']

        is_referred = False
        is_valid = 1

        if CustomUser.objects.filter(phone=phone).exists():
            is_valid = 0
            messages.warning(request, 'Phone number is taken')
            
        if CustomUser.objects.filter(email=email).exists():
            is_valid = 0
            messages.error(request, 'Email is taken')

        if referred_code:
            if not CustomUser.objects.filter(referral_code=referred_code).exists():
                is_valid = 0
                messages.info(request, 'Referral code is not valid')
            else:
                is_referred = True


        if is_valid==0:
            return redirect('signup')

        else:
            otp_sent = str(random.randint(100000,999999))
            otp_expiry =  datetime.now() + timedelta(seconds=60)
            print(otp_expiry)

            characters = string.digits + string.ascii_uppercase
            referral_code = ''.join(random.choice(characters) for i in range(6))

            user = CustomUser.objects.create_user(username=email, phone=phone, email=email, password=password,fullname=fullname,referral_code=referral_code,is_active=False, otp=otp_sent,otp_expiry=otp_expiry)
            
            if is_referred:
                balance = 100
                amount = 100
                Wallet.objects.create(
                    user=user,
                    amount=amount,
                    balance=balance,
                    transaction_type = "Credit",
                    transaction_details = f"Recieved Login bonus through Referral"
                )

                referred_user = CustomUser.objects.filter(referral_code=referred_code).first()

                reffered_user_wallet = Wallet.objects.filter(user=referred_user).order_by('-id').first()

                if not reffered_user_wallet:
                    reffered_user_balance = 0
                else:
                    reffered_user_balance = reffered_user_wallet.balance
                
                new_balance = reffered_user_balance + amount

                Wallet.objects.create(
                    user=referred_user,
                    amount=amount,
                    balance=new_balance,
                    transaction_type = "Credit",
                    transaction_details = f"Recieved Refferal Bonus by Inviting Friend"
                )

            
            request.session['email'] = email
            request.session['user_id'] = user.id
            return redirect('otp')


    return render(request,'userlogin/signup.html')


# Authenticate User
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


# check OTP
def otp(request):
    user = CustomUser.objects.get(id=request.session['user_id'])
    otp_expiry = user.otp_expiry
    if request.method == 'POST':
        otp_expiry = user.otp_expiry
        entered_otp = request.POST['otp']
        if entered_otp != user.otp:
            messages.error(request, 'Invalid otp')
            return redirect('otp')
        elif (datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)) > user.otp_expiry :
            print(datetime.now(timezone.utc) + timedelta(hours=5, minutes=30))
            print(user.otp_expiry)
            messages.error(request, 'Otp Expired! Please Click Resend OTP')
            return redirect('otp')
        else :
            user.is_active = True
            user.save()
            return redirect('signin')
            
    return render(request,'userlogin/otp.html',{'otp_expiry': otp_expiry})


def landing(request):
    return render(request, 'userlogin/homepage.html')


# resend otp 
def send_otp(request):
    user = CustomUser.objects.get(id=request.session['user_id'])
    user.otp = str(random.randint(100000,999999))
    otp_expiry =  datetime.now() + timedelta(seconds=65)
    user.otp_expiry = otp_expiry
    user.save()
    return redirect('otp')

def send_forget_password_mail(email, token):
    subject = "Your forget Password Link"
    message = f'Hi, click on hte link to reset your password \n Link : http://127.0.0.1:8000/user/reset_password/{token}/'
    email_from = os.environ.get('SENDER_EMAIL')
    recipient_list = [email]
    send_mail(subject,message,email_from,recipient_list)
    return True

def forget_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if CustomUser.objects.filter(email=email).exists():
            token = str(uuid.uuid4())
            user = CustomUser.objects.filter(email=email).first()
            user.forget_password_token = token
            user.save()
            send_forget_password_mail(email, token)
            messages.success(request, "Email send !! \n Please verify your email")
            return redirect('forget_password')

        else:
            messages.error(request, 'Invalid Email')
            return redirect('forget_password')
    return render(request, 'userlogin/forget.html')




def reset_password(request, token):
    user = CustomUser.objects.get(forget_password_token=token)
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_pass = request.POST.get('confirm-password')
        user.set_password(password)
        user.save()
        return redirect('signin')
    return render(request, 'userlogin/reset.html')


