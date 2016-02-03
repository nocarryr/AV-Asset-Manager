from django.contrib import admin

from assettypes.models import (
    Manufacturer,
    GenericModel,
    GenericAccessoryModel,
    ProjectorLampModel,
    ProjectorFilterModel,
    ProjectorLensModel,
    ProjectorModel,
    MovingLightLampModel,
    MovingLightModel,
    LEDLightModel,
    CameraLensModel,
    VideoCameraModel,
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

@admin.register(ProjectorLampModel)
class ProjectorLampModelAdmin(admin.ModelAdmin):
    pass

@admin.register(ProjectorFilterModel)
class ProjectorFilterModelAdmin(admin.ModelAdmin):
    pass

@admin.register(ProjectorLensModel)
class ProjectorLensModelAdmin(admin.ModelAdmin):
    pass

@admin.register(MovingLightLampModel)
class MovingLightLampModelAdmin(admin.ModelAdmin):
    pass

@admin.register(VideoCameraModel)
class VideoCameraModelAdmin(admin.ModelAdmin):
    pass

@admin.register(CameraLensModel)
class CameraLensModelAdmin(admin.ModelAdmin):
    pass
