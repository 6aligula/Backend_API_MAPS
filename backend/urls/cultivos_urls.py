from django.urls import path
from backend.views import cultivos_views as views

urlpatterns = [
    path('cultivos/', views.cultivo_list, name='cultivo_list'),
    path('cultivos/<int:pk>/', views.cultivo_detail, name='cultivo_detail'),
    path('fases_cultivo/<int:pk>/', views.fase_cultivo_detail, name='fase_cultivo_detail'),
    # Añadir más rutas según sea necesario
]