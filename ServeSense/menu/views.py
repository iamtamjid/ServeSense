from django.shortcuts import render, redirect, get_object_or_404
from .models import MenuItem
from .forms import MenuItemForm

def menu_list(request):
    """
    Display all menu items and handle adding a new menu item.

    This view fetches all existing MenuItem records and displays them in a list.
    It also processes the form submission for adding a new menu item.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders 'menu/menu_list.html' with menu items and add form.
    """
    menu_items = MenuItem.objects.all()

    # Handle add form submission
    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('menu_list')
    else:
        form = MenuItemForm()

    return render(request, 'menu_list.html', {'menu_items': menu_items, 'form': form})


def menu_edit(request, pk):
    """
    Edit an existing menu item.

    Retrieves a MenuItem by primary key. If the request method is POST,
    updates the item with form data. Otherwise, displays the form pre-filled
    with the item's current data.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): Primary key of the MenuItem to edit.

    Returns:
        HttpResponse: Renders 'menu/menu_edit.html' with the edit form.
    """
    item = get_object_or_404(MenuItem, pk=pk)
    if request.method == 'POST':
        form = MenuItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('menu_list')
    else:
        form = MenuItemForm(instance=item)
    return render(request, 'menu_edit.html', {'form': form})


def menu_delete(request, pk):
    """
    Delete a menu item.

    Retrieves a MenuItem by primary key and deletes it from the database.
    Redirects to the menu list after deletion.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): Primary key of the MenuItem to delete.

    Returns:
        HttpResponseRedirect: Redirects to the 'menu_list' view.
    """
    item = get_object_or_404(MenuItem, pk=pk)
    item.delete()
    return redirect('menu_list')
