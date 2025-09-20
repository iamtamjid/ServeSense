from django.shortcuts import render, redirect, get_object_or_404
from .models import Table
from .forms import TableForm

def table_list(request):
    """
    Display all tables and handle adding a new table.

    This view fetches all existing Table records and displays them in a list.
    It also processes the form submission for adding a new table.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders 'tables/table_list.html' with tables and add form.
    """
    tables = Table.objects.all()

    # Handle add form submission
    if request.method == 'POST':
        form = TableForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('table_list')
    else:
        form = TableForm()

    return render(request, 'table_list.html', {'tables': tables, 'form': form})


def table_edit(request, pk):
    """
    Edit an existing table.

    Retrieves a Table by primary key. If the request method is POST,
    updates the table with form data. Otherwise, displays the form pre-filled
    with the table's current data.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): Primary key of the Table to edit.

    Returns:
        HttpResponse: Renders 'tables/table_edit.html' with the edit form.
    """
    table = get_object_or_404(Table, pk=pk)
    if request.method == 'POST':
        form = TableForm(request.POST, instance=table)
        if form.is_valid():
            form.save()
            return redirect('table_list')
    else:
        form = TableForm(instance=table)

    return render(request, 'table_edit.html', {'form': form})


def table_delete(request, pk):
    """
    Delete a table.

    Retrieves a Table by primary key and deletes it from the database.
    Redirects to the table list after deletion.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): Primary key of the Table to delete.

    Returns:
        HttpResponseRedirect: Redirects to the 'table_list' view.
    """
    table = get_object_or_404(Table, pk=pk)
    table.delete()
    return redirect('table_list')
