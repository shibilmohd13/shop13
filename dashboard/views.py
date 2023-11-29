from datetime import datetime,timedelta
from django.utils import timezone
from django.shortcuts import render,redirect
from orders.models import Orders, OrdersItem
from products.models import *
from userlogin.models import CustomUser
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.cache import cache_control
from django.http import HttpResponse,JsonResponse
from django.db.models import Sum , F,Count, ExpressionWrapper, DecimalField
import csv
import xlwt
from django.db.models.functions import TruncMonth,TruncYear


# Dashboard with Sales report
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u:u.is_superuser, login_url='admin_login')
def admin_dash(request):

    users_count = CustomUser.objects.filter(is_active=True,is_superuser=False).count()

    total_revenue = round(
        OrdersItem.objects
        .exclude(status="Cancelled")
        .exclude(status="Returned")
        .annotate(total_price=ExpressionWrapper(F('quantity') * F('price'), output_field=DecimalField()))
        .aggregate(total_revenue=Sum('total_price'))['total_revenue'] or 0
    )    

    order_counts = Orders.objects.all().count()

    recent_updations = OrdersItem.objects.all().order_by('-modified_time')[:8]

    recent_orders = Orders.objects.all().order_by('-order_date')

    razorpay_orders = OrdersItem.objects.filter(order__payment_method="razorpay").count()
    wallet_orders = OrdersItem.objects.filter(order__payment_method="wallet").count()
    cod_orders = OrdersItem.objects.filter(order__payment_method="COD").count()


    all_brands = Brand.objects.all()
    sales_data = []

    for brand in all_brands:
        brand_sales = OrdersItem.objects.filter(variant__product__brands=brand).count()
        sales_data.append((brand.name, brand_sales))

    
    #################### Pro ####################
    order_filter = request.GET.get('orderfilter')

    if order_filter == "Y":

        # Query to get the yearly order count for the last 7 years including this year
        order_count_datas = (
            Orders.objects.annotate(year=TruncYear('order_date'))
            .values('year')
            .annotate(order_count=Count('order_id'))
            .order_by('-year')[:7]
        )

        # Reverse the order_count_data list to start from the most recent year
        order_count_datas = list(reversed(order_count_datas))

        # Prepare data for rendering yearly sales in the template
        order_data = [
            (entry['year'].strftime('%Y'), entry['order_count']) for entry in order_count_datas
        ]

        # Get the current date
        current_date = datetime.now()

        # Create a list of the last 7 years
        last_seven_years = [current_date.strftime('%Y')]

        for i in range(1, 7):
            # Subtract one year from the current date in each iteration
            current_date = current_date - timedelta(days=365)
            last_seven_years.append(current_date.strftime('%Y'))

        # Print the list of the last 7 years
        print(last_seven_years)

        dict1 = dict(order_data)

        # Create the result list
        order_count_data = [(item, dict1.get(item, 0)) for item in last_seven_years][::-1]

        

    elif order_filter == "M":

        # Query to get the monthly order count for the last 7 months including this month
        order_count_datas = (
            Orders.objects.annotate(month=TruncMonth('order_date'))
            .values('month')
            .annotate(order_count=Count('order_id'))
            .order_by('-month')[:7]
        )

        # Reverse the order_count_data list to start from the most recent month
        order_count_datas = list(reversed(order_count_datas))

        # Prepare data for rendering monthly sales in the template
        order_data = [
            (entry['month'].strftime('%Y-%m'), entry['order_count']) for entry in order_count_datas
        ]


        # Get the current date
        current_date = datetime.now()

        # Create a list of the last 7 months
        last_seven_months = [current_date.strftime('%Y-%m')]

        for i in range(1, 7):
            # Subtract one month from the current date in each iteration
            current_date = current_date - timedelta(days=current_date.day)
            last_seven_months.append(current_date.strftime('%Y-%m'))

        # Print the list of the last 7 months
        print(last_seven_months)

        dict1 = dict(order_data)

        # Create the result list
        order_count_data = [(item, dict1.get(item, 0)) for item in last_seven_months][::-1]
    else:

        # Calculate today's date
        today = timezone.now().date()

        # Calculate the date 6 days ago from today
        six_days_ago = today - timedelta(days=6)

        # Generate a list of date ranges for the last 7 days
        date_ranges = [six_days_ago + timedelta(days=i) for i in range(7)]

        # Query to get the order count per day for the last 7 days
        order_count_per_day = Orders.objects.filter(order_date__gte=six_days_ago)\
                                            .extra({'order_day': "date(order_date)"})\
                                            .values('order_day')\
                                            .annotate(order_count=Count('order_id'))\
                                            .order_by('order_day')

        # Create a dictionary to store the order counts by day
        order_count_dict = {entry['order_day']: entry['order_count'] for entry in order_count_per_day}

        # Prepare data for rendering in the template
        order_count_data = [
            (day.strftime('%Y-%m-%d'), order_count_dict.get(day, 0)) for day in date_ranges
        ]



    sales_from = request.GET.get('sales_from')
    sales_to = request.GET.get('sales_to')


    if sales_from and sales_to :
        sales_report = Orders.objects.all().order_by('-order_date').filter(order_date__range=[sales_from, sales_to])
    elif sales_from:
        sales_report = Orders.objects.all().order_by('-order_date').filter(order_date__gte=sales_from)
    elif sales_to:
        sales_report = Orders.objects.all().order_by('-order_date').filter(order_date__lte=sales_to)
    else: 
        sales_report = Orders.objects.all().order_by('-order_date')
    
    top_products = OrdersItem.objects.values('variant__product__name', 'variant__color')\
                      .annotate(total_sold=Sum('quantity'))\
                      .order_by('-total_sold')[:5]

    # Prepare data for rendering in the template as a list of tuples
    product_sales_data = [(product['variant__product__name'], product['variant__color'], product['total_sold']) for product in top_products]

    # Pass both sets of data to the template

    print(order_count_data)
    context = {

        'users_count' : users_count,
        'total_revenue' : total_revenue,
        'order_counts' : order_counts,
        'recent_updations' : recent_updations,
        'recent_orders' : recent_orders,
        'razorpay_orders' : razorpay_orders,
        'wallet_orders' : wallet_orders,
        'cod_orders' : cod_orders,
        'sales_data' : sales_data,
        'sales_report' : sales_report,
        'product_sales_data': product_sales_data,
        'order_count_data' : order_count_data,


    }
    
    return render(request, 'admin_panel/admin_dash.html',context)


def download_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=SalesReport-'+ str(datetime.now())+'-.csv' 
    writer = csv.writer(response)
    writer.writerow(['SI.NO','Order ID', 'User', 'Date', 'Time', 'Products', 'Quantity', 'Total','Payment Method'])


    # Retrieve the 'sales_from' parameter from the request, or use the default value
    sales_from = request.GET.get('sales_from',0)
    print(type(sales_from))

    sales_to = request.GET.get('sales_to',0)
    print(type(sales_to))

    if sales_from == "":
        sales_from = datetime.now() - timedelta(days=3 * 365)
    
    if sales_to == "":
        sales_to = datetime.now()

    orders = Orders.objects.all().order_by('-order_date').filter(order_date__range=[sales_from, sales_to])
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

    sales_from = request.GET.get('sales_from')
    sales_to = request.GET.get('sales_to')

    if not sales_from:
        sales_from = datetime.now() - timedelta(days=3 * 365)
    
    if not sales_to:
        sales_to = datetime.now()

    orders = Orders.objects.all().order_by('-order_date').filter(order_date__range=[sales_from, sales_to]).values_list('order_id','user__fullname','order_date__date','order_date__time','ordersitem__variant__product__name','ordersitem__variant__color','ordersitem__quantity','ordersitem__price','payment_method')
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





#Automaticly downloads to PDF file
class DownloadPDF(View):
	def get(self, request, *args, **kwargs):
		

		sales_from = request.GET.get('sales_from')
		sales_to = request.GET.get('sales_to')
		if sales_from == "":
			sales_from = datetime.now() - timedelta(days=3 * 365)
		if sales_to == "":
			sales_to = datetime.now()
		
		
		orders = Orders.objects.all().order_by('-order_date').filter(order_date__range=[sales_from, sales_to])
		
		data = {
            "company": "SHOP 13",
            "address": sales_from,
            "city": "Malappuram",
            "state": "Kerala",
            "zipcode": "676505",
            'orders': orders,
            "phone": sales_to,
            "email": "shop13ecommerce@gmail.com",
            "website": "shop13ecommerce.com",
	    }

		pdf = render_to_pdf('admin_panel/sales_report.html', data)

		response = HttpResponse(pdf, content_type='application/pdf')
		filename = f"Sales_report_{datetime.now()}.pdf"
		content = "attachment; filename='%s'" %(filename)
		response['Content-Disposition'] = content
		return response


def today_revenue(request):
    today = timezone.now().date()

    total_revenue = round(
        OrdersItem.objects
        .exclude(status="Cancelled")
        .exclude(status="Returned")
        .filter(order__order_date__gte=today)  # Add this line to filter orders placed today or later
        .annotate(total_price=ExpressionWrapper(F('quantity') * F('price'), output_field=DecimalField()))
        .aggregate(total_revenue=Sum('total_price'))['total_revenue'] or 0
    )
    dates = "Today"
    return JsonResponse({'success': True , 'todayRevenue': total_revenue, 'date': dates })
def this_month_revenue(request):

    today = timezone.now().date()
    first_day_of_month = today.replace(day=1)

    total_revenue = round(
        OrdersItem.objects
        .exclude(status="Cancelled")
        .exclude(status="Returned")
        .filter(order__order_date__gte=first_day_of_month)  # Filter orders from the first day of the month
        .annotate(total_price=ExpressionWrapper(F('quantity') * F('price'), output_field=DecimalField()))
        .aggregate(total_revenue=Sum('total_price'))['total_revenue'] or 0
    )
    dates = "This Month"
    return JsonResponse({'success': True , 'todayRevenue': total_revenue, 'date': dates })
def all_revenue(request):
    total_revenue = round(
        OrdersItem.objects
        .exclude(status="Cancelled")
        .exclude(status="Returned")
        .annotate(total_price=ExpressionWrapper(F('quantity') * F('price'), output_field=DecimalField()))
        .aggregate(total_revenue=Sum('total_price'))['total_revenue'] or 0
    )    

    dates = "All"
    return JsonResponse({'success': True , 'todayRevenue': total_revenue, 'date': dates })

def today_sales(request):
    today = timezone.now().date()
    sales_today = Orders.objects.all().filter(order_date__gte=today).count()
    date = "Today"
    return JsonResponse({'success': True , 'todaySales' : sales_today , 'date' : date})
def this_month_sales(request):
    today = timezone.now().date()
    first_day_of_month = today.replace(day=1)
    sales_today = Orders.objects.all().filter(order_date__gte=first_day_of_month).count()
    date = "This Month"
    return JsonResponse({'success': True , 'todaySales' : sales_today , 'date' : date})

def all_sales(request):
    print("get")
    sales_today = Orders.objects.all().count()
    date = "All"
    print("get2")
    return JsonResponse({'success': True , 'todaySales' : sales_today , 'date' : date})