from django.utils.crypto import get_random_string
from rest_framework import generics, permissions
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Model_Profil
from .serializers import ProfilSerializer


class ProfilMeView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfilSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profil

class UpdateProfilDetailView(generics.UpdateAPIView):
    serializer_class = ProfilSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profil

class ProfilPartialUpdateView(generics.UpdateAPIView):
    serializer_class = ProfilSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profil

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
import urllib.parse
import requests
from .models import Model_OTP

class SendOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone = request.data.get("phone_number")
        existing_user = request.data.get("existing_user")  # bool attendu

        if not phone:
            return Response({"detail": "Numéro requis"}, status=400)

        if existing_user is None:
            return Response({"detail": "Le paramètre 'existing_user' est requis (true ou false)."}, status=400)

        user_exists = User.objects.filter(username=phone).exists()

        if existing_user is True and not user_exists:
            return Response({"detail": "Aucun utilisateur associé à ce numéro."}, status=400)

        if existing_user is False and user_exists:
            return Response({"detail": "Ce numéro est déjà associé à un utilisateur."}, status=400)

        otp = Model_OTP.generate_otp()
        message = f"Bienvenue sur BRIGHT\nVotre code de verification est {otp}"
        encoded_message = urllib.parse.quote(message)

        url = (
            "https://api2.dream-digital.info/api/SendSMS"
            f"?api_id=API18753314170"
            f"&api_password=90crxTbtS9"
            f"&sms_type=T"
            f"&encoding=T"
            f"&sender_id=BRIGHT-Co"
            f"&phonenumber={phone}"
            f"&textmessage={encoded_message}"
        )

        try:
            response = requests.get(url)
            result = response.json()
            if result.get("status") == "S":
                Model_OTP.objects.update_or_create(phone_number=phone, defaults={"code": otp})
                return Response({"detail": "OTP envoyé avec succès."})
            return Response({"detail": f"Erreur SMS: {result.get('remarks')}"}, status=400)
        except Exception as e:
            return Response({"detail": f"Erreur d'envoi: {str(e)}"}, status=500)

        # Model_OTP.objects.update_or_create(phone_number=phone, defaults={"code": otp})
        # print(f"Bienvenue sur BRIGHT\nVotre code de verification est {otp}")
        # return Response({"detail": "OTP envoyé pour connexion."})

class VerifyOTPView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        phone = request.data.get("phone_number")
        code = request.data.get("otp")
        pseudo = request.data.get("pseudo")

        if not all([phone, code, pseudo]):
            return Response({"detail": "Champs requis : phone_number, otp, pseudo"}, status=400)

        try:
            otp_obj = Model_OTP.objects.get(phone_number=phone)
        except Model_OTP.DoesNotExist:
            return Response({"detail": "OTP non trouvé."}, status=400)

        if not otp_obj.is_valid() or str(otp_obj.code) != str(code):
            return Response({"detail": "OTP invalide ou expiré."}, status=400)

        random_password = get_random_string(length=8)
        user = User.objects.create_user(username=phone, password=random_password)
        profil = Model_Profil.objects.create(user=user, phone_number=phone, pseudo=pseudo)
        otp_obj.delete()

        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "profil": {
                "id": profil.id,
                "pseudo": profil.pseudo,
                "phone_number": profil.phone_number
            }
        })

class LoginOTPRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone = request.data.get("phone_number")
        if not phone:
            return Response({"detail": "Numéro requis"}, status=400)

        if not User.objects.filter(username=phone).exists():
            return Response({"detail": "Utilisateur inexistant."}, status=400)

        otp = Model_OTP.generate_otp()
        message = f"Connexion BRIGHT\nVotre code de verification est {otp}"
        encoded_message = urllib.parse.quote(message)

        url = (
            "https://api2.dream-digital.info/api/SendSMS"
            f"?api_id=API18753314170"
            f"&api_password=90crxTbtS9"
            f"&sms_type=T"
            f"&encoding=T"
            f"&sender_id=BRIGHT-Co"
            f"&phonenumber={phone}"
            f"&textmessage={encoded_message}"
        )

        try:
            response = requests.get(url)
            result = response.json()
            if result.get("status") == "S":
                Model_OTP.objects.update_or_create(phone_number=phone, defaults={"code": otp})
                return Response({"detail": "OTP envoyé pour connexion."})
            return Response({"detail": f"Erreur SMS: {result.get('remarks')}"}, status=400)
        except Exception as e:
            return Response({"detail": f"Erreur d'envoi: {str(e)}"}, status=500)

        # Model_OTP.objects.update_or_create(phone_number=phone, defaults={"code": otp})
        # print(f"Bienvenue sur BRIGHT\nVotre code de verification est {otp}")
        # return Response({"detail": "OTP envoyé pour connexion."})


class LoginOTPVerifyView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone = request.data.get("phone_number")
        code = request.data.get("otp")

        if not all([phone, code]):
            return Response({"detail": "Champs requis : phone_number, otp"}, status=400)

        try:
            user = User.objects.get(username=phone)
        except User.DoesNotExist:
            return Response({"detail": "Utilisateur introuvable."}, status=400)

        try:
            otp_obj = Model_OTP.objects.get(phone_number=phone)
        except Model_OTP.DoesNotExist:
            return Response({"detail": "OTP non trouvé."}, status=400)

        if not otp_obj.is_valid() or str(otp_obj.code) != str(code):
            return Response({"detail": "OTP invalide ou expiré."}, status=400)

        otp_obj.delete()

        refresh = RefreshToken.for_user(user)
        profil = user.profil
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "profil": {
                "id": profil.id,
                "pseudo": profil.pseudo,
                "phone_number": profil.phone_number
            }
        })
