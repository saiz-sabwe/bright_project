from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Model_Service, Model_Demande, Model_Professionnel


from django.contrib import admin
from django.db.models.signals import post_save
from .models import Model_Demande

@admin.action(description="Valider les demandes sélectionnées")
def valider_demandes(modeladmin, request, queryset):
    for demande in queryset:
        demande.statut = Model_Demande.STATUT_ACCEPTE
        demande.cloturer_demande(save=False)
        demande.save()

@admin.action(description="Refuser les demandes sélectionnées")
def refuser_demandes(modeladmin, request, queryset):
    for demande in queryset:
        demande.statut = Model_Demande.STATUT_REFUSE
        demande.cloturer_demande(save=False)
        demande.save()


@admin.register(Model_Service)
class ModelServiceAdmin(ImportExportModelAdmin):
    list_display = (
        'id', 'nom', 'description', 'rang', 'create', 'last_update', 'create_by', 'update_by'
    )
    search_fields = ('nom', 'description')
    list_filter = ('create', 'last_update', 'create_by', 'update_by')
    readonly_fields = ('create', 'last_update', 'create_by', 'update_by')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.create_by = request.user
        obj.update_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Model_Demande)
class ModelDemandeAdmin(ImportExportModelAdmin):
    list_display = (
        'id', 'profil', 'isClosed', 'service', 'professionnel', 'date_souhaitee',
        'adresse', 'statut', 'create', 'last_update', 'create_by', 'update_by'
    )
    search_fields = ('profil__pseudo', 'adresse', 'description')
    list_filter = (
        'statut', 'service', 'professionnel', 'create', 'last_update'
    )
    readonly_fields = ('create', 'last_update', 'create_by', 'update_by')
    actions = [valider_demandes, refuser_demandes]

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.create_by = request.user
        obj.update_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Model_Professionnel)
class ModelProfessionnelAdmin(ImportExportModelAdmin):
    list_display = (
        'id', 'profil', 'titre', 'note',
        'create', 'last_update', 'create_by', 'update_by'
    )
    search_fields = ('profil__pseudo', 'titre')
    list_filter = ('note', 'create', 'last_update')
    readonly_fields = ('create', 'last_update', 'create_by', 'update_by')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.create_by = request.user
        obj.update_by = request.user
        super().save_model(request, obj, form, change)