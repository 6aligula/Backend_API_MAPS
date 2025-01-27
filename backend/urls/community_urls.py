from django.urls import path
from backend.views import community_views as views

urlpatterns = [
    path('all/', views.getCommunityProfile, name="community-profile"),
    path('update/', views.updateCommunity, name="community-update"),

]
