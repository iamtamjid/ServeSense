from django.db import models

class Customer(models.Model):
    """Represents a customer who makes a reservation.

    This model stores the basic contact information for a customer, which allows
    the restaurant to identify them. The phoneNumber is a key piece of information
    used to look up existing customers when a new reservation is being made.

    Attributes:
        firstName (str): The customer's first name.
        lastName (str): The customer's last name.
        phoneNumber (str): The customer's contact phone number.
    """
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    phoneNumber = models.CharField(max_length=20)

    def __str__(self):
        """Returns a string representation of the customer for the admin panel."""
        return self.lastName + ", " + self.phoneNumber


class Table(models.Model):
    """Represents a single physical table in the restaurant.

    Each table has a unique number or identifier, a capacity to indicate how
    many guests it can seat, and a status to track whether it is currently
    available, reserved for an upcoming booking, or occupied by guests.

    Attributes:
        tableNumber (str): A unique identifier for the table (e.g., 'A1').
        capacity (int): The maximum number of guests the table can seat.
        status (str): The current status of the table (e.g., 'available').
    """
    tableNumber = models.CharField(unique=True, max_length=10)
    capacity = models.IntegerField()
    status = models.CharField(max_length=20, default='available')

    def __str__(self):
        """Returns a detailed string summary of the table."""
        return f"Table {self.tableNumber} - Seats: {self.capacity} - Status: {self.status}"


class Reservation(models.Model):
    """Represents a booking made by a customer for a specific table.

    This is the central model that links a Customer to a Table for a specific
    date and time. It tracks the number of guests, the booking details, and
    the current status of the reservation (e.g., Pending, Confirmed, or
    Cancelled).

    Attributes:
        customer (Customer): A foreign key to the customer who made the booking.
        table (Table): A foreign key to the table that was booked.
        numberOfGuests (int): The number of people in the party.
        reservationTime (TimeField): The time of the reservation.
        reservationDate (DateField): The date of the reservation.
        status (str): The current status of the booking (e.g., 'Pending').
        
    """
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    numberOfGuests = models.IntegerField()
    reservationTime = models.TimeField()
    reservationDate = models.DateField()
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        """Returns a concise summary of the reservation."""
        return f"Reservation for {self.customer} at {self.reservationDate} for Table {self.table}"