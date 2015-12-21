from __future__ import unicode_literals

from django.db import models

class Building(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __unicode__(self):
        return self.name
    
class Room(models.Model):
    name = models.CharField(max_length=100)
    building = models.ForeignKey(Building, related_name='rooms')
    class Meta:
        unique_together = ('building', 'name')
    def __unicode__(self):
        return self.name
    
class Location(models.Model):
    name = models.CharField(max_length=100)
    room = models.ForeignKey(Room, related_name='locations')
    class Meta:
        unique_together = ('room', 'name')
    def __unicode__(self):
        return self.name
