from __future__ import unicode_literals
import datetime

from django.db import models

from locations.models import Location
from assettypes import models as asset_models

class AssetBase(models.Model):
    location = models.ForeignKey(Location)
    in_use = models.BooleanField(default=True)
    retired = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    date_acquired = models.DateTimeField(auto_now_add=True, editable=True)
    class Meta:
        abstract = True
    def save(self, *args, **kwargs):
        if self.retired and self.in_use:
            self.in_use = False
        super(AssetBase, self).save(*args, **kwargs)
    def __unicode__(self):
        return unicode(self.asset_model)

class LifeTrackedAsset(AssetBase):
    current_usage = models.DurationField(default=datetime.timedelta())
    expected_life = models.DurationField(blank=True, null=True)
    class Meta:
        abstract = True
    def save(self, *args, **kwargs):
        if self.expected_life is None:
            m = self.asset_model
            if hasattr(m, 'max_hours'):
                self.expected_life = datetime.timedelta(hours=m.max_hours)
            else:
                for attr in ['max_life', 'expected_life']:
                    if hasattr(m, attr):
                        self.expected_life = getattr(m, attr)
                        break
        super(LifeTrackedAsset, self).save(*args, **kwargs)

class Installable(models.Model):
    class Meta:
        abstract = True

class GenericAsset(AssetBase):
    asset_model = models.ForeignKey(
        asset_models.GenericModel,
        related_name='assets',
    )

class GenericAccessory(AssetBase):
    asset_model = models.ForeignKey(
        asset_models.GenericAccessoryModel,
        related_name='assets',
    )
    
class LampBase(LifeTrackedAsset, Installable):
    class Meta:
        abstract = True

class FilterBase(LifeTrackedAsset, Installable):
    class Meta:
        abstract = True

class Projector(AssetBase):
    asset_model = models.ForeignKey(
        asset_models.ProjectorModel,
        related_name='assets',
    )

class ProjectorLamp(LampBase):
    asset_model = models.ForeignKey(
        asset_models.ProjectorLampModel,
        related_name='assets',
    )
    installed_in = models.ForeignKey(Projector,
        related_name='lamps',
        blank=True,
        null=True,
    )

class ProjectorFilter(FilterBase):
    asset_model = models.ForeignKey(
        asset_models.ProjectorFilterModel,
        related_name='assets',
    )
    installed_in = models.ForeignKey(Projector,
        related_name='filters',
        blank=True,
        null=True,
    )

class MovingLight(AssetBase):
    asset_model = models.ForeignKey(
        asset_models.MovingLightModel,
        related_name='assets',
    )

class MovingLightLamp(LampBase):
    asset_model = models.ForeignKey(
        asset_models.MovingLightLampModel,
        related_name='assets',
    )
    installed_in = models.ForeignKey(
        MovingLight,
        related_name='lamps',
        blank=True,
        null=True,
    )

class LEDLight(AssetBase):
    asset_model = models.ForeignKey(
        asset_models.LEDLightModel,
        related_name='assets',
    )
