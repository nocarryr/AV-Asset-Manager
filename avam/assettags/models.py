from __future__ import unicode_literals

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import python_2_unicode_compatible

from assettags import tag_handler

class AssetTagError(Exception):
    def __init__(self, msg, asset_tag=None):
        self.msg = msg
        self.asset_tag = asset_tag
    def __str__(self):
        s = self.msg
        if self.asset_tag is not None:
            s = '%s (asset_tag=%s)' % (s, self.asset_tag)
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
    
@python_2_unicode_compatible
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
    def __str__(self):
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


@python_2_unicode_compatible
class AssetTagImageTemplate(models.Model):
    name = models.CharField(max_length=30, unique=True)
    width = models.IntegerField()
    height = models.IntegerField()
    header_text = models.CharField(max_length=100, blank=True, null=True)
    qr_code_size = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        help_text='Size of the QR Code. (Can be in percent "%") Leave blank for "auto"',
    )
    location_choices = (
        ('a', 'Above'),
        ('b', 'Below'),
        ('n', 'None'),
    )
    code_text_location = models.CharField(
        max_length=1,
        choices=location_choices,
        default='b',
    )
    @classmethod
    def get_default_template(cls):
        try:
            obj = cls.objects.get(name='default')
        except cls.DoesNotExist:
            obj = None
        if obj is None:
            obj = cls(name='default', width=200, height=100)
            obj.save()
        return obj
    def __str__(self):
        return self.name

class Box(object):
    def __init__(self, **kwargs):
        self.x = kwargs.get('x', 0.)
        self.y = kwargs.get('y', 0.)
        self.w = kwargs.get('w')
        self.h = kwargs.get('h')
    @property
    def right(self):
        return self.x + self.w
    @property
    def bottom(self):
        return self.y + self.h
    def __mul__(self, other):
        keys = ['x', 'y', 'w', 'h']
        kwargs = {k:getattr(self, k) * other for k in keys}
        return Box(**kwargs)
    def __imul__(self, other):
        self.x *= other
        self.y *= other
        self.w *= other
        self.h *= other
        return self
    def __repr__(self):
        return 'Box %s' % (self)
    def __str__(self):
        return str([getattr(self, k) for k in ['x', 'y', 'w', 'h']])


@python_2_unicode_compatible
class PaperFormat(models.Model):
    name = models.CharField(max_length=30, unique=True)
    width = models.FloatField(default=8.5, help_text='Page Width (inches)')
    height = models.FloatField(default=11.0, help_text='Page Height (inches')
    top_margin = models.FloatField(default=0.5)
    bottom_margin = models.FloatField(default=0.5)
    left_margin = models.FloatField(default=0.2)
    right_margin = models.FloatField(default=0.2)
    def __str__(self):
        return self.name
    
@python_2_unicode_compatible
class AssetTagPrintTemplate(models.Model):
    name = models.CharField(max_length=30, unique=True)
    paper_format = models.ForeignKey(PaperFormat)
    asset_tag_template = models.ForeignKey(AssetTagImageTemplate)
    dpi = models.FloatField(default=300.0, help_text='Dots per inch')
    columns_per_row = models.IntegerField()
    column_spacing = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        help_text='Space between columns. Can be pixels (px) or inches (in, "). Leave blank for no spacing',
    )
    rows_per_page = models.IntegerField()
    row_spacing = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        help_text='Space between rows. Can be pixels (px) or inches (in, "). Leave blank for no spacing',
    )
    def get_spacing(self):
        dpi = self.dpi
        def parse(s):
            if not s:
                return 0.
            val = None
            units = ['in', '"']
            for unit in units:
                if unit in s.lower():
                    val = float(s.lower().split(unit)[0])
                    break
            if val is not None:
                return val / dpi
            if 'px' in s.lower():
                s = s.lower().split('px')[0]
            return float(s)
        d = {}
        for attr in ['column_spacing', 'row_spacing']:
            val = parse(getattr(self, attr))
            d[attr] = val
        return d
    def __str__(self):
        return self.name
