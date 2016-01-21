from __future__ import unicode_literals

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import python_2_unicode_compatible

from categories.queryutils import GenericFKManager

@python_2_unicode_compatible
class Category(models.Model):
    """Generic category definition that can hold references to Django `Model` instances.

    Categories can be nested by assigning the `Category.parent_category` field.
    Links can be made to other categories which will syncronize the
    related `Model` instances via the `Category.linked_categories` field.
    """
    name = models.CharField(max_length=100)
    parent_category = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='subcategories',
    )
    linked_categories = models.ManyToManyField(
        'self',
        symmetrical=False,
        blank=True,
    )
    class Meta:
        unique_together = ('parent_category', 'name')
    def add_item(self, instance):
        """Adds a `Model` instance as a member of the category.
        It will also be added to any linked categories defined.

        :param instance: the `Model` instance to be added to the category
        """
        CategoryItem.objects.get_or_create(category=self, content_object=instance)
    def add_item_to_links(self, instance):
        for linked_category in self.linked_categories.all():
            linked_category.add_item(instance)
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
        """Returns a `QuerySet` containing immediate members of the category
        using the `CategoryItem` model.
        """
        if queryset is None:
            queryset = CategoryItem.objects.all()
        queryset = queryset.filter(category=self)
        return queryset
    def get_all_items(self, queryset=None):
        """Returns a `QuerySet` containing members of the category and its
        subcategories using the `CategoryItem` model.
        """
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

class CategoryItemManager(GenericFKManager):
    def get_for_object(self, obj):
        queryset = self.get_queryset()
        return queryset.filter(content_object=obj)

class CategoryItem(models.Model):
    """A helper `Model` that stores the references to items in a `Category`.

    Uses the `contenttypes` framework and `GenericForeignKey` for references.
    """
    category = models.ForeignKey(Category, related_name='items')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    objects = CategoryItemManager()
    class Meta:
        unique_together = ('category', 'content_type', 'object_id')

class CategorizedMixin(object):
    """A mixin to add `Model` methods for `Category` integration
    """
    def get_current_categories(self):
        """Returns a `QuerySet` containing all `Category` items that a
        `Model` instance is a member of
        """
        content_type = ContentType.objects.get_for_model(self._meta.model)
        q = Category.objects.filter(
            items__content_type=content_type,
            items__object_id=self.pk,
        )
        return q
    def get_category_choices(self):
        """Returns all available `Category` items available as a `QuerySet`
        """
        return Category.objects.all()
    def add_category(self, **kwargs):
        """Adds the `Model` instance to a `Category`, creating one if necessary

        :param **kwargs: keyword arguments used to create or lookup the `Category`
            (passed directly to the `Manager.get_or_create` method)
        """
        category, created = Category.objects.get_or_create(**kwargs)
        self.add_to_category(category)
    def add_to_category(self, category):
        """Adds the `Model` instance to the given category

        :param category: the `Category` instance to add
        """
        category.add_item(self)
