from __future__ import unicode_literals

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Category(models.Model):
    name = models.CharField(max_length=100)
    parent_category = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='subcategories',
    )
    def iter_parents(self, top_down=True):
        if top_down is False:
            yield self
        p = self.parent_category
        if p is not None:
            for obj in p.iter_parents(top_down):
                yield obj
        if top_down is True:
            yield self
    def __str__(self):
        return '/'.join([obj.name for obj in self.iter_parents()])

class CategoryItem(models.Model):
    category = models.ForeignKey(Category, related_name='items')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_object = GenericForeignKey('content_type', 'object_id')
