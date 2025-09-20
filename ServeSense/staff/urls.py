# staff/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.staff_list, name='staff_list'),
    path('edit/<int:staff_id>/', views.edit_staff, name='edit_staff'),
    path('add/', views.add_staff, name='add_staff'),
    path('clock_in/<int:staff_id>/', views.clock_in, name='clock_in'),
    path('clock_out/<int:staff_id>/', views.clock_out, name='clock_out'),
    path('log/', views.attendance_log, name='attendance_log')
]