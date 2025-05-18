from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .auth import RegisterView
from .views import ProfilMeView, UpdateProfilDetailView, ProfilPartialUpdateView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth-register'),
    path('login/', TokenObtainPairView.as_view(), name='auth-login'),
    path('me/', ProfilMeView.as_view(), name='profil-me'),
    path('me/update/', UpdateProfilDetailView.as_view(), name='profil-update'),
    path('me/update/partial/', ProfilPartialUpdateView.as_view(), name='profil-partial'),  # PATCH


]
