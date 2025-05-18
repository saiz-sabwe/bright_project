from django.db import models
from django.conf import settings


class Model_Service(models.Model):
    nom = models.CharField(max_length=100, verbose_name="Nom du service")
    description = models.TextField(verbose_name="Description")
    icon = models.ImageField(upload_to='services/', null=True, blank=True, verbose_name="Icône")

    create = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    last_update = models.DateTimeField(auto_now=True, verbose_name="Dernière mise à jour")
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, default=None, on_delete=models.SET_NULL, related_name="service_createby", verbose_name="Créé par")
    update_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, default=None, on_delete=models.SET_NULL, related_name="service_updateby", verbose_name="Mis à jour par")

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"
        ordering = ("-create",)


class Model_Demande(models.Model):
    STATUTS = [
        ("attente", "En attente"),
        ("acceptee", "Acceptée"),
        ("refusee", "Refusée"),
    ]

    profil = models.ForeignKey( "ModuleProfil.Model_Profil", on_delete=models.CASCADE, related_name='demandes', verbose_name="Client (profil)")
    service = models.ForeignKey('ModuleServices.Model_Service', on_delete=models.CASCADE, verbose_name="Service demandé")
    professionnel = models.ForeignKey("ModuleServices.Model_Professionnel", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Professionnel assigné")
    date_souhaitee = models.DateField(verbose_name="Date souhaitée")
    adresse = models.CharField(max_length=255, verbose_name="Adresse d’intervention")
    description = models.TextField(verbose_name="Description du besoin")
    statut = models.CharField(max_length=20, choices=STATUTS, default="attente", verbose_name="Statut")

    create = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    last_update = models.DateTimeField(auto_now=True, verbose_name="Dernière mise à jour")
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, default=None, on_delete=models.SET_NULL, related_name="demande_createby", verbose_name="Créé par")
    update_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, default=None, on_delete=models.SET_NULL, related_name="demande_updateby", verbose_name="Mis à jour par")

    def __str__(self):
        return f"{self.profil.pseudo} → {self.service.nom} ({self.statut})"

    class Meta:
        verbose_name = "Demande"
        verbose_name_plural = "Demandes"
        ordering = ("-create",)


class Model_Professionnel(models.Model):
    profil = models.OneToOneField( "ModuleProfil.Model_Profil", on_delete=models.CASCADE, related_name="professionnel", verbose_name="Profil associé")
    titre = models.CharField(max_length=255, verbose_name="Titre professionnel")
    note = models.FloatField(default=0.0, verbose_name="Note moyenne")
    services = models.ManyToManyField("ModuleServices.Model_Service", related_name="professionnels", verbose_name="Services proposés")

    create = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    last_update = models.DateTimeField(auto_now=True, verbose_name="Dernière mise à jour")
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, default=None, on_delete=models.SET_NULL, related_name="pro_createby", verbose_name="Créé par")
    update_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, default=None, on_delete=models.SET_NULL, related_name="pro_updateby", verbose_name="Mis à jour par")

    def __str__(self):
        return f"PRO {self.profil.pseudo} - {self.titre}"

    class Meta:
        verbose_name = "Professionnel"
        verbose_name_plural = "Professionnels"
        ordering = ("-create",)

