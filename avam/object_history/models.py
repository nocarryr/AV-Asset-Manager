from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from object_history.utils import (
    iter_fields, get_query_value, value_to_str, str_to_value
)

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
    
class ObjectUpdateManager(models.Manager):
    def get_for_object(self, obj):
        q = self.get_queryset()
        if isinstance(obj, ObjectUpdate):
            q = q.filter(content_type=obj.content_type, object_id=obj.object_id)
        else:
            content_type = ContentType.objects.get_for_model(obj._meta.model)
            q = q.filter(content_type=content_type, object_id=obj.pk)
        return q

class ObjectUpdate(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    datetime = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
    objects = ObjectUpdateManager()
    class Meta:
        ordering = ['-datetime']
    def get_update_queryset(self, queryset=None, **kwargs):
        if queryset is None:
            queryset = self._meta.model.objects.get_for_object(self.content_object)
        queryset = queryset.filter(**kwargs)
        return queryset
    def get_previous(self):
        q = self._meta.model.objects.get_for_object(self.content_object)
        q = q.filter(datetime__lt=self.datetime)
        q = q.exclude(id=self.id)
        if not q.exists():
            return None
        return q.latest('datetime')
    def get_all_fields(self):
        instance = self.content_object
        fields = {}
        for m, fname, f, value in iter_fields(instance):
            obj_change = self.get_change(fname)
            if obj_change is not None:
                fields[fname] = {'value':obj_change.get_value(), 'stored':True}
            else:
                fields[fname] = {'value':value, 'created':True}
        return fields
    def get_change(self, field_name):
        try:
            obj_change = self.changes.get(field_name=field_name)
        except ObjectChange.DoesNotExist:
            obj_change = None
        if obj_change is not None:
            return obj_change
        else:
            prev_update = self.get_previous()
            if prev_update is not None:
                return prev_update.get_change(field_name)
        return None
    def get_field_value(self, field_name):
        obj_change = self.get_change(field_name)
        if obj_change is not None:
            return obj_change.get_value()
    def reconstruct(self):
        q = self._meta.model.objects.get_for_object(self.content_object)
        field_names = set(q.values_list('changes__field_name', flat=True))
        d = {'instance':self.content_object, 'updates':{}, 'values':{}}
        for fname in field_names:
            obj_change = self.get_change(fname)
            d['updates'][fname] = obj_change.update
            d['values'][fname] = obj_change.get_model_value()
        return d
    def save(self, *args, **kwargs):
        created = self.pk is None
        super(ObjectUpdate, self).save(*args, **kwargs)
        if created:
            ObjectChange.find_changes(self)
    def __unicode__(self):
        return u'%s: %s' % (self.content_object, self.datetime)


class ObjectChange(models.Model):
    update = models.ForeignKey(ObjectUpdate, related_name='changes')
    field_name = models.CharField(max_length=100)
    py_type = models.CharField(max_length=100)
    str_value = models.CharField(max_length=300)
    @classmethod
    def find_changes(cls, object_update):
        instance = object_update.content_object
        for fname, fdata in object_update.get_all_fields().items():
            if fdata.get('created'):
                py_type = str(type(fdata['value']))
                py_type = py_type.lstrip("<type '").rstrip("'>")
                obj_change = cls(
                    update=object_update,
                    field_name=fname,
                    py_type=py_type,
                    str_value=value_to_str(fdata['value']),
                )
                obj_change.save()
                continue
            current_val = get_query_value(instance, fname)
            py_type = str(type(current_val))
            py_type = py_type.lstrip("<type '").rstrip("'>")
            str_value = value_to_str(current_val)
            if str_value != value_to_str(fdata['value']):
                obj_change = cls(
                    update=object_update,
                    field_name=fname,
                    py_type=py_type,
                    str_value=str_value,
                )
                obj_change.save()
    @property
    def instance(self):
        instance = getattr(self, '_instance_object', None)
        if instance is None:
            instance = self._instance_object = self.update.content_object
        return instance
    @property
    def model_field(self):
        f = getattr(self, '_model_field', None)
        if f is None:
            instance = self.instance
            f = self._model_field = instance._meta.get_field(self.field_name)
        return f
    def get_value(self):
        return str_to_value(self.str_value, self.py_type)
    def get_model_value(self):
        f = self.model_field
        v = self.get_value()
        if f.is_relation:
            m = f.related_model
            return m.objects.get(pk=v)
        return v
    def __unicode__(self):
        return u' = '.join([self.field_name, self.str_value])

    
