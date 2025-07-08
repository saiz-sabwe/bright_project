from django.apps import AppConfig


class ModuleservicesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ModuleServices'
    def ready(self):
        import ModuleServices.signals
