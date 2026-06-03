from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='Home'),
    path('OnlineBooking/', views.OnlineBooking, name='OnlineBooking'),
    path('Aothur_login/', views.Aothur_login, name='Aothur_login'),
    path('Athur_Register/', views.Athur_Register, name='Athur_Register'),
    path('wyloguj/', views.Logout_user, name='Logout_user'),
    path('moje-rezerwacje/', views.MyReservations, name='MyReservations'),
    path('anuluj-rezerwacje/<int:pk>/', views.CancelBooking, name='CancelBooking'),
    path('panel/', views.StaffPanel, name='StaffPanel'),
    path('panel/rezerwacja/<int:pk>/usun/', views.StaffDeleteBooking, name='StaffDeleteBooking'),
    path('panel/uprawnienia/nadaj/', views.StaffGrantEmployee, name='StaffGrantEmployee'),
    path('panel/uprawnienia/<int:pk>/odebierz/', views.StaffRevokeEmployee, name='StaffRevokeEmployee'),
    path('api/dostepnosc/', views.BookingAvailabilityAPI, name='BookingAvailabilityAPI'),
]