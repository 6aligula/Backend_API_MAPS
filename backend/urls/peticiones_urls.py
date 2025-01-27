from django.urls import path
from backend.views import peticiones_views as views

urlpatterns = [
    path('crear/', views.crear_peticion, name='crear-peticion'),
    path('obtener/', views.obtener_peticiones, name='obtener-peticiones'),
]
