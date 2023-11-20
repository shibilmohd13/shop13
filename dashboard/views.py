from django.shortcuts import render
from userlogin.models import CustomUser
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.cache import cache_control
# Create your views here.

# Dashboard with Sales report
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u:u.is_superuser, login_url='admin_login')
def admin_dash(request):
    users_count = CustomUser.objects.filter(is_active=True).count()

    context = {
        'users_count' : users_count,
    }
    
    return render(request, 'admin_panel/admin_dash.html',context)

