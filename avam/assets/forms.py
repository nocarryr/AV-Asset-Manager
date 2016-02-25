from django import forms

from assets import models
from site_navigation.widgets import (
    MDLTextInput,
    MDLNumberInput,
    MDLCheckBox,
    MDLSelect
)

class AssetFormBase(forms.ModelForm):
    class Meta:
        fields = [
            'in_use',
            'retired',
            'notes',
            'date_acquired',
            'serial_number',
            'location',
            'asset_model',
        ]
        widgets = {
            'in_use':MDLCheckBox(),
            'retired':MDLCheckBox(),
            'notes':MDLTextInput(),
            'date_acquired':MDLTextInput(),
            'serial_number':MDLTextInput(),
            'location':MDLSelect(), 
            'asset_model':MDLSelect(),
        }

class LifeTrackedAssetForm(AssetFormBase):
    class Meta:
        fields = [
            'current_usage',
            'excpected_life',
        ]
        widgets = {
            'current_usage':MDLNumberInput(),
            'excpected_life':MDLNumberInput(),
        }

class LampForm(LifeTrackedAssetForm):
    class Meta:
        fields = [
            'installed_in',
        ]
        widgets = {
            'installed_in':MDLSelect(),
        }

class FilterForm(LifeTrackedAssetForm):
    class Meta:
        fields = [
            'installed_in',
        ]
        widgets = {
            'installed_in':MDLSelect(),
        }

class LensForm(AssetFormBase):
    class Meta:
        fields = [
            'installed_in',
        ]
        widgets = {
            'installed_in':MDLSelect(),
        }

def form_cls_for_model(m):
    if issubclass(m, models.LampBase):
        fcls = LampForm
    elif issubclass(m, models.FilterBase):
        fcls = FilterForm
    elif issubclass(m, models.LensBase):
        fcls = LensForm
    else:
        fcls = AssetFormBase
    return fcls

def build_model_form(model=None, instance=None):
    if model is None:
        model = instance._meta.model
    fcls = form_cls_for_model(model)
    return forms.modelform_factory(model, form=fcls)

def build_form(model=None, **kwargs):
    model_form = build_model_form(model, kwargs.get('instance'))
    return model_form(**kwargs)