from django.contrib import admin
from django.db import models

from assets.models import (
    GenericAsset,
    GenericAccessory,
    Projector,
    ProjectorLamp,
    ProjectorFilter,
    MovingLight,
    MovingLightLamp,
    LEDLight,
)

from assets.fields import HoursField

class AssetAdminBase(admin.ModelAdmin):
    formfield_overrides = {
        models.DurationField:{
            'form_class':HoursField,
            'widget':admin.widgets.AdminTextInputWidget,
        }
    }
    list_display = [
        'asset_model',
        'location',
        'in_use',
        'retired',
    ]
    list_filter = [
        'retired',
        'in_use',
        'location',
    ]

@admin.register(GenericAsset)
class GenericAssetAdmin(AssetAdminBase):
    pass

@admin.register(GenericAccessory)
class GenericAccessoryAdmin(AssetAdminBase):
    pass

@admin.register(Projector)
class ProjectorAdmin(AssetAdminBase):
    pass

@admin.register(ProjectorLamp)
class ProjectorLampAdmin(AssetAdminBase):
    pass

@admin.register(ProjectorFilter)
class ProjectorFilterAdmin(AssetAdminBase):
    pass

@admin.register(MovingLight)
class MovingLightAdmin(AssetAdminBase):
    pass

@admin.register(MovingLightLamp)
class MovingLightLampAdmin(AssetAdminBase):
    pass

@admin.register(LEDLight)
class LEDLightAdmin(AssetAdminBase):
    pass
