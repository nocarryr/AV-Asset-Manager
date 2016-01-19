from django.test import TestCase

from assettypes.models import (
    Manufacturer,
    ProjectorLampModel,
    ProjectorFilterModel,
    ProjectorModel,
    MovingLightLampModel,
    MovingLightModel,
    LEDLightModel,
)

def build_test_fixtures():
    manuf = Manufacturer.objects.create(name='Test Manufacturer')
    lamp = ProjectorLampModel.objects.create(
        manufacturer=manuf,
        model_name='Test Projector Lamp',
        max_hours=2000,
    )
    filt = ProjectorFilterModel.objects.create(
        manufacturer=manuf,
        model_name='Test Projector Filter',
        filter_type='c',
        max_hours=12000,
        replaceable=True,
    )
    proj = ProjectorModel.objects.create(
        manufacturer=manuf,
        model_name='Test Projector',
        lamp_count=2,
        lamp_type=lamp,
        filter_type=filt,
    )
    lighting_manuf = Manufacturer.objects.create(name='Lighting Manufacturer')
    mover_lamp = MovingLightLampModel.objects.create(
        manufacturer=lighting_manuf,
        model_name='Test MovingLight Lamp',
        max_hours=2000,
    )
    mover = MovingLightModel.objects.create(
        manufacturer=lighting_manuf,
        model_name='Test MovingLight',
        lamp_type=mover_lamp,
    )
    led_fixture = LEDLightModel.objects.create(
        manufacturer=lighting_manuf,
        model_name='Test LED',
    )
    d = dict(
        projector=proj, lamp=lamp, filter=filt, manufacturer=manuf,
        lighting_manuf=lighting_manuf, mover_lamp=mover_lamp,
        mover=mover, led_fixture=led_fixture,
    )
    return d

class AssetTypesTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        fixtures = build_test_fixtures()
        for key, val in fixtures.items():
            setattr(cls, key, val)
