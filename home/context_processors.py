from products.models import *

def navbar_elements(request):
    categories_nav = Category.objects.exclude(is_listed=False)
    brands_nav = Brand.objects.exclude(is_listed=False)
    
    try: 
        user = request.session['fullname']
        return {'users' : user, 'categories_nav' : categories_nav , 'brands_nav' :brands_nav}
    except:
        return {'users' : 'Login Now', 'categories_nav' : categories_nav , 'brands_nav' :brands_nav}
