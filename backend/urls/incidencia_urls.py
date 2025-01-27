from django.urls import path
from backend.views import incidencia_views as views

urlpatterns = [
    path('crear/', views.crear_incidencia, name='crear-incidencia'),
    path('obtener/', views.obtener_incidencias, name='obtener-incidencias'),
]
