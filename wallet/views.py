from django.shortcuts import render,redirect
from userlogin.models import CustomUser
from .models import Wallet
from django.http import JsonResponse
import razorpay
# Create your views here.

def wallet(request):
    email = request.session['email']
    user_name = CustomUser.objects.get(email=email)
    wallet = Wallet.objects.filter(user=user_name).order_by("-id")
    if wallet:
        balance= wallet.first().balance
    else: 
        balance=0

    return render(request, "home/wallet.html", {'wallet' : wallet, 'balance' : balance})

client = razorpay.Client(auth=("rzp_test_364uDI7fwiadCE", "ePLDxAKYVU5LybscC7YNuTqL"))

def add_to_wallet(request):
    amount = int(request.POST.get('amount')) * 100
    print(amount)
    data = { "amount": amount, "currency": "INR" }
    print(data)
    payment = client.order.create(data=data)
    request.session['amount'] = amount / 100
    return JsonResponse({
        "success" : True, 'payment' : payment,'payment_id': payment['id'], 'amount' : amount,
    })

def update_wallet(request):
    email = request.session['email']
    amount = request.session['amount']
    user_name = CustomUser.objects.get(email=email)
    user = Wallet.objects.filter(user=user_name).order_by('-id').first()
    if not user:
        balance = 0
    else:
        balance = user.balance
    
    new_balance = balance+amount
    Wallet.objects.create(
        user=user_name,
        amount=amount,
        balance=new_balance,
        transaction_type = "Credit",
        transaction_details = f"Added Money through Razorpay"
    )

    return redirect('wallet')
