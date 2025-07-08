from django.apps import AppConfig


class ModuleprofilConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ModuleProfil'
    def ready(self):
        import ModuleProfil.signals
