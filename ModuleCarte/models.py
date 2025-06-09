from django.db import models

# Create your models here.

from django.db import models
from django.utils import timezone


class Agent(models.Model):
    nom = models.CharField(max_length=100, verbose_name="Nom")
    postnom = models.CharField(max_length=100, verbose_name="Post-nom")
    prenom = models.CharField(max_length=100, verbose_name="Prénom")
    direction = models.CharField(max_length=150, verbose_name="Direction")
    service = models.CharField(max_length=150, verbose_name="Service")
    fonction = models.CharField(max_length=100, verbose_name="Fonction")
    matricule = models.CharField(max_length=50, unique=True, verbose_name="Matricule")
    photo = models.ImageField(
        upload_to='agents/photos/',
        null=True,
        blank=True,
        verbose_name="Photo de profil"
    )

    class Meta:
        verbose_name = "Agent"
        verbose_name_plural = "Agents"

    def __str__(self):
        return f"{self.nom} {self.postnom} {self.prenom} ({self.matricule})"

class Presence(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name="presences", verbose_name="Agent")
    date = models.DateField(default=timezone.now, verbose_name="Date")
    heure_arrivee = models.TimeField(null=True, blank=True, verbose_name="Heure d'arrivée")
    heure_depart = models.TimeField(null=True, blank=True, verbose_name="Heure de départ")
    remarques = models.TextField(null=True, blank=True, verbose_name="Remarques")

    class Meta:
        verbose_name = "Présence"
        verbose_name_plural = "Présences"
        unique_together = ('agent', 'date')  # Un enregistrement par jour

    def __str__(self):
        return f"{self.agent} - {self.date}"
