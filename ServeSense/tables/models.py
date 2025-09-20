from django.db import models

class Table(models.Model):
    """
    Represents a restaurant table and its current status.

    Attributes:
        number (int): Unique table number.
        capacity (int): Maximum number of guests the table can accommodate.
        status (str): Current status of the table. Choices are:
            - 'Free': Table is available.
            - 'Reserved': Table is booked for a reservation.
            - 'Occupied': Table is currently in use.
        time_left (int): Optional; estimated minutes remaining for the table to be free.
    """
    STATUS_CHOICES = [
        ('Free', 'Free'),
        ('Reserved', 'Reserved'),
        ('Occupied', 'Occupied'),
    ]

    number = models.IntegerField(unique=True)
    capacity = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Free')
    time_left = models.IntegerField(null=True, blank=True)

    def __str__(self):
        """
        Returns a human-readable representation of the table.
        """
        return f"Table {self.number}"
