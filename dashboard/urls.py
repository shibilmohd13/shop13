from django.urls import path,include
from . import views


urlpatterns = [
    path('',views.admin_dash, name='admin_dash'),
    path('download_csv',views.download_csv,name="download_csv"),
    path('download_exel',views.download_exel,name="download_exel"),
    path('download_pdf',views.download_pdf,name="download_pdf"),
    path('pdf_download',views.DownloadPDF.as_view(),name='pdf_download'),
    path('today_revenue',views.today_revenue,name="today_revenue"),
    path('this_month_revenue',views.this_month_revenue,name="this_month_revenue"),
    path('all_revenue',views.all_revenue,name="all_revenue"),
    path('today_sales',views.today_sales,name="today_sales"),
    path('this_month_sales',views.this_month_sales,name="this_month_sales"),
    path('all_sales',views.all_sales,name="all_sales"),


    
    
]
