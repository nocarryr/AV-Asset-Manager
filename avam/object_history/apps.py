from django.apps import AppConfig


class ObjectHistoryConfig(AppConfig):
    name = 'object_history'
    def ready(self):
        import object_history.signals
