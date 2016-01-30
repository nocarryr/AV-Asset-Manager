from __future__ import unicode_literals
import sys
import datetime

from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible

from locations.models import Location
from assettypes import models as asset_models
from assettags.models import AssetTaggedMixin

PY2 = sys.version_info.major == 2

class Asset(models.Model):
    temp_in_use = models.BooleanField(default=True)
    retired = models.BooleanField(default=False)
    notes = models.TextField(null=True)
    date_acquired = models.DateTimeField(blank=True, null=True)

@python_2_unicode_compatible
class AssetBase(Asset, AssetTaggedMixin):
    location = models.ForeignKey(Location)
    class Meta:
        abstract = True
    @classmethod
    def iter_subclasses(cls):
        def is_abstract(_cls):
            return getattr(_cls._meta, 'abstract', False)
        if not is_abstract(cls):
            yield cls
        for subcls in cls.__subclasses__():
            for _cls in subcls.iter_subclasses():
                yield _cls
    @classmethod
    def connect_post_save(cls):
        for cls in AssetBase.iter_subclasses():
            post_save.connect(on_asset_base_post_save, sender=cls)
    def save(self, *args, **kwargs):
        if self.retired and self.in_use:
            self.in_use = False
        super(AssetBase, self).save(*args, **kwargs)
    def __str__(self):
        if PY2:
            return unicode(self.asset_model)
        return str(self.asset_model)

def on_asset_base_post_save(sender, **kwargs):
    if kwargs.get('raw'):
        return
    if not kwargs.get('created'):
        return
    obj = kwargs.get('instance')
    if obj.date_acquired is None:
        obj.date_acquired = timezone.now()
        obj.save()

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
