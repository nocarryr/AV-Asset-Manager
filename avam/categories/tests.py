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
                print(category)
                if next_name is not None:
                    build_children(next_name, category)
        build_children()
    def test_str(self):
        root = Category.objects.get(name='root_1')
        branch = root.subcategories.get(name='branch_1')
        leaf = branch.subcategories.get(name='leaf_1')
        self.assertEqual(str(leaf), 'root_1/branch_1/leaf_1')
    def test_uniques(self):
        root = Category.objects.get(name='root_1')
        with self.assertRaises(IntegrityError):
            bad_branch = Category(name='branch_1', parent_category=root)
            bad_branch.save()
