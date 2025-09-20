# reservations/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ReservationForm, EditReservationForm
from .models import Customer, Table, Reservation

def home(request):
    """Renders the main homepage of the application."""
    return render(request, 'index.html')


def create_reservation(request):
    """
    Handles the logic for the "Add Reservation" page.

    If the user is just visiting the page (a GET request), it shows a blank
    reservation form. If the user submits the form (a POST request), it first
    validates the data. If valid, it will either find an existing customer by
    their phone number or create a new one. It then searches for a table that
    is big enough and not already booked at that specific date and time. If an
    available table is found, the reservation is created, a success message is
    shown, and the user is redirected to the main reservation list. If no table
    is free, it shows an error on the form.
    """
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # create new customer or get existing one
            try:
                customer = Customer.objects.get(phoneNumber=data['phone_number'])
            except Customer.DoesNotExist:
                customer = Customer.objects.create(
                    firstName=data['first_name'],
                    lastName=data['last_name'],
                    phoneNumber=data['phone_number']
                )
            
            possible_tables = Table.objects.filter(capacity__gte=data['number_of_guests'])
            
            # Check for available tables at the requested time
            found_table = None
            for table in possible_tables:
                is_reserved = Reservation.objects.filter(
                    table=table, 
                    reservationDate=data['reservation_date'], 
                    reservationTime=data['reservation_time']
                ).exists()  # is_reserved is True if the table is already booked
                
                if not is_reserved:
                    found_table = table
                    break
            
            if found_table:
                Reservation.objects.create(
                    customer=customer,
                    table=found_table,
                    numberOfGuests=data['number_of_guests'],
                    reservationDate=data['reservation_date'],
                    reservationTime=data['reservation_time']
                )
                messages.success(request, "Reservation created successfully!")
                return redirect('reservation_list')
            else:
                form.add_error(None, "Sorry, no tables are available for that time and party size.")
    
    else:
        form = ReservationForm()

    return render(request, 'add_reservation.html', {'form': form})


def edit_reservation(request, reservation_id):
    """
    Manages the "Edit Reservation" page.
    
    It finds the specific reservation to edit using the 'reservation_id'
    from the URL. If the user is just visiting the page, it displays the
    edit form pre-filled with that reservation's current details. If the
    user submits the form with changes, it validates the data, saves the
    updates, and redirects back to the main reservation list.
    """
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if request.method == 'POST':
        form = EditReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            messages.success(request, "Reservation updated successfully!")
            return redirect('reservation_list')
    else:
        form = EditReservationForm(instance=reservation)

    return render(request, 'edit_reservation.html', {'form': form, 'reservation': reservation})


def delete_reservation(request, reservation_id):
    """
    Handles the deletion of a specific reservation.

    On a GET request, it shows a confirmation page to make sure the user
    really wants to delete the reservation. If the user confirms by submitting
    the form (a POST request), the reservation record is deleted from the
    database, and the user is redirected back to the reservation list.
    """
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if request.method == 'POST':
        reservation.delete()
        messages.success(request, "Reservation has been cancelled.")
        return redirect('reservation_list')

    return render(request, 'delete_reservation.html', {'reservation': reservation})


def accept_reservation(request, reservation_id):
    """
    Handles the business logic for confirming a reservation.

    This view is triggered when a manager "accepts" a reservation. It finds
    the specific reservation, changes its status to 'Confirmed', and then finds
    the associated table and updates its status to 'reserved'. Finally, it
    redirects the manager back to the reservation list with a success message.
    """
    reservation = get_object_or_404(Reservation, id=reservation_id)
    
    reservation.status = 'Confirmed'
    reservation.save()
    
    table_to_update = reservation.table
    table_to_update.status = 'reserved'
    table_to_update.save()

    messages.success(request, f"Reservation for {reservation.customer.firstName} has been Confirmed and Table {table_to_update.tableNumber} is now reserved.")
    
    return redirect('reservation_list')


def reservation_list(request):
    """
    Displays a complete list of all reservations.

    This view fetches every Reservation object from the database, ordering them
    by date and then by time so the earliest ones appear first. It then passes
    this list to the 'reservation_list.html' template to be displayed in a table.
    """
    all_reservations = Reservation.objects.order_by('reservationDate', 'reservationTime')
    context = {
        'reservations': all_reservations
    }
    return render(request, 'reservation_list.html', context)