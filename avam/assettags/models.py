from __future__ import unicode_literals

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from assettags import tag_handler

class AssetTagError(Exception):
    def __init__(self, msg, asset_tag=None):
        self.msg = msg
        self.asset_tag = asset_tag
    def __str__(self):
        s = self.msg
        if self.asset_tag is not None:
            s = '%s (asset_tag=%s' % (s, self.asset_tag)
        return s

class AssetTagManager(models.Manager):
    def generate_tags(self, num_tags=1):
        q = self.get_queryset()
        codes = set()
        while len(codes) < num_tags:
            code = tag_handler.generate_code()
            while q.filter(code=code).exists() or code in codes:
                code = tag_handler.generate_code()
            codes.add(code)
        q.bulk_create([AssetTag(code=c) for c in codes])
        return codes
    def get_for_object(self, content_object):
        q = self.get_queryset()
        content_type = ContentType.objects.get_for_model(content_object._meta.model)
        return q.get(content_type=content_type, object_id=content_object.pk)
    def object_for_tag(self, asset_tag):
        if not isinstance(asset_tag, AssetTag):
            try:
                asset_tag = self.get(code=asset_tag)
            except AssetTag.DoesNotExist:
                return None
        return asset_tag.content_object
    
class AssetTag(models.Model):
    code = models.CharField(max_length=50, unique=True)
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    objects = AssetTagManager()
    class Meta:
        unique_together = ('content_type', 'object_id')
    def assign_asset(self, instance):
        if self.content_object is not None:
            raise AssetTagError(
                'Cannot assign tag to %s.  This tag is already assigned.' % (instance),
                self
            )
        try:
            other_tag = self._meta.model.objects.get_for_object(instance)
        except self._meta.model.DoesNotExist:
            other_tag = None
        if other_tag is not None and other_tag.pk != self.pk:
            raise AssetTagError(
                'Asset %s is already assigned to another tag.' % (instance),
                other_tag
            )
        self.content_object = instance
        self.save()
    def __unicode__(self):
        return self.code
    
class AssetTaggedMixin(object):
    @property
    def asset_tag(self):
        try:
            asset_tag = AssetTag.objects.get_for_object(self)
        except AssetTag.DoesNotExist:
            asset_tag = None
        return asset_tag
    def assign_asset_tag(self, asset_tag):
        if not isinstance(asset_tag, AssetTag):
            asset_tag, created = AssetTag.objects.get_or_create(code=asset_tag)
        asset_tag.assign_asset(self)
