from django.db import models
from ModuleProfil.models import Model_Profil, Model_Professionnel

class Model_Service(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.ImageField(upload_to='services/', null=True, blank=True)

    def __str__(self):
        return self.nom


class Model_Demande(models.Model):
    STATUTS = [
        ("attente", "En attente"),
        ("acceptee", "Acceptée"),
        ("refusee", "Refusée"),
    ]

    profil = models.ForeignKey(Model_Profil, on_delete=models.CASCADE, related_name='demandes')
    service = models.ForeignKey(Model_Service, on_delete=models.CASCADE)
    professionnel = models.ForeignKey(Model_Professionnel, null=True, blank=True, on_delete=models.SET_NULL)
    date_souhaitee = models.DateField()
    adresse = models.CharField(max_length=255)
    description = models.TextField()
    statut = models.CharField(max_length=20, choices=STATUTS, default="attente")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.profil.pseudo} → {self.service.nom} ({self.statut})"
