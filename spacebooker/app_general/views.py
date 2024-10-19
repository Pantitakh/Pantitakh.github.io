from django.shortcuts import render
from django.utils import timezone
from app_booking.models import Booking
from datetime import datetime, timedelta

def home(request):
    # Get today's date
    today = timezone.now().date()
    
    # Get the selected date from request, default to today
    selected_date_str = request.GET.get('selected_date')
    
    if selected_date_str:
        try:
            selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
        except ValueError:
            selected_date = today
    else:
        selected_date = today

    # Get approved bookings for the selected date and future dates
    upcoming_bookings = Booking.objects.filter(
        start_time__date__gte=selected_date,  # Greater than or equal to selected date
        start_time__date__lte=selected_date + timedelta(days=7),  # Show next 30 days max
        status='approved'
    ).select_related('room', 'user').order_by('start_time')

    # Group bookings by date
    bookings_by_date = {}
    for booking in upcoming_bookings:
        booking_date = booking.start_time.date()
        if booking_date not in bookings_by_date:
            bookings_by_date[booking_date] = []
        bookings_by_date[booking_date].append(booking)

    context = {
        'bookings_by_date': bookings_by_date,
        'selected_date': selected_date,
        'today': today,
    }
    return render(request, 'app_general/home.html', context)