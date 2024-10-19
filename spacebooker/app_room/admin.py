from django.contrib import admin
from app_room.models import Room
# Register your models here.
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'building', 'category', 'capacity', 'status']
    list_filter = ['building', 'category', 'status']
    search_fields = ['name', 'building']
    
admin.site.register(Room, RoomAdmin)