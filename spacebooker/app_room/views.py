from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Room, ROOM_CATEGORIES
from django.conf import settings
from django.db.models import Case, When, Value, IntegerField, Q

def rooms(request):
    # Get all filter parameters
    search_query = request.GET.get('search', '')
    selected_building = request.GET.get('building', '')
    selected_category = request.GET.get('category', '')
    
    # Get all unique buildings
    all_buildings = Room.objects.values_list('building', flat=True).distinct().order_by('building')
    
    # Start with all rooms
    rooms_query = Room.objects.all()
    
    # Apply filters
    if search_query:
        rooms_query = rooms_query.filter(
            Q(name__icontains=search_query)
        )
    
    if selected_building:
        rooms_query = rooms_query.filter(building=selected_building)
        
    if selected_category:
        rooms_query = rooms_query.filter(category=selected_category)
    
    # Order by status
    rooms_query = rooms_query.order_by(
        Case(
            When(status='Available', then=Value(0)),
            When(status='Booked', then=Value(1)),
            When(status='Disabled', then=Value(2)),
            default=Value(3),
            output_field=IntegerField(),
        ),
        'id'
    )
    
    context = {
        'rooms': rooms_query,
        'selected_building': selected_building,
        'selected_category': selected_category,
        'buildings': all_buildings,
        'search_query': search_query,
        'categories': ROOM_CATEGORIES,
    }
    return render(request, 'app_room/rooms.html', context)

def room(request, room_id):
    one_room = Room.objects.get(id=room_id)
    context = {'room': one_room}
    return render(request, 'app_room/room_detail.html', context)

def room_detail(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    context = {
        'room': room,
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request, 'app_room/room_detail.html', context)