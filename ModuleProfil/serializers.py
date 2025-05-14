from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Model_Profil

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    pseudo = serializers.CharField()
    phone_number = serializers.CharField()
    nom = serializers.CharField()
    prenom = serializers.CharField()
    commune = serializers.CharField()

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        profil = Model_Profil.objects.create(
            user=user,
            pseudo=validated_data['pseudo'],
            phone_number=validated_data['phone_number'],
            nom=validated_data['nom'],
            prenom=validated_data['prenom'],
            commune=validated_data['commune']
        )
        return user, profil


class ProfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model_Profil
        fields = '__all__'
        depth = 1
