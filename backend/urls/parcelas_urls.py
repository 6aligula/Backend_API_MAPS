from django.urls import path
from backend.views import parcelas_views as views

urlpatterns = [
    path('caracteristicas-parcela/', views.caracteristicas_parcela_list, name='caracteristicas-parcela'),
    path('usos-parcela/', views.usos_parcela_list, name='usos-parcela'),
    path('contadores-medidas/', views.contadores_medidas_list, name='contadores-medidas'),
    path('consumos/', views.consumos_list, name='consumos'),
    path('datos-adicionales/', views.datos_adicionales_list, name='datos-adicionales'),
    path('control-pagos/', views.control_pagos_list, name='control-pagos'),

]
