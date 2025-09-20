from django.test import TestCase
from django.urls import reverse
from .models import MenuItem
from decimal import Decimal

class MenuItemModelTest(TestCase):
    """
    Test suite for the MenuItem model.

    Ensures that MenuItem instances can be created and that their fields
    contain the expected values.
    """

    def setUp(self):
        """
        Set up test data for MenuItem model tests.

        Creates a sample MenuItem instance named "Pizza".
        """
        MenuItem.objects.create(name="Pizza", price=9.99, available=True)

    def test_menu_item_creation(self):
        """
        Test that a MenuItem is correctly created and its fields are accurate.

        Checks the price and availability of the created MenuItem.
        """
        item = MenuItem.objects.get(name="Pizza")
        self.assertEqual(item.price, Decimal('9.99'))
        self.assertTrue(item.available)


class MenuViewsTest(TestCase):
    """
    Test suite for Menu-related views.

    Ensures that the menu list view loads correctly and displays menu items.
    """

    def setUp(self):
        """
        Set up test data for Menu views tests.

        Creates a sample MenuItem instance named "Burger".
        """
        MenuItem.objects.create(name="Burger", price=5.99, available=True)

    def test_menu_list_view(self):
        """
        Test that the menu list view returns HTTP 200 and contains expected content.

        Sends a GET request to the 'menu' view and checks for status code and item name.
        """
        response = self.client.get(reverse('menu_list'))  # corrected name to match typical URL
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Burger")
