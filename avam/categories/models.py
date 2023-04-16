
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from categories.queryutils import GenericFKManager



class Category(models.Model):
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

class CategoryItemManager(GenericFKManager):
    def get_for_object(self, obj):
        queryset = self.get_queryset()
        return queryset.filter(content_object=obj)
    def get_for_objects(self, *objects):
        return self.filter(content_object__in=objects)

class CategoryItem(models.Model):
    category = models.ForeignKey(
        Category,
        related_name='items',
        on_delete=models.CASCADE,
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    objects = CategoryItemManager()
    class Meta:
        unique_together = ('category', 'content_type', 'object_id')

class CategorizedMixin(object):
    def add_model_category_defaults(self):
        """Adds an instance to any categories defined on its class and base classes
        
        Category definitions can be add with a class attribute :attr:`default_categories`
        as shown in the example below.
        ```
        class MyModel(models.Model):
            default_categories = [
                'some single category',
                ['some root category', 'some subcategory'],
            ]
        ```
        Or by extending/overriding the :meth:`CategorizedMixin.get_default_categories` method
        
        This would mostly be useful on either the :meth:`django.db.models.Model.save` method
        or in its :attr:`django.db.models.signals.post_save` handler.
        """
        for category_defs in self.get_default_categories():
            for category_def in category_defs:
                if isinstance(category_def, str):
                    category_def = [category_def]
                parent = None
                for name in category_def:
                    category = self.add_category(
                        name=name,
                        parent_category=parent,
                    )
                    parent = category
    @classmethod
    def get_default_categories(cls):
        def iter_bases(cls_):
            if cls_ is not object:
                yield cls_
                for cls__ in cls_.__bases__:
                    yield iter_bases(cls__)
        for _cls in iter_bases(cls):
            f = getattr(_cls, 'get_default_categories', None)
            if (hasattr(_cls, 'get_default_categories') and
                    _cls is not CategorizedMixin and
                    f.__func__.__module__ != 'categories.models'):
                yield _cls.get_default_categories()
            elif hasattr(_cls, 'default_categories'):
                yield _cls.default_categories
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
        return category
    def add_to_category(self, category):
        category.add_item(self)
