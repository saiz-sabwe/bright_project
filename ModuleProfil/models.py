import random
import uuid
from datetime import timedelta

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone

from ModuleServices.models import Model_Service


class Model_Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profil", verbose_name="Utilisateur associé")
    phone_number = models.CharField(max_length=20, unique=True, verbose_name="Numéro de téléphone")
    pseudo = models.CharField(max_length=100, verbose_name="Pseudonyme")
    nom = models.CharField(max_length=100, null=True, blank=True, verbose_name="Nom")
    isStaff = models.BooleanField(default=False, verbose_name="Est un membre du personnel")
    prenom = models.CharField(max_length=100, null=True, blank=True, verbose_name="Prénom")
    commune = models.CharField(max_length=100, null=True, blank=True, verbose_name="Commune")
    uuid = models.CharField(max_length=40, null=True, blank=True, verbose_name="Uuid")

    isActif = models.BooleanField(verbose_name="Actif", default=True)
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

    @classmethod
    def get_staff_profiles(cls):
        return cls.objects.filter(isStaff=True,isActif=True)


class Model_OTP(models.Model):

    OTP_VALIDITY_MINUTES = 10

    phone_number = models.CharField(max_length=20, verbose_name="Numéro de téléphone")
    otp_code = models.CharField(max_length=6)
    is_used = models.BooleanField(default=False, verbose_name="Utilisé")


    isActif = models.BooleanField(verbose_name="Actif", default=True)
    create = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    last_update = models.DateTimeField(auto_now=True, verbose_name="Dernière mise à jour")
    create_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, default=None,
        on_delete=models.SET_NULL, related_name="otp_createby", verbose_name="Créé par")
    update_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, default=None,
        on_delete=models.SET_NULL, related_name="otp_updateby", verbose_name="Mis à jour par")

    def __str__(self):
        return f"{self.id} ({self.phone_number})"

    class Meta:
        verbose_name = "OTP"
        verbose_name_plural = "OTPs"
        ordering = ("-create",)


    @staticmethod
    def generate_otp():
        return str(random.randint(100000, 999999))


    def is_valid(self):
        return (
            not self.is_used and
            self.isActif and
            timezone.now() <= self.create + timedelta(minutes=self.OTP_VALIDITY_MINUTES)
        )


    def mark_as_used(self):
        self.is_used = True
        self.save(update_fields=["is_used", "last_update"])

    @classmethod
    def verify_otp(cls, phone_number, code):

        try:
            otp = cls.objects.filter(
                phone_number=phone_number,
                otp_code=code,
                is_used=False,
                isActif=True
            ).latest('create')

            if otp.is_valid():
                otp.mark_as_used()
                return True
            return False
        except cls.DoesNotExist:
            return False


    @classmethod
    def create_otp(cls, phone_number, user=None):
        code = cls.generate_otp()
        otp = cls.objects.create(
            phone_number=phone_number,
            otp_code=code,
            create_by=user,
            update_by=user
        )
        return otp


    @classmethod
    def get_last_valid_otp(cls, phone_number):
        return cls.objects.filter(
            phone_number=phone_number,
            is_used=False,
            isActif=True,
            create__gte=timezone.now() - timedelta(minutes=cls.OTP_VALIDITY_MINUTES)
        ).order_by('-create').first()


    @classmethod
    def deactivate_old_otps(cls, phone_number):
        cls.objects.filter(
            phone_number=phone_number,
            is_used=False,
            isActif=True
        ).update(isActif=False)
