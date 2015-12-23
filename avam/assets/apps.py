from django.apps import AppConfig


class AssetsConfig(AppConfig):
    name = 'assets'
    def ready(self):
        import assets.signals
        from django.apps import apps
        object_history = apps.get_app_config('object_history').models_module
        object_history.add_model_history(*[m for m in self.get_models()])
