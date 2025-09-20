from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm


class EditStaffForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'role']
        

class AddStaffForm(UserCreationForm):
    """
    Create new staff users by extending Django's default UserCreationForm to include our custom fields
    """
    class Meta(UserCreationForm.Meta):
        model = User
        # Define the fields to be shown on the form
        fields = ('username', 'first_name', 'last_name', 'phone_number', 'role')