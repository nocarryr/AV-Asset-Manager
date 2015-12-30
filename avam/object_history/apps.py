from django.apps import AppConfig
from django.db.models.signals import post_migrate


def on_post_migrate(sender, **kwargs):
    import object_history.signals

class ObjectHistoryConfig(AppConfig):
    name = 'object_history'
    def ready(self):
        post_migrate.connect(on_post_migrate, sender=self)
