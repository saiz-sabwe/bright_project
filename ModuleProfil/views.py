from rest_framework import generics, permissions
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

