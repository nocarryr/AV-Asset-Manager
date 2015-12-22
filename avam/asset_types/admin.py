from django.contrib import admin

from asset_types.models import (
    Manufacturer,
    GenericAsset,
    GenericAccessory,
    LampAsset,
    FilterAsset,
    ProjectorAsset,
    MovingLightAsset,
    LEDLightAsset,
)

@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    pass

@admin.register(GenericAsset)
class GenericAssetAdmin(admin.ModelAdmin):
    pass

@admin.register(GenericAccessory)
class GenericAccessoryAdmin(admin.ModelAdmin):
    pass

@admin.register(ProjectorAsset)
class ProjectorAssetAdmin(admin.ModelAdmin):
    pass

@admin.register(MovingLightAsset)
class MovingLightAssetAdmin(admin.ModelAdmin):
    pass

@admin.register(LEDLightAsset)
class LEDLightAssetAdmin(admin.ModelAdmin):
    pass

@admin.register(LampAsset)
class LampAssetAdmin(admin.ModelAdmin):
    pass

@admin.register(FilterAsset)
class FilterAssetAdmin(admin.ModelAdmin):
    pass
