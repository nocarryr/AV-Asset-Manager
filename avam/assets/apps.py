from django.apps import AppConfig
from django.db.models.signals import post_migrate


def on_post_migrate(sender, **kwargs):
    import assets.signals
    from django.apps import apps
    object_history = apps.get_app_config('object_history').models_module
    object_history.add_model_history(*[m for m in sender.get_models()])
    
class AssetsConfig(AppConfig):
    name = 'assets'
    def ready(self):
        post_migrate.connect(on_post_migrate, sender=self)
