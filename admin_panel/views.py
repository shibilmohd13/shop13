from django.shortcuts import render

# Create your views here.

def admin_login(request):
    return render(request, 'admin_panel/admin_login.html')