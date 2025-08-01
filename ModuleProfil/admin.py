from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Model_Profil, Model_OTP


@admin.register(Model_Profil)
class ModelProfilAdmin(ImportExportModelAdmin):
    list_display = (
        'id', 'user', 'pseudo', 'phone_number', 'nom', 'prenom', 'commune',
        'create', 'last_update', 'create_by', 'update_by'
    )
    search_fields = ('pseudo', 'phone_number', 'nom', 'prenom', 'user__username')
    list_filter = ('commune', 'create', 'last_update')
    readonly_fields = ('create', 'last_update', 'create_by', 'update_by')
    ordering = ('-create',)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.create_by = request.user
        obj.update_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Model_OTP)
class ModelOTPAdmin(ImportExportModelAdmin):
    list_display = (
        'id', 'phone_number', 'otp_code', 'is_used', 'create', 'last_update',
        'create_by', 'update_by'
    )
    search_fields = ('phone_number', 'otp_code')
    list_filter = ('is_used', 'create', 'last_update')
    readonly_fields = ('create', 'last_update', 'create_by', 'update_by')
    ordering = ('-create',)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.create_by = request.user
        obj.update_by = request.user
        super().save_model(request, obj, form, change)
