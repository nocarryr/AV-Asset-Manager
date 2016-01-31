from __future__ import unicode_literals
import sys
import datetime

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible

from locations.models import Location
from assettypes import models as asset_models
from assettags.models import AssetTaggedMixin

PY2 = sys.version_info.major == 2

class Asset(models.Model, AssetTaggedMixin):
    in_use = models.BooleanField(default=True)
    retired = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)
    date_acquired = models.DateTimeField(blank=True, null=True)
    @property
    def asset_instance(self):
        obj = getattr(self, '_asset_instance', None)
        if obj is None:
            obj = self._asset_instance = self.get_asset_instance()
        return obj
    def get_asset_instance(self):
        if self.__class__ is not Asset:
            return self
        for rel in self._meta.related_objects:
            try:
                obj = getattr(self, rel.name)
            except ObjectDoesNotExist:
                obj = None
            if obj is not None:
                return obj
    def save(self, *args, **kwargs):
        if self.retired and self.in_use:
            self.in_use = False
        super(Asset, self).save(*args, **kwargs)

@receiver(post_save, sender=Asset)
def on_asset_base_post_save(sender, **kwargs):
    if kwargs.get('raw'):
        return
    if not kwargs.get('created'):
        return
    obj = kwargs.get('instance')
    if obj.date_acquired is None:
        obj.date_acquired = timezone.now()
        obj.save()

@python_2_unicode_compatible
class AssetBase(Asset):
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
    def __str__(self):
        return '{0} ({1})'.format(self.asset_model, self.location)

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
