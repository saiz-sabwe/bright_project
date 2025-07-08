from django.utils.crypto import get_random_string
from rest_framework import generics, permissions
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
import urllib.parse
import requests
from .models import Model_Profil, Model_OTP
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


class SendOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone = request.data.get("phone_number")
        existing_user = request.data.get("existing_user")  # bool attendu

        if not phone:
            return Response({"detail": "Numéro requis"}, status=400)

        if existing_user is None:
            return Response({"detail": "Le paramètre 'existing_user' est requis (true ou false)."}, status=400)

        user_qs = User.objects.filter(username=phone)
        user_exists = user_qs.exists()

        # Vérifications de cohérence
        if existing_user is True and not user_exists:
            return Response({"detail": "Aucun utilisateur associé à ce numéro."}, status=400)

        if existing_user is False and user_exists:
            return Response({"detail": "Ce numéro est déjà associé à un utilisateur."}, status=400)


        #  Nettoyer les anciens OTP actifs
        Model_OTP.deactivate_old_otps(phone)

        #  Création d’un nouvel OTP
        otp_instance = Model_OTP.create_otp(phone_number=phone)

        #  Préparation du message
        message = f"Bienvenue sur TEMPO\nVotre code de verification est {otp_instance.otp_code}"
        # print(message)  # Pour debug

        #  Si tu veux envoyer via SMS : décommente cette section
        try:
            encoded_message = urllib.parse.quote(message)
            url = (
                "https://api2.dream-digital.info/api/SendSMS"
                f"?api_id=API18753314170"
                f"&api_password=90crxTbtS9"
                f"&sms_type=T"
                f"&encoding=T"
                f"&sender_id=TEMPO-Co"
                f"&phonenumber={phone}"
                f"&textmessage={encoded_message}"
            )

            response = requests.get(url)
            result = response.json()
            if result.get("status") == "S":
                return Response({"detail": "OTP envoyé avec succès."})
            return Response({"detail": f"Erreur SMS: {result.get('remarks')}"}, status=400)
        except Exception as e:
            return Response({"detail": f"Erreur d'envoi: {str(e)}"}, status=500)

class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone = request.data.get("phone_number")
        code = request.data.get("otp")
        pseudo = request.data.get("pseudo")

        if not all([phone, code, pseudo]):
            return Response({"detail": "Champs requis : phone_number, otp, pseudo"}, status=400)

        random_password = get_random_string(length=8)
        user = User.objects.create_user(username=phone, password=random_password)
        if not user:
            return Response({"detail": "echec de verification."}, status=400)

        profil = Model_Profil.objects.create(user=user, phone_number=phone, pseudo=pseudo)
        if not profil:
            return Response({"detail": "echec de verification.."}, status=400)

        is_valid = Model_OTP.verify_otp(phone_number=phone, code=code)
        if not is_valid:
            return Response({"detail": "OTP invalide ou expiré."}, status=400)


        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            "profil": {
                "id": profil.id,
                "pseudo": profil.pseudo,
                "phone_number": profil.phone_number,
                "token": str(token),
                "uuid": profil.uuid
            }
        })

class LoginOTPRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone = request.data.get("phone_number")

        if not phone:
            return Response({"detail": "Numéro requis"}, status=400)

        try:
            user = User.objects.get(username=phone)
            profil = Model_Profil.objects.get(user=user)
        except User.DoesNotExist:
            return Response({"detail": "Utilisateur inexistant."}, status=400)
        except Model_Profil.DoesNotExist:
            return Response({"detail": "Profil associé non trouvé."}, status=400)

        # 🔁 Désactivation des anciens OTP
        Model_OTP.deactivate_old_otps(phone)

        # 🔢 Création d’un nouvel OTP
        otp_instance = Model_OTP.create_otp(phone)

        # 📤 Préparation du message
        message = f"Connexion TEMPO\nVotre code de verification est {otp_instance.otp_code}"
        print(message)  # Pour debug uniquement

        # ✅ Pour envoyer via SMS, décommente ici :
        try:

            encoded_message = urllib.parse.quote(message)
            url = (
                "https://api2.dream-digital.info/api/SendSMS"
                f"?api_id=API18753314170"
                f"&api_password=90crxTbtS9"
                f"&sms_type=T"
                f"&encoding=T"
                f"&sender_id=TEMPO-Co"
                f"&phonenumber={phone}"
                f"&textmessage={encoded_message}"
            )

            response = requests.get(url)
            result = response.json()
            if result.get("status") == "S":
                return Response({"detail": "OTP envoyé pour connexion."})
            return Response({"detail": f"Erreur SMS: {result.get('remarks')}"}, status=400)
        except Exception as e:
            return Response({"detail": f"Erreur d'envoi: {str(e)}"}, status=500)

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
            profil = Model_Profil.objects.get(user=user)
        except Model_Profil.DoesNotExist:
            return Response({"detail": "Profil introuvable."}, status=400)

        if not Model_OTP.verify_otp(phone_number=phone, code=code):
            return Response({"detail": "OTP invalide ou expiré."}, status=400)

        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            "profil": {
                "id": profil.id,
                "pseudo": profil.pseudo,
                "phone_number": profil.phone_number,
                "token": str(token),
                "uuid": profil.uuid
            }
        })
