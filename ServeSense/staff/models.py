from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Represents a staff member in the system.

    This model extends Django's built-in User model to include details
    specific to restaurant staff, such as their role and on-duty status.

    Attributes:
        role (str): The staff member's job title (e.g., Manager, Waiter).
        is_on_duty (bool): True if the staff member is currently clocked in.
        phone_number (str): The staff member's contact phone number (optional).
    """
    ROLE_CHOICES = (
        ('Manager', 'Manager'),
        ('Waiter', 'Waiter'),
        ('Chef', 'Chef'),
    )
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='Waiter')
    is_on_duty = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        """Returns the username for a readable representation."""
        return self.username


class Attendance(models.Model):
    """Records a single work shift for a staff member.

    Each time a user clocks in, a new Attendance record is created. When they
    clock out, the 'clock_out_time' for that record is updated.

    Attributes:
        staff_member (User): A foreign key linking to the User who worked the shift.
        clock_in_time (DateTimeField): The exact date and time the shift started.
        clock_out_time (DateTimeField): The exact date and time the shift ended.
            This is null if the shift is still active.
    """
    staff_member = models.ForeignKey(User, on_delete=models.CASCADE)
    clock_in_time = models.DateTimeField(auto_now_add=True)
    clock_out_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        """Returns a string summary of the shift for the admin panel."""
        return f"{self.staff_member.username} - Shift from {self.clock_in_time.strftime('%Y-%m-%d %H:%M')}"