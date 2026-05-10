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
]