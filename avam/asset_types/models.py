from __future__ import unicode_literals

from django.db import models

class Manufacturer(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __unicode__(self):
        return self.name
    
class ModelType(models.Model):
    name = models.CharField(max_length=100)
    manufacturer = models.ForeignKey(Manufacturer, related_name='models')
    class Meta:
        unique_together = ('manufacturer', 'name')
    def __unicode__(self):
        return self.name
    
class AssetBase(models.Model):
    model_type = models.ForeignKey(ModelType)
    other_accessories = models.ManyToManyField('asset_types.GenericAccessory', blank=True)
    class Meta:
        abstract = True
    def __unicode__(self):
        return unicode(self.model_type)
    
class AccessoryAsset(AssetBase):
    class Meta:
        abstract = True

class LightingAssetBase(AssetBase):
    class Meta:
        abstract = True
    
class GenericAsset(AssetBase):
    pass
    
class GenericAccessory(AccessoryAsset):
    pass
    
class LampAsset(AccessoryAsset):
    max_hours = models.PositiveIntegerField()

class FilterAsset(AccessoryAsset):
    filter_type_choices = (
        ('w', 'Washable'),
        ('c', 'Cartridge'),
        ('s', 'Scrolling'),
    )
    filter_type = models.CharField(max_length=1, choices=filter_type_choices)
    max_hours = models.PositiveIntegerField(blank=True, null=True)
    replaceable = models.BooleanField(default=False)

class ProjectorAsset(AssetBase):
    lamp_count = models.PositiveIntegerField(default=1)
    lamp_type = models.ForeignKey(LampAsset)
    filter_type = models.ForeignKey(FilterAsset, blank=True, null=True)

class MovingLightAsset(LightingAssetBase):
    lamp_type = models.ForeignKey(LampAsset)

class LEDLightAsset(LightingAssetBase):
    pass
