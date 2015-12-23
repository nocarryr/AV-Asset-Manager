from __future__ import unicode_literals

import datetime

from django.conf import settings
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

def iter_fields(obj, query_lookup=None):
    m = obj._meta
    for f in m.get_fields():
        if query_lookup is None:
            fname = f.name
        else:
            fname = '__'.join([query_lookup, f.name])
        if f.is_relation:
            content_type = ContentType.objects.get_for_model(f.related_model)
            watched = WatchedModel.objects.filter(content_type=content_type).exists()
            if f.many_to_many or f.one_to_many:
                for _obj in getattr(obj, f.name).all():
                    if False:#not watched:
                        yield iter_fields(_obj, fname)
                    else:
                        yield m, fname, f, _obj.pk
            else:
                if False:#watched:
                    yield iter_fields(getattr(obj, f.name), fname)
                else:
                    yield m, fname, f, getattr(obj, f.name).pk
        else:
            yield m, fname, f, getattr(obj, f.name)
    
def get_query_value(obj, query_lookup):
    if '__' not in query_lookup:
        return getattr(obj, query_lookup)
    attr = query_lookup.split('__')[0]
    query_lookup = '__'.join(query_lookup.split('__')[1:])
    return get_query_value(getattr(obj, attr), query_lookup)

class WatchedModel(models.Model):
    content_type = models.ForeignKey(ContentType)
    def __unicode__(self):
        return self.content_type.name
    
def add_model_history(*models):
    for m in models:
        content_type = ContentType.objects.get_for_model(m)
        if WatchedModel.objects.filter(content_type=content_type).exists():
            continue
        wm = WatchedModel(content_type=content_type)
        wm.save()
    
class ObjectUpdate(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    datetime = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
    def get_previous(self):
        q = self._meta.model.objects.filter(content_object=self.content_object)
        q = q.filter(datetime__lt=self.datetime)
        if not q.exists():
            return None
        return q.latest('datetime')
    def get_all_fields(self):
        instance = self.content_object
        fields = {}
        for m, fname, f, value in iter_fields(instance):
            try:
                obj_change = self.changes.get(field_name=fname)
            except ObjectChange.DoesNotExist:
                obj_change = None
            if obj_change is None:
                prev_update = self.get_previous()
                while prev_update is not None:
                    try:
                        obj_change = prev_update.changes.get(field_name=fname)
                    except ObjectChange.DoesNotExist:
                        prev_update = self.get_previous()
            if obj_change is not None:
                fields[fname] = {'value':obj_change.get_value()}
            else:
                fields[fname] = {'value':value, 'created':True}
        return fields
    def save(self, *args, **kwargs):
        created = self.pk is None
        super(ObjectUpdate, self).save(*args, **kwargs)
        if created:
            ObjectChange.find_changes(self)

PY_TYPES = dict(
    int=int,
    str=str,
    unicode=unicode,
    float=float,
    bool=bool,
    NoneType=None,
)

def str_to_value(s, py_type):
    if 'datetime' in py_type:
        dtcls = py_type.split('.')
        if dtcls == 'datetime':
            dt_fmt = '%Y-%m-%d %H:%M:%S.f+00:00'
            dt = datetime.datetime.strptime(s, dt_fmt)
            value = timezone.utc.localize(dt)
        elif dtcls == 'time':
            if '.' in s:
                s = ':'.join(s.split('.'))
            args = [int(arg) for arg in s.split(':')]
            value = datetime.time(*args)
        elif dtcls == 'date':
            args = [int(arg) for arg in s.split('-')]
            value = datetime.date(*args)
        elif dtcls == 'timedelta':
            value = datetime.timedelta(float(s))
    else:
        py_type = PY_TYPES.get(py_type)
        if py_type is None:
            value = None
        else:
            value = py_type(s)
    return value

def value_to_str(value):
    if isinstance(value, datetime.timedelta):
        value = value.total_seconds()
    return unicode(value)

class ObjectChange(models.Model):
    update = models.ForeignKey(ObjectUpdate, related_name='changes')
    field_name = models.CharField(max_length=100)
    py_type = models.CharField(max_length=100)
    str_value = models.CharField(max_length=300)
    @classmethod
    def find_changes(cls, object_update):
        instance = object_update.content_object
        prev_update = object_update.get_previous()
        for fname, fdata in prev_update.get_all_fields():
            if fdata.get('created'):
                obj_change = cls(
                    update=object_update,
                    field_name=fname,
                    py_type=type(fdata['value']),
                    str_value=value_to_str(fdata['value']),
                )
                obj_change.save()
                continue
            current_val = get_query_value(instance, fname)
            if current_val != fdata['value']:
                obj_change = cls(
                    update=object_update,
                    field_name=fname,
                    py_type=type(current_val),
                    str_value=value_to_str(current_val),
                )
                obj_change.save()
    def get_value(self):
        return str_to_value(self.str_value, self.py_type)

    
