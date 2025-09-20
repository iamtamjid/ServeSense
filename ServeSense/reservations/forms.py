from django import forms
from .models import Reservation

class ReservationForm(forms.Form):
    # customer fields
    first_name = forms.CharField(max_length=50, required=True, label="First Name")
    last_name = forms.CharField(max_length=50, required=True, label="Last Name")
    phone_number = forms.CharField(max_length=20, required=True, label="Phone Number")

    # reservation fields
    number_of_guests = forms.IntegerField(min_value=1, required=True, label="Number of Guests")
    reservation_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True, label="Date")
    reservation_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), required=True, label="Time")


class EditReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation  # template model
        fields = ['numberOfGuests', 'reservationDate', 'reservationTime'] # The fields we need to change
        widgets = {
            'reservationDate': forms.DateInput(attrs={'type': 'date'}),
            'reservationTime': forms.TimeInput(attrs={'type': 'time'}),
        }