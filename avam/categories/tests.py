from django.test import TestCase
from django.db import IntegrityError

from categories.models import Category

class CategoriesTestCase(TestCase):
    def setUp(self):
        base_names = ['root', 'branch', 'leaf']
        def build_children(base_name=None, parent=None):
            if base_name is None:
                base_name = base_names[0]
            try:
                next_name = base_names[base_names.index(base_name) + 1]
            except IndexError:
                next_name = None
            for i in range(3):
                name = '{0}_{1}'.format(base_name, i)
                category = Category(name=name, parent_category=parent)
                category.save()
                if next_name is not None:
                    build_children(next_name, category)
        build_children()
    def get_category(self, *args):
        category = None
        for name in args:
            if category is None:
                category = Category.objects.get(name=name)
            else:
                category = category.subcategories.get(name=name)
        return category
    def test_str(self):
        leaf = self.get_category('root_1', 'branch_1', 'leaf_1')
        self.assertEqual(str(leaf), 'root_1/branch_1/leaf_1')
    def test_uniques(self):
        root = self.get_category('root_1')
        with self.assertRaises(IntegrityError):
            bad_branch = Category(name='branch_1', parent_category=root)
            bad_branch.save()
    def test_walk(self):
        root = self.get_category('root_1')
        names = {'branches':[], 'leaves':[]}
        for sub_category in root.walk_subcategories():
            if 'branch' in sub_category.name:
                key = 'branches'
            else:
                key = 'leaves'
            names[key].append(int(sub_category.name.split('_')[1]))
        self.assertEqual(names, {'branches':[0, 1, 2], 'leaves':[0, 1, 2]*3})
    def test_ancestry(self):
        root = self.get_category('root_1')
        branch = self.get_category('root_1', 'branch_1')
        leaf = self.get_category('root_1', 'branch_1', 'leaf_1')
        not_root = self.get_category('root_0')
        self.assertTrue(leaf.is_ancestor(branch))
        self.assertTrue(leaf.is_ancestor(root))
        self.assertFalse(leaf.is_ancestor(not_root))

class CategoryItemTestCase(TestCase):
    def setUp(self):
        from assettypes.tests import build_test_fixtures as build_assettypes_fixures
        assettypes_fixtures = build_assettypes_fixures()
        category_fixtures = {}
        for name in ['Video', 'Lighting', 'Accessories']:
            category = Category.objects.create(name=name)
            category_fixtures[name] = category
            if name != 'Accessories':
                sub_category = Category.objects.create(
                    name='Accessories',
                    parent_category=category,
                )
                category_fixtures[str(sub_category)] = sub_category
        self.category_fixtures = category_fixtures
        self.assettypes_fixtures = assettypes_fixtures
    def get_fk_fields(self, obj):
        for field in obj._meta.get_fields():
            if not field.is_relation:
                continue
            if not field.one_to_many:
                continue
            yield field
    def assign_items(self):
        proj = self.assettypes_fixtures['projector']
        manuf = proj.manufacturer
        category = self.category_fixtures['Video']
        category.add_item(manuf)
        for f in self.get_fk_fields(manuf):
            if not hasattr(f.related_model, 'manufacturer'):
                continue
            attr = f.get_accessor_name()
            for obj in getattr(manuf, attr).all():
                category.add_item(obj)
    def test_assignment(self):
        self.assign_items()
        category = self.category_fixtures['Video']
        q = category.get_items()
        manuf = self.assettypes_fixtures['projector'].manufacturer
        for category_item in q:
            obj = category_item.content_object
            if obj._meta.model_name == 'manufacturer':
                continue
            self.assertEqual(obj.manufacturer, manuf)
