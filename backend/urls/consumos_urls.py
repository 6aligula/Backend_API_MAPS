from django.urls import path
from backend.views import consumos_views as views

urlpatterns = [
    path('', views.obtener_consumos, name='obtener-consumos'),
]
