import sys
from django.contrib import admin

from object_history.models import (
    WatchedModel,
    ObjectUpdate,
    ObjectChange,
)

PY2 = sys.version_info.major == 2

@admin.register(WatchedModel)
class WatchedModelAdmin(admin.ModelAdmin):
    pass

class ContentObjectFilter(admin.SimpleListFilter):
    title = 'content object'
    parameter_name = 'content_object'
    def lookups(self, request, model_admin):
        l = []
        q = ObjectUpdate.objects.all()
        ctypes = set(q.values_list('content_type__id', flat=True))
        for ctype in ctypes:
            _q = q.filter(content_type__id=ctype)
            obj_ids = set(_q.values_list('object_id', flat=True))
            for obj_id in obj_ids:
                qstr = '%s_%s' % (ctype, obj_id)
                object_update = q.filter(content_type__id=ctype, object_id=obj_id).first()
                if PY2:
                    lbl = unicode(object_update.content_object)
                else:
                    lbl = str(object_update.content_object)
                l.append((qstr, lbl))
        return l
    def queryset(self, request, queryset):
        v = self.value()
        if not v:
            return queryset
        ctype, obj_id = self.value().split('_')
        return queryset.filter(content_type__id=ctype, object_id=obj_id)

@admin.register(ObjectUpdate)
class ObjectUpdateAdmin(admin.ModelAdmin):
    list_display = [
        'content_type',
        'content_object',
        'datetime',
    ]
    list_filter = [
        'content_type',
        ContentObjectFilter,
    ]
    ordering = ['-datetime']

@admin.register(ObjectChange)
class ObjectChangeAdmin(admin.ModelAdmin):
    list_display = [
        'update',
        'field_name',
        'str_value',
        'py_type',
    ]
    list_filter = [
        'update',
    ]
    ordering = ['-update__datetime']
