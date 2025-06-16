from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Agent, Presence

@admin.register(Agent)
class AgentAdmin(ImportExportModelAdmin):
    list_display = ('id', 'nom', 'postnom', 'prenom', 'matricule', 'fonction', 'service', 'direction')
    search_fields = ('nom', 'postnom', 'prenom', 'matricule', 'fonction', 'service')
    list_filter = ('direction', 'service', 'fonction')
    ordering = ('nom',)

@admin.register(Presence)
class PresenceAdmin(ImportExportModelAdmin):
    list_display = ('id', 'agent', 'date', 'heure_arrivee', 'heure_depart')
    search_fields = ('agent__nom', 'agent__postnom', 'agent__matricule')
    list_filter = ('date',)
    ordering = ('-date',)

    def has_add_permission(self, request):
        # Laisse Django gérer par défaut, ou personnalise ici si besoin
        return super().has_add_permission(request)
