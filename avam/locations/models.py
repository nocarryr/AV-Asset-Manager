
from django.db import models


class Building(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name
    

class Room(models.Model):
    name = models.CharField(max_length=100)
    building = models.ForeignKey(
        Building,
        related_name='rooms',
        on_delete=models.CASCADE,
    )
    class Meta:
        unique_together = ('building', 'name')
    def __str__(self):
        return '{0} > {1}'.format(self.building, self.name)
    

class Location(models.Model):
    name = models.CharField(max_length=100)
    room = models.ForeignKey(
        Room,
        related_name='locations',
        on_delete=models.CASCADE,
    )
    class Meta:
        unique_together = ('room', 'name')
    def __str__(self):
        return '{0} > {1}'.format(self.room, self.name)
