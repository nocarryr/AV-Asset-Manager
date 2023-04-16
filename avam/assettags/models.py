
from django.urls import reverse
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from assettags import tag_handler
from assettags.units import Unit, Inch, Pixel

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
    def get_asset_url(self):
        asset = self.content_object
        if asset is None:
            return None
        try:
            url = asset.get_absolute_url()
        except AttributeError:
            url = None
        return url
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
    def url_for_assign_view(self):
        content_type = ContentType.objects.get_for_model(self)
        return reverse('assettags:asset_tag_assign', kwargs=dict(
            content_type_id=content_type.id,
            object_id=self.pk,
        ))



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
        ('l', 'Left'),
        ('r', 'Right'),
        ('n', 'None'),
    )
    header_text_location = models.CharField(
        max_length=1,
        choices=location_choices,
        default='a',
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
    @classmethod
    def get_resized(cls, template, **kwargs):
        w = kwargs.get('width', template.width)
        h = kwargs.get('height', template.height)
        if w == template.width and h == template.height:
            return template
        fnames = ['header_text', 'qr_code_size',
                  'header_text_location', 'code_text_location']
        qkwargs = {fname:getattr(template, fname) for fname in fnames}
        qkwargs.update(dict(width=w, height=h))
        q = cls.objects.filter(**qkwargs)
        if q.exists():
            return q.first()
        name_fmt = 'Auto created from "%(name)s" (%(i)s)'
        d = {'name':template.name, 'i':0}
        name = name_fmt % d
        while cls.objects.filter(name=name).exists():
            d['i'] += 1
            name = name_fmt % d
        qkwargs['name'] = name
        new_template = cls(**qkwargs)
        new_template.save()
        return new_template
    @property
    def calc_qr_size(self):
        size = getattr(self, '_calc_qr_size', None)
        if size is not None:
            return size
        size = self.qr_code_size
        if not size:
            size = '%spx' % (self.height * .75)
        self._calc_qr_size = size
        return size
    def __str__(self):
        return self.name

class Box(object):
    def __init__(self, **kwargs):
        self._dpi = kwargs.get('dpi')
        kwargs.setdefault('x', '0px')
        kwargs.setdefault('y', '0px')
        for key in ['x', 'y', 'w', 'h']:
            val = kwargs.get(key)
            if val is None:
                obj = Unit(0., dpi=self.dpi)
            elif isinstance(val, Unit):
                obj = val.copy()
            else:
                obj = Unit.unit_from_label(val, dpi=self.dpi)
            setattr(self, key, obj)
    @property
    def dpi(self):
        return self._dpi
    @dpi.setter
    def dpi(self, value):
        if value == self._dpi:
            return
        self._dpi = value
        for key in ['x', 'y', 'w', 'h']:
            obj = getattr(self, key)
            obj.dpi = value
    @property
    def right(self):
        return self.x + self.w
    @property
    def bottom(self):
        return self.y + self.h
    @property
    def center_x(self):
        return self.width / 2. + self.x
    @property
    def center_y(self):
        return self.height / 2. + self.y
    def __mul__(self, other):
        keys = ['x', 'y', 'w', 'h']
        kwargs = {k:getattr(self, k) * other for k in keys}
        kwargs.setdefault('dpi', self.dpi)
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



class PaperFormat(models.Model):
    name = models.CharField(max_length=30, unique=True)
    width = models.FloatField(default=8.5, help_text='Page Width (inches)')
    height = models.FloatField(default=11.0, help_text='Page Height (inches')
    top_margin = models.FloatField(default=0.5)
    bottom_margin = models.FloatField(default=0.5)
    left_margin = models.FloatField(default=0.2)
    right_margin = models.FloatField(default=0.2)
    def get_full_area(self, dpi=72):
        kwargs = dict(x=0., y=0., w=self.width, h=self.height)
        for key in kwargs.keys():
            kwargs[key] = '{}in'.format(kwargs[key])
        kwargs['dpi'] = dpi
        return Box(**kwargs)
    def get_printable_area(self, dpi=72):
        w = self.width
        h = self.height
        w -= self.left_margin + self.right_margin
        h -= self.top_margin + self.bottom_margin
        kwargs = dict(x=self.left_margin, y=self.top_margin, w=w, h=h)
        for key in kwargs.keys():
            kwargs[key] = '{}in'.format(kwargs[key])
        kwargs['dpi'] = dpi
        return Box(**kwargs)
    def __str__(self):
        return self.name


class AssetTagPrintTemplate(models.Model):
    name = models.CharField(max_length=30, unique=True)
    paper_format = models.ForeignKey(
        PaperFormat,
        on_delete=models.CASCADE,
    )
    asset_tag_template = models.ForeignKey(
        AssetTagImageTemplate,
        on_delete=models.CASCADE,
    )
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
    def get_spacing(self, dpi=None):
        if dpi is None:
            dpi = self.dpi
        def parse(s):
            if s is None:
                s = '0px'
            elif s.endswith('"'):
                s = s.rstrip('"')
                s = '{}in'.format(s)
            elif not s.endswith('px') and not s.endswith('in'):
                s = '{}px'.format(s)
            return Unit.unit_from_label(s, dpi)
        d = {}
        for attr in ['column_spacing', 'row_spacing']:
            val = parse(getattr(self, attr))
            d[attr] = val
        return d
    def get_full_area(self, dpi=None):
        if dpi is None:
            dpi = self.dpi
        box = self.paper_format.get_full_area(dpi)
        return box
    def get_printable_area(self, dpi=None):
        if dpi is None:
            dpi = self.dpi
        box = self.paper_format.get_printable_area(dpi)
        return box
    def get_html_padding(self, dpi=96):
        spacing = self.get_spacing(dpi)
        keymap = {
            'column_spacing':['left', 'right'],
            'row_spacing':['top', 'bottom'],
        }
        d = {}
        for spkey, padkeys in keymap.items():
            val = spacing[spkey] / 2.
            for padkey in padkeys:
                d[padkey] = val
        return d
    def iter_cells(self, dpi=None):
        full_box = self.get_printable_area(dpi)
        spacing = self.get_spacing(dpi)
        num_cols = self.columns_per_row
        col_gaps = num_cols - 1
        col_size = full_box.w / num_cols
        if spacing['column_spacing'] > 0:
            col_size -= col_gaps * spacing['column_spacing'] / num_cols
        num_rows = self.rows_per_page
        row_gaps = num_rows - 1
        row_size = full_box.h / num_rows
        if spacing['row_spacing'] > 0:
            row_size -= row_gaps * spacing['row_spacing'] / num_rows
        y = full_box.y
        for r in range(num_rows):
            last_col = None
            for c in range(num_cols):
                if last_col is not None:
                    x = last_col.right + spacing['column_spacing']
                else:
                    x = full_box.x
                last_col = Box(x=x, y=y, w=col_size, h=row_size, dpi=dpi)
                yield last_col
            y += row_size + spacing['row_spacing']
    def get_cells(self, dpi=None):
        return [cell for cell in self.iter_cells(dpi)]
    def iter_page_row_col(self, asset_tags=None, full_page=True):
        rows = self.rows_per_page
        cols = self.columns_per_row
        if asset_tags is not None:
            if hasattr(asset_tags, 'iterator'):
                tag_iter = asset_tags.iterator()
            else:
                tag_iter = asset_tags
        else:
            tag_iter = range(rows * cols)
        if isinstance(tag_iter, list):
            tag_iter = iter(tag_iter)
        tag = None
        page = 0
        while tag is not False:
            for row in range(rows):
                for col in range(cols):
                    try:
                        tag = next(tag_iter)
                    except StopIteration:
                        if full_page:
                            tag = None
                        else:
                            tag = False
                            break
                    if asset_tags is not None:
                        yield page, row, col, tag
                    else:
                        yield page, row, col
                if tag is False:
                    break
            if tag is None:
                tag = False
            page += 1
    def iter_page_row_col_cell(self, asset_tags=None, full_page=True, dpi=None):
        cell_iter = self.iter_cells(dpi)
        last_page = 0
        for t in self.iter_page_row_col(asset_tags, full_page):
            page = t[0]
            if page > last_page:
                cell_iter = self.iter_cells(dpi)
                last_page = page
            cell = next(cell_iter)
            if asset_tags is not None:
                page, row, col, tag = t
                yield page, row, col, tag, cell
            else:
                page, row, col = t
                yield page, row, col, cell

    def __str__(self):
        return self.name
