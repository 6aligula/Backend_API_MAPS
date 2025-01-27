from django.urls import path
from backend.views import geo_views as views

urlpatterns = [
    path('', views.getLocations, name="locations"),
    path('get/plot/', views.getPlot, name="locations"),
    path('add/', views.addLocation, name="location-add"),
    path('add/plot/', views.addPlot, name="plot-add"),
    # path('<str:pk>/', views.getLocation, name="location"),
    # path('update/<str:pk>/', views.updateLocation, name="location-update"),
    # path('delete/<str:pk>/', views.deleteLocation, name="location-delete"),
]