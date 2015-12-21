from django.contrib import admin

from locations.models import Building, Room, Location

@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    pass

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    pass

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    pass
