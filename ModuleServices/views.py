from rest_framework import generics, permissions

from ModuleProfil.models import Model_Profil
from .models import Model_Service, Model_Demande, Model_Professionnel
from .serializers import ServiceSerializer, DemandeCreateSerializer, DemandeListSerializer, ProfessionnelSerializer


class ServiceListView(generics.ListAPIView):
    queryset = Model_Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated]

class DemandeCreateView(generics.CreateAPIView):
    serializer_class = DemandeCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        profil = Model_Profil.objects.get(user=self.request.user)
        serializer.save(profil=profil, create_by=self.request.user, update_by=self.request.user)

class DemandeListView(generics.ListAPIView):
    serializer_class = DemandeListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        profil = Model_Profil.objects.get(user=self.request.user)
        return Model_Demande.objects.filter(profil=profil).order_by('-create')

class ProfessionnelByServiceView(generics.ListAPIView):
    serializer_class = ProfessionnelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        service_id = self.request.query_params.get("service")
        return Model_Professionnel.objects.filter(services__id=service_id)
