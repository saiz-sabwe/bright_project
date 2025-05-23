from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Model_Profil


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    pseudo = serializers.CharField()
    password = serializers.CharField(write_only=True, required=False)

    def create(self, validated_data):
        username = validated_data["username"]
        password = validated_data.get("password") or User.objects.make_random_password()

        user = User.objects.create_user(
            username=username,
            password=password
        )
        profil = Model_Profil.objects.create(
            user=user,
            pseudo=validated_data["pseudo"],
            phone_number=username
        )
        return user, profil


class ProfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model_Profil
        fields = '__all__'
        depth = 1
