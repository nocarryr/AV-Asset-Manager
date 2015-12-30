from django.test import TestCase

from locations.models import Building, Room, Location

def build_test_fixtures():
    building = Building.objects.create(name='Test Building')
    room = Room.objects.create(name='Test Room', building=building)
    location = Location.objects.create(name='Test Location', room=room)
    return dict(building=building, room=room, location=location)

class LocationsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        fixtures = build_test_fixtures()
        for key, val in fixtures.items():
            setattr(cls, key, val)
