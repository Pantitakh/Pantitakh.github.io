from django.contrib.auth.models import User
from django.db import models
from shortuuid.django_fields import ShortUUIDField

ROOM_STATUS = (
    ("Available", "Available"),
    ("Booked", "Booked"),
    ("Unavailable", "Unavailable"),
    ("Under Maintenance", "Under Maintenance"),
    ("Closed", "Closed"),
    ("Pending", "Pending"),
    ("In Use", "In Use"),
    ("Reserved", "Reserved"),
)

DAYS_OF_WEEK = (
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
    ('Sunday', 'Sunday'),
    ('Weekdays (Mon.-Fri.)', 'Weekdays (Mon.-Fri.)'),
    ('Weekend', 'Weekend'),
    ('Everyday', 'Everyday'),
)

ROOM_CATEGORIES = (
    ('Conference', 'Conference Room'),
    ('Meeting', 'Meeting Room'),
    ('Classroom', 'Classroom'),
    ('Laboratory', 'Laboratory'),
)

# Create your models here. #
class Room(models.Model):
    BUILDING = (
    ('EN01 Department of Civil Engineering', 'EN01 Department of Civil Engineering'),
    ('EN02 Civil Engineering Laboratory', 'EN02 Civil Engineering Laboratory'),
    ('EN03', 'EN03'),
    ('EN04 Department of Computer Engineering Building', 'EN04 Department of Computer Engineering Building'),
    ('EN05 Department of Agriculture Engineering', 'EN05 Department of Agriculture Engineering'),
    ('EN06 Environmental Engineering Laboratory Building', 'EN60 Environmental Engineering Laboratory Building'),
    ('EN07 Mechanical Engineering Laboratory Building', 'EN07 Mechanical Engineering Laboratory Building'),
    ('EN08 Department od Industrial Engineering', 'EN08 Department od Industrial Engineering'),
    ('EN09 CB Building', 'EN09 CB Building'),
    ('EN10 Department of Mechanical Engineering', 'EN10 Department of Mechanical Engineering'),
    ('EN11 Department of Electrical Engineering', 'EN11 Department of Electrical Engineering'),
    ('EN12 Agricultural Engineering Laboratory Building', 'EN12 Agricultural Engineering Laboratory Building'),
    ('EN13 Department of Environmental Engineering', 'EN13 Department of Environmental Engineering'),
    ('EN14 Department of Chemical Engineering', 'EN14 Department of Chemical Engineering'),
    ('EN15 Engineering Library', 'EN15 Engineering Library'),
    ('EN16 Pienvijit Building', 'EN16 Pienvijit Building'),
    ('EN17 Industrial Engineering Laboratory Building', 'EN17 Industrial Engineering Laboratory Building'),
    ('EN18 50 Years Engineering Building', 'EN18 50 Years Engineering Building'),
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    image1 = models.ImageField(default='enkku.jpg', blank=True)
    image2 = models.ImageField(default='enkku.jpg', blank=True)
    image3 = models.ImageField(default='enkku.jpg', blank=True)
    floor = models.CharField(null=True, max_length=10)
    building = models.CharField(choices=BUILDING, max_length=100, default='Pienvijit')
    capacity = models.IntegerField()
    has_mic = models.BooleanField(default=False)
    has_camera = models.BooleanField(default=False)
    has_laptop = models.BooleanField(default=False)
    description = models.TextField(null=True)
    category = models.CharField(
        max_length=20,
        choices=ROOM_CATEGORIES,
        default='Meeting'
    )
    day = models.CharField(choices=DAYS_OF_WEEK, max_length=20, default='Weekdays (Mon.-Fri.)')
    open_time = models.TimeField(default='08:00:00')
    close_time = models.TimeField(default='16:00:00')
    status = models.CharField(choices=ROOM_STATUS, max_length=20, default="Available")

    def __str__(self):
        return self.name

    @classmethod
    def get_building_choices(cls):
        return cls.BUILDING