from django.contrib import admin

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

@admin.register(GenericAsset)
class GenericAssetAdmin(admin.ModelAdmin):
    pass

@admin.register(GenericAccessory)
class GenericAccessoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Projector)
class ProjectorAdmin(admin.ModelAdmin):
    pass

@admin.register(ProjectorLamp)
class ProjectorLampAdmin(admin.ModelAdmin):
    pass

@admin.register(ProjectorFilter)
class ProjectorFilterAdmin(admin.ModelAdmin):
    pass

@admin.register(MovingLight)
class MovingLightAdmin(admin.ModelAdmin):
    pass

@admin.register(MovingLightLamp)
class MovingLightLampAdmin(admin.ModelAdmin):
    pass

@admin.register(LEDLight)
class LEDLightAdmin(admin.ModelAdmin):
    pass
