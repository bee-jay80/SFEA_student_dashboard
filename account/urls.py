from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('verify-otp/', views.verify_otp_view, name='otp_verification'),
    path('awaiting-approval/', views.awaiting_approval, name='awaiting_approval'),
    path('resend-otp/', views.resend_otp_api, name='resend_otp_api'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.user_logout, name='logout'),
]
