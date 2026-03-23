from django.contrib import admin
from django.urls import path
from django.contrib.auth import logout
from django.shortcuts import redirect
from HotelApp import views


# Szybkie wylogowanie bez białego ekranu
def szybkie_wylogowanie(request):
    logout(request)
    return redirect('/')


urlpatterns = [
    path('admin/', admin.site.urls),  # Panel Jazzmin
    path('', views.Home, name='Home'),  # Strona główna
    path('wyloguj/', szybkie_wylogowanie, name='wyloguj'),  # Przycisk wylogowania

    # Podpięcie "Booking Now"
    path('OnlineBooking/', views.OnlineBooking, name='OnlineBooking'),

    # Podpięcie ŁADNEGO logowania
    path('login/', views.Aothur_login, name='Aothur_login'),
]