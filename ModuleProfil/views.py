from rest_framework import generics, permissions
from .models import Model_Profil
from .serializers import ProfilSerializer

class ProfilMeView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfilSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profil
