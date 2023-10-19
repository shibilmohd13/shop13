from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from userlogin.models import CustomUser
# Create your views here.

def admin_login(request):
    if request.method == 'POST':
        email = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            if user.is_superuser:
                return redirect('admin_dash')
            else:
                return redirect('admin_login')
        else:
            return redirect('admin_login')
    return render(request, 'admin_panel/admin_login.html')

def admin_dash(request):
    return render(request, 'admin_panel/admin_dash.html')

def users(request):
    users = CustomUser.objects.all().exclude(is_superuser=True).order_by('id')
    context = { 'users' : users}
    return render(request, 'admin_panel/users.html', context)

def user_status(request, id):
    user = CustomUser.objects.filter(id=id).first()
    if user.is_active == True:
        user.is_active = False
        user.save()
    else:
        user.is_active = True
        user.save()
    return redirect('users')

def admin_logout(request):
    request.session.flush()
    return redirect('admin_login')
