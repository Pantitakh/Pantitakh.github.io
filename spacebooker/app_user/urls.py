from django.urls import path, include
from .views import register, login_view, logout_view
from app_booking.views import my_booking, create_booking, delete_booking

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path('login/', login_view, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout_view, name='logout'),
    path('mybooking/', my_booking, name='my_booking'),
    path('create/<int:room_id>/', create_booking, name='create_booking'),
    path('delete-booking/<int:booking_id>/', delete_booking, name='delete_booking'),
]