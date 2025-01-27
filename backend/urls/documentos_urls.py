
#documentos_urls.py
from django.urls import path
from backend.views import documentos_views as views

urlpatterns = [
    path('', views.obtener_documentos, name='obtener-documentos'),
    path('nuevo/', views.crear_documento, name='crear-documento'),
    path('<int:pk>/', views.obtener_documento, name='obtener-documento'),  # Nuevo endpoint

]