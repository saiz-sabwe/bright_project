from django.contrib import admin
from import_export.admin import ExportMixin
from .models import Model_Profil, Model_Professionnel

@admin.register(Model_Profil)
class ProfilAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ("pseudo", "phone_number", "nom", "prenom", "commune", "create", "last_update")
    list_filter = ("commune", "create", "last_update")
    search_fields = ("pseudo", "nom", "prenom", "phone_number")
    ordering = ("-create",)


@admin.register(Model_Professionnel)
class ProfessionnelAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ("profil", "titre", "note", "create", "last_update")
    list_filter = ("note", "create", "last_update")
    search_fields = ("profil__pseudo", "titre")
    ordering = ("-create",)
