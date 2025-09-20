from django.urls import path
from . import views

"""
URL patterns for Menu management.

These routes allow viewing, editing, and deleting menu items.

Routes:
    '' (menu_list): Displays all menu items and handles adding a new item.
    'edit/<int:pk>/' (menu_edit): Edit an existing menu item by its primary key.
    'delete/<int:pk>/' (menu_delete): Delete a menu item by its primary key.
"""
urlpatterns = [
    path('', views.menu_list, name='menu_list'),
    path('edit/<int:pk>/', views.menu_edit, name='menu_edit'),
    path('delete/<int:pk>/', views.menu_delete, name='menu_delete'),
]
