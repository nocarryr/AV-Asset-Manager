from django.db import models
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType

class GenericFKQuerySet(models.query.QuerySet):
    def _filter_or_exclude_content_objects(self, negate, *content_objects):
        models = [obj._meta.model for obj in content_objects]
        content_types = ContentType.objects.get_for_models(*models)
        qexp = None
        for content_object, m in zip(content_objects, models):
            content_type=content_types[m]
            qkwargs = dict(content_type__id=content_type.pk, object_id=content_object.pk)
            if qexp is None:
                qexp = Q(**qkwargs)
            else:
                qexp = qexp | Q(**qkwargs)
        return qexp
    def _filter_or_exclude(self, negate, args, kwargs):
        args, kwargs = self._get_content_object_from_query_args(negate, args, kwargs)
        return super()._filter_or_exclude(negate, args, kwargs)

    def _filter_or_exclude_inplace(self, negate, args, kwargs):
        args, kwargs = self._get_content_object_from_query_args(negate, args, kwargs)
        return super()._filter_or_exclude_inplace(negate, args, kwargs)

    def _get_content_object_from_query_args(self, negate, args, kwargs):
        content_objects = kwargs.pop('content_object__in', [])
        content_object = kwargs.pop('content_object', None)
        if content_object is not None:
            content_objects = list(content_objects)
            content_objects.append(content_object)
        if len(content_objects):
            qexp = self._filter_or_exclude_content_objects(negate, *content_objects)
            args = list(args)
            args.append(qexp)
            args = tuple(args)
        return args, kwargs


class GenericFKManager(models.Manager):
    def get_queryset(self):
        return GenericFKQuerySet(model=self.model, using=self._db, hints=self._hints)
