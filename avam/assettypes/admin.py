from django.contrib import admin

import nested_admin

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
    LightingProfile,
    LightingProfileChannel,
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

class LightingProfileChannelInline(nested_admin.NestedStackedInline):
    model = LightingProfileChannel
    sortable_field_name = 'index'
    def __init__(self, parent_model, admin_site):
        parent_model = LightingProfile
        super(LightingProfileChannelInline, self).__init__(parent_model, admin_site)

class LightingProfileInline(nested_admin.NestedStackedInline):
    inlines = [LightingProfileChannelInline]

class MovingLightProfileInline(LightingProfileInline):
    model = MovingLightModel.profiles.through

class LEDLightProfileInline(LightingProfileInline):
    model = LEDLightModel.profiles.through

class LightingAdmin(nested_admin.NestedAdmin):
    pass

@admin.register(MovingLightModel)
class MovingLightModelAdmin(LightingAdmin):
    inlines = [MovingLightProfileInline]

@admin.register(LEDLightModel)
class LEDLightModelAdmin(LightingAdmin):
    inlines = [LEDLightProfileInline]

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
