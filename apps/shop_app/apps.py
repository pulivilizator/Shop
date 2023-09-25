from django.apps import AppConfig


class ShopAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.shop_app'

    def ready(self):
        import apps.shop_app.signals
