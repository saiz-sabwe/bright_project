from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from ModuleServices.models import Model_Service


class Model_Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profil", verbose_name="Utilisateur associé")
    phone_number = models.CharField(max_length=20, unique=True, verbose_name="Numéro de téléphone")
    pseudo = models.CharField(max_length=100, verbose_name="Pseudonyme")
    nom = models.CharField(max_length=100, null=True, blank=True, verbose_name="Nom")
    prenom = models.CharField(max_length=100, null=True, blank=True, verbose_name="Prénom")
    commune = models.CharField(max_length=100, null=True, blank=True, verbose_name="Commune")

    create = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    last_update = models.DateTimeField(auto_now=True, verbose_name="Dernière mise à jour")
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, default=None, on_delete=models.SET_NULL, related_name="profil_createby", verbose_name="Créé par")
    update_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, default=None, on_delete=models.SET_NULL, related_name="profil_updateby", verbose_name="Mis à jour par")

    def __str__(self):
        return f"{self.pseudo} ({self.phone_number})"

    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profils"
        ordering = ("-create",)
