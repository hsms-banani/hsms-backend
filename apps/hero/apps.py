from django.apps import AppConfig

class HeroConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.hero'
    verbose_name = 'Hero Section Management'

    def ready(self):
        # Import signals here if you need any
        pass