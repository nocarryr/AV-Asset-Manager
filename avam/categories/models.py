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
    class Meta:
        unique_together = ('parent_category', 'name')
    def add_item(self, instance):
        item = CategoryItem(category=self, content_object=instance)
        item.save()
    def walk_subcategories(self):
        for category in self.subcategories.all():
            yield category
            for sub_category in category.walk_subcategories():
                yield sub_category
    def is_ancestor(self, category):
        if not isinstance(category, Category):
            return False
        parent = self.parent_category
        if parent is None:
            return False
        if parent == category:
            return True
        return parent.is_ancestor(category)
    def get_items(self, queryset=None):
        if queryset is None:
            queryset = CategoryItem.objects.all()
        queryset = queryset.filter(category=self)
        return queryset
    def get_all_items(self, queryset=None):
        if queryset is None:
            queryset = CategoryItem.objects.all()
        ids = set(self.pk)
        for category in self.walk_subcategories():
            ids.add(category.pk)
        queryset = queryset.filter(id__in=ids)
        return queryset
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
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    class Meta:
        unique_together = ('category', 'content_type', 'object_id')

class CategorizedMixin(object):
    def get_current_categories(self):
        content_type = ContentType.objects.get_for_model(self._meta.model)
        q = Category.objects.filter(
            items__content_type=content_type,
            items__object_id=self.pk,
        )
        return q
    def get_category_choices(self):
        return Category.objects.all()
    def add_category(self, **kwargs):
        category, created = Category.objects.get_or_create(**kwargs)
        self.add_to_category(category)
    def add_to_category(self, category):
        category.add_item(self)
