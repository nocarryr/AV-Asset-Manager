from django.test import TestCase

from assets.models import (
    ProjectorLamp,
    ProjectorFilter,
    Projector,
)

from assettypes.tests import build_test_fixtures as build_assettypes_fixures
from locations.tests import build_test_fixtures as build_locations_fixtures

def build_test_fixtures():
    assettype_fixtures = build_assettypes_fixures()
    location_fixtures = build_locations_fixtures()
    location = location_fixtures['location']
    proj = Projector.objects.create(
        asset_model=assettype_fixtures['projector'],
        location=location,
    )
    lamps = []
    for i in range(proj.asset_model.lamp_count):
        lamps.append(ProjectorLamp.objects.create(
            asset_model=assettype_fixtures['lamp'],
            location=location,
            installed_in=proj,
        ))
    filter = ProjectorFilter.objects.create(
        asset_model=assettype_fixtures['filter'],
        location=location,
        installed_in=proj,
    )
    return dict(projector=proj, lamp1=lamps[0], lamp2=lamps[1], filter=filter)

class AssetsTestCase(TestCase):
    def setUp(self):
        fixtures = build_test_fixtures()
        for key, val in fixtures.items():
            setattr(self, key, val)
