from django import forms
from .models import Table

class TableForm(forms.ModelForm):
    """
    Form for creating or updating Table records.

    This form provides fields to add or edit a restaurant table,
    including its number, capacity, current status, and optional time left.

    Fields:
        number (int): Unique table number.
        capacity (int): Maximum number of guests the table can accommodate.
        status (str): Current status of the table. Choices: Free, Reserved, Occupied.
        time_left (int): Optional; estimated minutes remaining for the table to be free.
    """
    class Meta:
        model = Table
        fields = ['number', 'capacity', 'status', 'time_left']
