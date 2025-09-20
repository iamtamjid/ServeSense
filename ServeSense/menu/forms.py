from django import forms
from .models import MenuItem

class MenuItemForm(forms.ModelForm):
    """
    Form for creating or updating MenuItem records.

    This form allows adding or editing a menu item in the restaurant,
    including its name, price, availability, and whether it is a best seller.

    Fields:
        name (str): Name of the menu item.
        price (Decimal): Price of the item.
        available (bool): Whether the item is currently available for order.
        best_seller (bool): Whether the item is marked as a popular choice.
    """
    class Meta:
        model = MenuItem
        fields = ['name', 'price', 'available', 'best_seller']
