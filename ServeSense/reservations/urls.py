from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.reservation_list, name='reservation_list'),
    path('create/', views.create_reservation, name='add_reservation'),
    path('edit/<int:reservation_id>/', views.edit_reservation, name='edit_reservation'),
    path('delete/<int:reservation_id>/', views.delete_reservation, name='delete_reservation'),
    path('accept/<int:reservation_id>/', views.accept_reservation, name='accept_reservation'),
    path('', views.home, name='home'),  # Home page view
]