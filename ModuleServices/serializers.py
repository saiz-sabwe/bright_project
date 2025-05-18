from rest_framework import serializers

from .models import Model_Service, Model_Demande, Model_Professionnel


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model_Service
        fields = '__all__'

class DemandeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model_Demande
        fields = ['id', 'service', 'date_souhaitee', 'adresse', 'description']

class DemandeListSerializer(serializers.ModelSerializer):
    service_nom = serializers.CharField(source="service.nom", read_only=True)

    class Meta:
        model = Model_Demande
        fields = ['id', 'service', 'service_nom', 'date_souhaitee', 'adresse', 'description', 'statut', 'create']

class ProfessionnelSerializer(serializers.ModelSerializer):
    profil_pseudo = serializers.CharField(source="profil.pseudo", read_only=True)

    class Meta:
        model = Model_Professionnel
        fields = ['id', 'profil_pseudo', 'titre', 'note']