from django.urls import path
from backend.views import contact_views as views

urlpatterns = [
    path('add/', views.contact_form_view , name="contact-form"),
]
