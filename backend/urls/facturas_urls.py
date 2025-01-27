# urls.py
from django.urls import path
from backend.views import facturas_view as views

urlpatterns = [
    path('all/', views.get_facturas, name='get_facturas'),
    path('<int:factura_id>/pdf/', views.generate_pdf_invoice, name='factura-pdf'),
    path('generate/payment/pdf/', views.generate_payment_report, name='factura-pdf'),
]
