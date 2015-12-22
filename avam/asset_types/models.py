from __future__ import unicode_literals

from django.db import models

class Manufacturer(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __unicode__(self):
        return self.name
    
class ModelBase(models.Model):
    model_name = models.CharField(max_length=100)
    manufacturer = models.ForeignKey(Manufacturer)
    other_accessories = models.ManyToManyField('asset_types.GenericAccessoryModel', blank=True)
    class Meta:
        unique_together = ('manufacturer', 'model_name')
        abstract = True
    def __unicode__(self):
        return self.model_name
    
class AccessoryModel(ModelBase):
    class Meta:
        abstract = True

class LightingModelBase(ModelBase):
    class Meta:
        abstract = True
    
class GenericModel(ModelBase):
    pass
    
class GenericAccessoryModel(AccessoryModel):
    pass
    
class LampModel(AccessoryModel):
    max_hours = models.PositiveIntegerField()

class FilterModel(AccessoryModel):
    filter_type_choices = (
        ('w', 'Washable'),
        ('c', 'Cartridge'),
        ('s', 'Scrolling'),
    )
    filter_type = models.CharField(max_length=1, choices=filter_type_choices)
    max_hours = models.PositiveIntegerField(blank=True, null=True)
    replaceable = models.BooleanField(default=False)

class ProjectorModel(ModelBase):
    lamp_count = models.PositiveIntegerField(default=1)
    lamp_type = models.ForeignKey(LampModel)
    filter_type = models.ForeignKey(FilterModel, blank=True, null=True)

class MovingLightModel(LightingModelBase):
    lamp_type = models.ForeignKey(LampModel)

class LEDLightModel(LightingModelBase):
    pass
