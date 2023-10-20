from products.models import *

def navbar_elements(request):
    categories_nav = Category.objects.all()
    brands_nav = Brand.objects.all()

    try: 
        user = request.session['fullname']
        return {'user' : user, 'categories_nav' : categories_nav , 'brands_nav' :brands_nav}
    except:
        return {'user' : 'Login Now', 'categories_nav' : categories_nav , 'brands_nav' :brands_nav}
