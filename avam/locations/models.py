from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Building(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name
    
@python_2_unicode_compatible
class Room(models.Model):
    name = models.CharField(max_length=100)
    building = models.ForeignKey(Building, related_name='rooms')
    class Meta:
        unique_together = ('building', 'name')
    def __str__(self):
        return self.name
    
@python_2_unicode_compatible
class Location(models.Model):
    name = models.CharField(max_length=100)
    room = models.ForeignKey(Room, related_name='locations')
    class Meta:
        unique_together = ('room', 'name')
    def __str__(self):
        return self.name
