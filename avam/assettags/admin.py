from django.contrib import admin

from assettags.models import (
    AssetTagImageTemplate,
    PaperFormat,
    AssetTagPrintTemplate,
)

@admin.register(AssetTagImageTemplate)
class AssetTagImageTemplateAdmin(admin.ModelAdmin):
    pass

@admin.register(PaperFormat)
class PaperFormatAdmin(admin.ModelAdmin):
    pass

@admin.register(AssetTagPrintTemplate)
class AssetTagPrintTemplateAdmin(admin.ModelAdmin):
    pass
