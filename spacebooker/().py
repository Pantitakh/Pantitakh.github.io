# coding: utf-8
from app_room.models import Room
Room.objects.filter(building__isnull=True).update(building='Pienvichit')
print(Room.objects.filter(building__isnull=True).count())
