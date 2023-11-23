from django.urls import path,include
from . import views


urlpatterns = [
    path('',views.admin_dash, name='admin_dash'),
    path('download_csv',views.download_csv,name="download_csv"),
    path('download_exel',views.download_exel,name="download_exel"),
    path('download_pdf',views.download_pdf,name="download_pdf"),
    path('pdf_download',views.DownloadPDF.as_view(),name='pdf_download'),
    
]
