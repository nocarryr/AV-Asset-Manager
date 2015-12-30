from django.test import TestCase

from assettags.models import AssetTagError, AssetTag

from assets.tests import build_test_fixtures as build_asset_fixtures

def build_test_fixtures():
    asset_fixtures = build_asset_fixtures()
    codes = AssetTag.objects.generate_tags(len(asset_fixtures))
    asset_tags = AssetTag.objects.filter(code__in=codes)
    return dict(assets=asset_fixtures, asset_tags=asset_tags)

class AssetTagsTestCase(TestCase):
    def setUp(self):
        fixtures = build_test_fixtures()
        for key, val in fixtures.items():
            setattr(self, key, val)
    def assign_assets(self):
        for key, asset in self.assets.items():
            asset_tag = AssetTag.objects.filter(object_id__isnull=True).first()
            asset_tag.assign_asset(asset)
            yield asset_tag, asset
    def test_assignment(self):
        for asset_tag, asset in self.assign_assets():
            self.assertEqual(asset_tag.content_object, asset)
    def test_validation1(self):
        msg_fmt = 'Cannot assign tag to %s.  This tag is already assigned. (asset_tag=%s)'
        for assigned_tag, asset in self.assign_assets():
            assigned_tag.refresh_from_db()
            asset.refresh_from_db()
            self.assertEqual(AssetTag.objects.get_for_object(asset), assigned_tag)
            q = AssetTag.objects.exclude(code=assigned_tag.code, object_id__isnull=True)
            if not q.exists():
                break
            other_tag = q.first()
            msg = msg_fmt % (asset, other_tag)
            self.assertRaisesMessage(AssetTagError, msg, other_tag.assign_asset, asset)
    def test_validation2(self):
        msg_fmt = 'Asset %s is already assigned to another tag. (asset_tag=%s)'
        for assigned_tag, asset in self.assign_assets():
            codes = AssetTag.objects.generate_tags()
            unassigned_tag = AssetTag.objects.get(code=codes.pop())
            msg = msg_fmt % (asset, assigned_tag)
            self.assertRaisesMessage(AssetTagError, msg, unassigned_tag.assign_asset, asset)
        
