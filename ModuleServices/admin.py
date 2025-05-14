from django.contrib import admin
from import_export.admin import ExportMixin
from .models import Model_Service, Model_Demande

@admin.action(description="✅ Valider les demandes sélectionnées")
def valider_demandes(modeladmin, request, queryset):
    queryset.update(statut="acceptee")

@admin.action(description="❌ Refuser les demandes sélectionnées")
def refuser_demandes(modeladmin, request, queryset):
    queryset.update(statut="refusee")

@admin.register(Model_Service)
class ServiceAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ("nom", "description", "create", "last_update")
    list_filter = ("create", "last_update")
    search_fields = ("nom", "description")
    ordering = ("-create",)


@admin.register(Model_Demande)
class DemandeAdmin(ExportMixin, admin.ModelAdmin):
    list_display = (
        "profil", "service", "professionnel", "date_souhaitee",
        "adresse", "statut", "create", "last_update"
    )
    list_filter = ("statut", "service", "professionnel", "create")
    search_fields = ("profil__pseudo", "adresse", "description")
    ordering = ("-create",)
    actions = [valider_demandes, refuser_demandes]
