from django.apps import AppConfig
from django.db.models.signals import post_save

def on_asset_model_post_save(sender, **kwargs):
    if kwargs.get('raw'):
        return
    instance = kwargs.get('instance')
    instance.add_model_category_defaults()

class AssetTypesConfig(AppConfig):
    name = 'assettypes'
    def ready(self):
        ModelBase = self.models_module.ModelBase
        for m in self.get_models():
            if not issubclass(m, ModelBase):
                continue
            post_save.connect(on_asset_model_post_save, sender=m)
