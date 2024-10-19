from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils import timezone
from app_room.models import Room
from .models import Booking
from django.shortcuts import redirect

@login_required
@require_POST
def create_booking(request, room_id):
    if request.method == 'POST':
        # Get data from the form submission
        booking_date = request.POST.get('booking_date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        purpose = request.POST.get('purpose')
        details = request.POST.get('details')

        # Combine date and time
        start_datetime = timezone.datetime.strptime(f"{booking_date} {start_time}", "%Y-%m-%d %H:%M")
        end_datetime = timezone.datetime.strptime(f"{booking_date} {end_time}", "%Y-%m-%d %H:%M")

        room = Room.objects.get(id=room_id)

        # Check if the booking is within the room's available hours
        day_of_week = start_datetime.strftime('%A')

        # Check if the booking is within the room's available hours and day
        if room.day == 'Weekdays (Mon.-Fri.)' and day_of_week in ['Saturday', 'Sunday']:
            return JsonResponse({
                'status': 'error',
                'message': 'This room is not available on the weekend (Sat-Sun)'
            })

        if room.day == 'Weekend' and day_of_week not in ['Saturday', 'Sunday']:
            return JsonResponse({
                'status': 'error',
                'message': 'This room is only available on weekends (Sat-Sun)'
            })

        if room.day == 'Everyday':
            # No need to check days if it is available every day
            pass
        else:
            if room.day != day_of_week and room.day != 'Weekdays (Mon.-Fri.)' and room.day != 'Weekend':
                return JsonResponse({
                    'status': 'error',
                    'message': f'This room is not available on {day_of_week}'
                })

        if start_datetime.time() < room.open_time or end_datetime.time() > room.close_time:
            return JsonResponse({
                'status': 'error',
                'message': f'This room is only available between {room.open_time} - {room.close_time}'
            })

        # Check for conflicting bookings
        conflicting_bookings = Booking.objects.filter(
            room=room,
            start_time__lt=end_datetime,
            end_time__gt=start_datetime,
        )

        if conflicting_bookings.exists():
            return JsonResponse({
                'status': 'error',
                'message': 'This room is already booked for the selected time'
            })

        # If no errors, save the booking
        booking = Booking.objects.create(
            room=room,
            user=request.user,
            booking_date=booking_date,
            start_time=start_datetime,
            end_time=end_datetime,
            purpose=purpose,
            details=details,
            status='pending'
        )

        return JsonResponse({
            'status': 'success',
            'message': 'Booking created successfully',
            'booking_id': booking.id
        })
    

def my_booking(request):
    if request.user.is_staff:  # If the user is an admin
        return redirect('/admin/app_booking/booking/')  # Redirect or handle admin differently
    
    all_bookings = Booking.objects.filter(user=request.user).order_by('-created_at') #Get every booking in database
    print(all_bookings)
    context = {
        'bookings': all_bookings,
        'current_time': timezone.now(),
    }
    return render(request, 'app_user/mybooking.html', context)

@login_required
@require_POST
def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking.delete()  # Delete the booking
    return JsonResponse({'status': 'success', 'message': 'Booking canceled successfully'})