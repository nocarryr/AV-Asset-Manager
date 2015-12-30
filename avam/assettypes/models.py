from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Manufacturer(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name
    
@python_2_unicode_compatible
class ModelBase(models.Model):
    model_name = models.CharField(max_length=100)
    manufacturer = models.ForeignKey(Manufacturer)
    other_accessories = models.ManyToManyField('assettypes.GenericAccessoryModel', blank=True)
    class Meta:
        unique_together = ('manufacturer', 'model_name')
        abstract = True
    def __str__(self):
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
    
class LampModelBase(AccessoryModel):
    max_hours = models.PositiveIntegerField()
    class Meta:
        abstract = True

class FilterModelBase(AccessoryModel):
    filter_type_choices = (
        ('w', 'Washable'),
        ('c', 'Cartridge'),
        ('s', 'Scrolling'),
    )
    filter_type = models.CharField(max_length=1, choices=filter_type_choices)
    max_hours = models.PositiveIntegerField(blank=True, null=True)
    replaceable = models.BooleanField(default=False)
    class Meta:
        abstract = True

class ProjectorLampModel(LampModelBase):
    pass

class ProjectorFilterModel(FilterModelBase):
    pass

class ProjectorModel(ModelBase):
    lamp_count = models.PositiveIntegerField(default=1)
    lamp_type = models.ForeignKey(ProjectorLampModel)
    filter_type = models.ForeignKey(ProjectorFilterModel, blank=True, null=True)

class MovingLightLampModel(LampModelBase):
    pass

class MovingLightModel(LightingModelBase):
    lamp_type = models.ForeignKey(MovingLightLampModel)

class LEDLightModel(LightingModelBase):
    pass
