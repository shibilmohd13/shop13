from cart.models import Cart
from products.models import *
from userlogin.models import *


# Context processor for Provide list of Categories, Brands And also User in Every View
def navbar_elements(request):
    categories_nav = Category.objects.exclude(is_listed=False)
    brands_nav = Brand.objects.exclude(is_listed=False)    
    try: 
        user = request.session['email']
        user_obj = CustomUser.objects.get(email=user)
        return {'users' : user, 'categories_nav' : categories_nav , 'brands_nav' : brands_nav, 'user_obj' : user_obj}
    except:
        return {'users' : 'Login Now', 'categories_nav' : categories_nav , 'brands_nav' :brands_nav}

def cart_count_badge(request):
    count = 0
    try:
        if 'email' in request.session:
            email = request.session['email']
            user = CustomUser.objects.get(email=email)
            count = Cart.objects.filter(user=user).count()
    except:
        count=0
    return {'cart_count' : count}
