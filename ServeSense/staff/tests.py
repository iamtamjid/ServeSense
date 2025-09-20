from django.test import TestCase
from django.urls import reverse #reverse is used to find urls
from .models import User, Attendance


class StaffTests(TestCase):

    def setUp(self):
        """
        Runs before every single test in this class.
        
        This method sets up a consistent testing environment by creating a
        single staff user. This user can then be used as a subject for all
        subsequent tests, such as editing their role or clocking them in.
        """
        self.staff_member = User.objects.create_user(
            username='testwaiter',
            password='Super_Password123',
            role='Waiter'
        )

    def test_staff_list_page_works(self):
        """
        Tests if the main staff list page loads correctly.
        
        This is a basic "smoke test" to ensure that the URL is configured
        properly and the view returns a successful HTTP 200 OK response,
        meaning the page can be accessed without server errors.
        """
        url = reverse('staff_list')
        response = self.client.get(url) #self.client is like a dummy web browser
        self.assertEqual(response.status_code, 200) #200 means OK


    def test_add_new_staff_member_works(self):
        """
        Tests if a new staff member can be successfully created.

        This test simulates a manager submitting the "add staff" form with
        valid data. It asserts that the total number of users in the database
        increases from 1 to 2, which confirms that the new user was created
        and saved correctly.
        """
        new_staff_data = {
            'username': 'newchef',
            'first_name': 'New',
            'last_name': 'Chef',
            'role': 'Chef',
            'password': 'VeryToughPassword456',
            'password2': 'VeryToughPassword456'
        }
        self.assertEqual(User.objects.count(), 1)
        url = reverse('add_staff')
        self.client.post(url, data=new_staff_data)
        self.assertEqual(User.objects.count(), 2)


    def test_edit_staff_role_works(self):
        """
        Tests if an existing staff member's role can be edited.
        
        It simulates submitting the edit form for our test user with a new
        role ('Manager'). It then fetches the user's data from the database
        again and asserts that the role has been successfully updated.
        """
        edited_data = {
            'role': 'Manager'
        }
        self.assertEqual(self.staff_member.role, 'Waiter')
        url = reverse('edit_staff', args=[self.staff_member.id])
        self.client.post(url, data=edited_data)
        self.staff_member.refresh_from_db()
        self.assertEqual(self.staff_member.role, 'Manager')


    def test_clock_in_and_out_works(self):
        """
        Tests the entire shift-tracking workflow for a staff member.

        This test first confirms the user starts as 'off duty'. It then
        simulates a "clock in" and asserts that the user's status becomes
        'on duty' and that an Attendance record is created. Finally, it
        simulates a "clock out" and asserts that the status flips back to
        'off duty' and that the Attendance record is updated with a
        clock-out time.
        """
        self.assertFalse(self.staff_member.is_on_duty)
        self.assertEqual(Attendance.objects.count(), 0)

        # Test Clocking In
        clock_in_url = reverse('clock_in', args=[self.staff_member.id])
        self.client.get(clock_in_url)
        self.staff_member.refresh_from_db()
        self.assertTrue(self.staff_member.is_on_duty)
        self.assertEqual(Attendance.objects.count(), 1)

        #Now let's test Clocking Out
        clock_out_url = reverse('clock_out', args=[self.staff_member.id])
        self.client.get(clock_out_url)
        self.staff_member.refresh_from_db()
        self.assertFalse(self.staff_member.is_on_duty)
        
        shift_log = Attendance.objects.first()
        self.assertEqual(shift_log.staff_member, self.staff_member)
        self.assertIsNotNone(shift_log.clock_out_time)