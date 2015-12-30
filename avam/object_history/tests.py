from django.test import TestCase

from object_history.models import WatchedModel, ObjectUpdate

from assets.tests import build_test_fixtures as build_asset_fixtures

class ObjectHistoryTestCase(TestCase):
    def setUp(self):
        self.assets = build_asset_fixtures()
    def rebuild_history(self):
        ObjectUpdate.objects.all().delete()
        for wm in WatchedModel.objects.all():
            m = wm.content_type.model_class()
            for obj in m.objects.all():
                obj_update = ObjectUpdate(content_object=obj)
                obj_update.save()
                obj.save()
    def get_object_update(self, obj):
        q = ObjectUpdate.objects.get_for_object(obj)
        return q.latest('datetime')
    def print_changes(self, obj):
        obj_update = self.get_object_update(obj)
        updates = obj_update.get_full_history()
        print('\n'.join(['\t'.join([str(v) for v in l]) for l in updates]))
    def check_reconstruction(self, obj):
        obj_update = self.get_object_update(obj)
        d = obj_update.reconstruct()
        for key, val in d['values'].items():
            obj_val = getattr(obj, key)
            f = obj._meta.get_field(key)
            if f.is_relation:
                if f.many_to_many or f.one_to_many:
                    vl = val.values_list('pk', flat=True)
                    for rel_val in obj_val.all():
                        self.assertIn(rel_val.pk, vl)
                    continue
            self.assertEqual(val, getattr(obj, key))
    def test1(self):
        if self.debug:
            print('test1')
            print('-'*60)
        self.rebuild_history()
        proj = self.assets['projector']
        if self.debug:
            self.print_changes(proj)
        self.check_reconstruction(proj)
    def test2(self):
        if self.debug:
            print('test2')
            print('-'*60)
        self.rebuild_history()
        proj = self.assets['projector']
        proj.notes = 'test 2'
        proj.save()
        if self.debug:
            self.print_changes(proj)
        obj_update = self.get_object_update(proj)
        q = obj_update.changes.all()
        self.assertEqual(q.count(), 1)
        change = q.first()
        self.assertEqual(change.field_name, 'notes')
        self.assertEqual(change.get_value(), proj.notes)
    
