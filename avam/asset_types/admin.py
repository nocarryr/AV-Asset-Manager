from django.contrib import admin

from asset_types.models import (
    Manufacturer,
    GenericModel,
    GenericAccessoryModel,
    LampModel,
    FilterModel,
    ProjectorModel,
    MovingLightModel,
    LEDLightModel,
)

@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    pass

@admin.register(GenericModel)
class GenericModelAdmin(admin.ModelAdmin):
    pass

@admin.register(GenericAccessoryModel)
class GenericAccessoryModelAdmin(admin.ModelAdmin):
    pass

@admin.register(ProjectorModel)
class ProjectorModelAdmin(admin.ModelAdmin):
    pass

@admin.register(MovingLightModel)
class MovingLightModelAdmin(admin.ModelAdmin):
    pass

@admin.register(LEDLightModel)
class LEDLightModelAdmin(admin.ModelAdmin):
    pass

@admin.register(LampModel)
class LampModelAdmin(admin.ModelAdmin):
    pass

@admin.register(FilterModel)
class FilterModelAdmin(admin.ModelAdmin):
    pass
