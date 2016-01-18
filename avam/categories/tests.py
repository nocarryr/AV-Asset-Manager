from django.test import TestCase
from django.db import IntegrityError

from categories.models import Category

class CategoriesTestCase(TestCase):
    def setUp(self):
        base_names = ['root', 'branch', 'leaf']
        for i in range(3):
            parent = None
            for base_name in base_names:
                name = '{0}_{1}'.format(base_name, i)
                category = Category(name=name, parent_category=parent)
                category.save()
                parent = category
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
