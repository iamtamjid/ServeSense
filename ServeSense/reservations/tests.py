from django.test import TestCase
from django.urls import reverse # reverse is used to find urls
from .models import Customer, Table, Reservation
import datetime


class ReservationTests(TestCase):

    def setUp(self):
        """
        Runs before every single test.

        This method sets up a consistent environment for all tests by creating
        a sample Table and a sample Customer in the test database. This avoids
        repeating the same creation code in every test function.
        """
        self.table = Table.objects.create(tableNumber='A1', capacity=2)
        self.customer = Customer.objects.create(firstName='John', lastName='Doe', phoneNumber='5231211')


    def test_create_reservation_works(self):
        """
        Tests the "happy path" for creating a new reservation.

        It simulates submitting the 'add_reservation' form with valid data and
        checks that the number of reservations in the database increases from
        0 to 1, confirming a successful creation.
        """
        new_booking_data = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'phone_number': '555-2222',
            'number_of_guests': 2,
            'reservation_date': datetime.date.today(),
            'reservation_time': '12:00',
        }

        self.assertEqual(Reservation.objects.count(), 0)
        self.client.post(reverse('add_reservation'), data=new_booking_data)
        self.assertEqual(Reservation.objects.count(), 1)


    def test_double_booking_is_prevented(self):
        """
        Tests the "sad path" to ensure the system prevents double bookings.

        First, it creates a reservation for a specific time. Then, it tries
        to create a second reservation for the exact same table at the same
        time. It asserts that the reservation count remains at 1 and that the
        user is shown an error message, confirming the system's validation works.
        """
        Reservation.objects.create(
            customer=self.customer,
            table=self.table,
            numberOfGuests=2,
            reservationDate=datetime.date.today(),
            reservationTime='20:00'
        )

        double_book_data = {
            'first_name': 'another',
            'last_name': 'person',
            'phone_number': '5553333',
            'number_of_guests': 2,
            'reservation_date': datetime.date.today(),
            'reservation_time': '20:00', # Same time
        }

        self.assertEqual(Reservation.objects.count(), 1)
        response = self.client.post(reverse('add_reservation'), data=double_book_data)
        self.assertEqual(Reservation.objects.count(), 1)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sorry, no tables are available")
        
        
    def test_edit_reservation_works(self):
        """
        Tests that the edit functionality correctly updates a reservation.

        It creates a reservation, then simulates submitting the edit form with
        a different number of guests. It then fetches the updated reservation
        from the database and asserts that the number of guests has changed,
        confirming the edit was successful.
        """
        reservation = Reservation.objects.create(
            customer=self.customer,
            table=self.table,
            numberOfGuests=2,
            reservationDate=datetime.date.today(),
            reservationTime='18:00'
        )
        
        edited_data = {
            'numberOfGuests': 1,
            'reservationDate': reservation.reservationDate,
            'reservationTime': reservation.reservationTime,
            'status': 'Pending',
        }
        
        edit_url = reverse('edit_reservation', args=[reservation.id])
        self.client.post(edit_url, data=edited_data)
        
        reservation.refresh_from_db()
        self.assertEqual(reservation.numberOfGuests, 1)


    def test_accept_reservation_works(self):
        """
        Tests the business logic for accepting a reservation.

        It creates a reservation with a 'Pending' status. It then simulates a
        manager clicking the "accept" link and verifies that the reservation's
        status changes to 'Confirmed' and the associated table's status
        changes to 'reserved'.
        """
        reservation = Reservation.objects.create(
            customer=self.customer,
            table=self.table,
            numberOfGuests=2,
            reservationDate=datetime.date.today(),
            reservationTime='17:00'
        )
        
        self.assertEqual(reservation.status, 'Pending')
        self.assertEqual(reservation.table.status, 'available')
        
        accept_url = reverse('accept_reservation', args=[reservation.id])
        self.client.get(accept_url)

        reservation.refresh_from_db()
        self.assertEqual(reservation.status, 'Confirmed')
        
        table = Table.objects.get(id=self.table.id)
        self.assertEqual(table.status, 'reserved')