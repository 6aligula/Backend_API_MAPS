from django.urls import path
from backend.views import user_views as views

urlpatterns = [
    path('login/', views.MyTokenObtainPairView.as_view(),
        name='token_obtain_pair'),
        
    path('register/', views.registerUser, name='register'),

    path('profile/', views.getUserProfile, name="users-profile"),
    path('profile/update/', views.updateUserProfile, name="users-profile-update"),
    path('forgotpassword/', views.forgotPassword, name="users-forgot-password"),
    path('resetpassword/<uidb64>/<token>/', views.resetPassword, name="users-reset-password"),

]
