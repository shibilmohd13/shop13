from datetime import datetime,timedelta
from django.shortcuts import render,redirect
from orders.models import Orders, OrdersItem
from products.models import Brand
from userlogin.models import CustomUser
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.cache import cache_control
from django.http import HttpResponse,JsonResponse
import csv
import xlwt

# Dashboard with Sales report
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u:u.is_superuser, login_url='admin_login')
def admin_dash(request):
    users_count = CustomUser.objects.filter(is_active=True,is_superuser=False).count()

    total_revenue = round(sum(Orders.objects.values_list('total_amount', flat=True)))
    
    order_count = Orders.objects.all().count()

    recent_updations = OrdersItem.objects.all().order_by('-modified_time')[:8]

    recent_orders = Orders.objects.all().order_by('-order_date')

    razorpay_orders = OrdersItem.objects.filter(order__payment_method="razorpay").count()
    wallet_orders = OrdersItem.objects.filter(order__payment_method="wallet").count()
    cod_orders = OrdersItem.objects.filter(order__payment_method="COD").count()

    all_brands = Brand.objects.values_list('name', flat=True)
    # sold_by_brands = OrdersItem.objects.


    context = {

        'users_count' : users_count,
        'total_revenue' : total_revenue,
        'order_count' : order_count,
        'recent_updations' : recent_updations,
        'recent_orders' : recent_orders,
        'razorpay_orders' : razorpay_orders,
        'wallet_orders' : wallet_orders,
        'cod_orders' : cod_orders,
        'all_brands' : all_brands,


    }
    
    return render(request, 'admin_panel/admin_dash.html',context)


def download_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=SalesReport-'+ str(datetime.now())+'-.csv' 
    writer = csv.writer(response)
    writer.writerow(['SI.NO','Order ID', 'User', 'Date', 'Time', 'Products', 'Quantity', 'Total','Payment Method'])
    orders = Orders.objects.all().order_by('-order_date')
    si_no = 1
    
    for order in orders:
        date = order.order_date.date()
        time = order.order_date.time()
        items = [f'{item.variant.product.name}-{item.variant.color}-({item.quantity} items)' for item in order.ordersitem_set.all()]
        writer.writerow([si_no,order.order_id,order.user.fullname,date,time,",".join(items),order.quantity,order.total_amount,order.payment_method])
        si_no += 1

    return response


def download_exel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=SalesReport-'+ str(datetime.now())+'-.xls' 
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('SalesReport')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold=True
    columns = ['Order ID', 'User', 'Date', 'Time', 'Product','Color', 'Quantity', 'Price','Payment Method']
    for col_num in range(len(columns)):
        ws.write(row_num,col_num,columns[col_num], font_style)
    
    font_style = xlwt.XFStyle()
    orders = Orders.objects.all().order_by('-order_date').values_list('order_id','user__fullname','order_date__date','order_date__time','ordersitem__variant__product__name','ordersitem__variant__color','ordersitem__quantity','ordersitem__price','payment_method')
    print(orders)

    for order in orders:
        row_num+=1
        for col_num in range(len(order)):
            ws.write(row_num,col_num,str(order[col_num]),font_style)

    wb.save(response)

    return response

def download_pdf(request):

    return request


from django.shortcuts import render
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa

def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None

orders = Orders.objects.all().order_by('-order_date')
data = {
	"company": "SHOP 13",
	"address": datetime.now(),
	"city": "Vancouver",
	"state": "WA",
	"zipcode": "676505",
    'orders': orders,
	"phone": timedelta(days=7),
	"email": "shop13ecommerce@gmail.com",
	"website": "shop13ecommerce.com",
	}


#Automaticly downloads to PDF file
class DownloadPDF(View):
	def get(self, request, *args, **kwargs):
		
		pdf = render_to_pdf('admin_panel/sales_report.html', data)

		response = HttpResponse(pdf, content_type='application/pdf')
		filename = f"Sales_report_{datetime.now()}.pdf"
		content = "attachment; filename='%s'" %(filename)
		response['Content-Disposition'] = content
		return response