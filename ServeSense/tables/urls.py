from django.urls import path
from . import views

"""
URL patterns for Table management.

These routes allow viewing, editing, and deleting restaurant tables.

Routes:
    '' (table_list): Displays all tables and handles adding a new table.
    'edit/<int:pk>/' (table_edit): Edit an existing table by its primary key.
    'delete/<int:pk>/' (table_delete): Delete a table by its primary key.
"""
urlpatterns = [
    path('', views.table_list, name='table_list'),
    path('edit/<int:pk>/', views.table_edit, name='table_edit'),
    path('delete/<int:pk>/', views.table_delete, name='table_delete'),
]
