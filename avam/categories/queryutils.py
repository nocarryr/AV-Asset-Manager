from django.db import models
from django.contrib.contenttypes.models import ContentType

class GenericFKQuerySet(models.query.QuerySet):
    def _filter_or_exclude(self, negate, *args, **kwargs):
        content_object = kwargs.pop('content_object', None)
        if content_object is not None:
            m = content_object._meta.model
            content_type = ContentType.objects.get_for_model(m)
            kwargs.update(dict(
                content_type=content_type,
                object_id=content_object.pk,
            ))
        return super(GenericFKQuerySet, self)._filter_or_exclude(negate, *args, **kwargs)

class GenericFKManager(models.Manager):
    def get_queryset(self):
        return GenericFKQuerySet(model=self.model, using=self._db, hints=self._hints)
