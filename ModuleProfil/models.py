from django.contrib.auth.models import User
from django.db import models

class Model_Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profil")
    phone_number = models.CharField(max_length=20, unique=True)
    pseudo = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    commune = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.pseudo} ({self.phone_number})"


class Model_Professionnel(models.Model):
    profil = models.OneToOneField(Model_Profil, on_delete=models.CASCADE, related_name="professionnel")
    titre = models.CharField(max_length=255)
    note = models.FloatField(default=0.0)

    def __str__(self):
        return f"PRO {self.profil.pseudo} - {self.titre}"
