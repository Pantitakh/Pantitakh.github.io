from django.urls import path
from . import views

urlpatterns = [
    path('create/<int:room_id>/', views.create_booking, name='create_booking'),
    path('delete-booking/<int:booking_id>/', views.delete_booking, name='delete_booking'),
    path('mybooking/', views.my_booking, name='my_booking'),
]