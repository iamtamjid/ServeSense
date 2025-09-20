from django.db import models

class MenuItem(models.Model):
    """
    Represents a single menu item in the restaurant.

    Attributes:
        name (str): The name of the menu item.
        price (Decimal): The price of the item, up to 9999.99.
        available (bool): True if the item is currently available for order.
        best_seller (bool): True if the item is a popular or recommended choice.
    """
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    available = models.BooleanField(default=True)
    best_seller = models.BooleanField(default=False)

    def __str__(self):
        """
        Returns a human-readable representation of the menu item.
        """
        return self.name
