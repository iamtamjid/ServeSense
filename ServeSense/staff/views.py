from django.shortcuts import get_object_or_404, redirect, render
from .models import User, Attendance # Import our custom User model
from .forms import EditStaffForm, AddStaffForm
from django.utils import timezone


def staff_list(request):
    """
    This function is responsible for the main staff overview page. 
    Its primary job is to fetch every user object from the database using User.objects.all(). 
    It then packages this list of staff members into a context dictionary and passes it 
    to the 'staff_list.html' template, which handles the actual display.
    """
    all_staff = User.objects.all() # fetch all staff
    
    context = {
        'staff_members': all_staff
    }
    return render(request, 'staff_list.html', context) # semd back context to ui 


def edit_staff(request, staff_id):
    """
    This view manages the process of updating a staff member's profile.
    It takes a 'staff_id' from the URL to identify which user to edit, using 
    get_object_or_404 to safely retrieve them. If the request is a POST, it means 
    a form was submitted, so it validates the data using the EditStaffForm and saves 
    the changes. If it's a GET request, it simply displays the same form, but 
    pre-filled with the staff member's current information.
    """
    staff_member = get_object_or_404(User, id=staff_id)
    # Check if the manager is submitting the form (POST) or just visiting the page (GET)
    if request.method == 'POST':
        form = EditStaffForm(request.POST, instance=staff_member)
        if form.is_valid():
            form.save() # Save the changes to the database
            return redirect('staff_list') # Redirect back to the main staff list page
    else:
        form = EditStaffForm(instance=staff_member) # Prefilled with current role

    # Render the HTML template, passing the form and staff member to it.
    context = {
        'form': form,
        'staff_member': staff_member
    }
    return render(request, 'edit_staff.html', context)


def add_staff(request):
    """
    This view handles the creation of a new staff member account. It uses the 
    custom AddStaffForm, which is based on Django's UserCreationForm to ensure 
    passwords are handled securely. On a GET request, it shows a blank form. 
    On a POST request, it validates the submitted data and, if valid, saves the new 
    user to the database before redirecting the manager back to the main staff list.
    """
    if request.method == 'POST':
        form = AddStaffForm(request.POST)
        if form.is_valid():

            user = form.save(commit=False)
            
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.phone_number = form.cleaned_data['phone_number']
            user.role = form.cleaned_data['role']
            
            # Now we save the user to the database with all the complete information.
            user.save()
            return redirect('staff_list')
    else:
        form = AddStaffForm()

    context = {
        'form': form
    }
    return render(request, 'add_staff_form.html', context)


def clock_in(request, staff_id):
    """
    This is a simple action-oriented view that handles when a staff member starts their shift.
    It finds the specific user by their ID, sets their 'is_on_duty' status to True,
    and saves the change. Critically, it also creates a new record in the Attendance table,
    linking it to the staff member and automatically timestamping the clock-in time.
    It does not render a template; it simply redirects back to the staff list.
    """
    staff_member = get_object_or_404(User, id=staff_id)
    staff_member.is_on_duty = True
    staff_member.save()
    
    Attendance.objects.create(staff_member=staff_member)
    return redirect('staff_list')


def clock_out(request, staff_id):
    """
    This view handles the end of a staff member's shift. It finds the user and sets
    their 'is_on_duty' status to False. It then attempts to find the most recent
    'Attendance' record for that user that does not yet have a clock-out time. 
    If it finds one, it updates the 'clock_out_time' to the current time, effectively
    ending the shift log. The 'try...except' block safely handles cases where an open
    shift might not be found, preventing the application from crashing.
    """
    staff_member = get_object_or_404(User, id=staff_id)
    staff_member.is_on_duty = False
    staff_member.save()

    try:
        # Find the current, un-ended shift for this staff member
        current_shift = Attendance.objects.get(staff_member=staff_member, clock_out_time__isnull=True) 
        current_shift.clock_out_time = timezone.now() # Set the clock-out time
        current_shift.save()
    except Attendance.DoesNotExist:
        # Handle cases where there might not be an open shift (e.g., data error)
        pass 
    return redirect('staff_list')


def attendance_log(request):
    """
    This function is built to display the complete history of all staff shifts.
    It queries the Attendance model to get every single record. It orders the results
    by 'clock_in_time' in descending order ('-clock_in_time') so that the most recent
    shifts appear at the top of the list. It then passes this list of logs to the 
    'attendance_log.html' template for display.
    """
    all_logs = Attendance.objects.all().order_by('-clock_in_time')
    context = {
        'logs': all_logs
    }
    return render(request, 'attendance_log.html', context)