from django.apps import AppConfig


class AppSocialConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_social'

    def ready(self) -> None:
        import app_social.signals

