from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .auth import RegisterView
from .views import ProfilMeView, UpdateProfilDetailView, ProfilPartialUpdateView, SendOTPView, VerifyOTPView, \
    LoginOTPRequestView, LoginOTPVerifyView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth-register'),
    path('login/', TokenObtainPairView.as_view(), name='auth-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('me/', ProfilMeView.as_view(), name='profil-me'),
    path('me/update/', UpdateProfilDetailView.as_view(), name='profil-update'),
    path('me/update/partial/', ProfilPartialUpdateView.as_view(), name='profil-partial'),  # PAT
    path('send-otp/', SendOTPView.as_view(), name='send-otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('login-with-otp/', LoginOTPRequestView.as_view(), name='otp-login-request'),
    path('login-with-otp/verify/', LoginOTPVerifyView.as_view(), name='otp-login-verify'),


]
