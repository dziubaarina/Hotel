from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Online_Booking
from datetime import datetime


# 1. STRONA GŁÓWNA
def Home(request):
    return render(request, 'Home.html')


# 2. MOJE REZERWACJE (Widok listy rezerwacji zalogowanego użytkownika)
@login_required(login_url='Aothur_login')
def MyReservations(request):
    # Wyświetlamy rezerwacje przypisane do adresu email zalogowanego użytkownika
    bookings = Online_Booking.objects.filter(Email=request.user.email).order_by('-Check_in')
    return render(request, 'my_reservations.html', {'bookings': bookings})


# 3. ANULOWANIE REZERWACJI
@login_required(login_url='Aothur_login')
def CancelBooking(request, pk):
    # Sprawdzamy, czy rezerwacja należy do użytkownika (po emailu)
    booking = get_object_or_404(Online_Booking, pk=pk, Email=request.user.email)
    booking.delete()
    messages.success(request, "Twoja rezerwacja została pomyślnie anulowana.")
    return redirect('MyReservations')


# 4. PROCES REZERWACJI
@login_required(login_url='Aothur_login')
def OnlineBooking(request):
    if request.method == 'POST':
        check_in = request.POST.get('Check_in')
        check_out = request.POST.get('Check_out')
        room_type = request.POST.get('Room_Type')

        try:
            d1 = datetime.strptime(check_in, '%Y-%m-%d')
            d2 = datetime.strptime(check_out, '%Y-%m-%d')

            if d1 >= d2:
                messages.error(request, "Data wyjazdu musi być późniejsza niż przyjazdu!")
                return render(request, 'online_booking_page.html')

            Online_Booking.objects.create(
                Check_in=check_in,
                Check_out=check_out,
                Name=request.POST.get('Name'),
                Surname=request.POST.get('Surname'),
                Email=request.user.email,  # Rezerwacja przypisana do emaila zalogowanego konta
                Phone_Number=request.POST.get('Phone_Number'),
                City=request.POST.get('City', ''),
                Country=request.POST.get('Country', ''),
                ADULT=request.POST.get('ADULT', '1'),
                CHILDREN=request.POST.get('CHILDREN', '0'),
                Room_Type=room_type,
            )
            messages.success(request, "Rezerwacja zakończona sukcesem!")
            return redirect('MyReservations')
        except (ValueError, TypeError):
            messages.error(request, "Wystąpił błąd w datach. Spróbuj ponownie.")
            return render(request, 'online_booking_page.html')

    return render(request, 'online_booking_page.html')


# 5. LOGOWANIE (ADMIN PO LOGINIE / KLIENT PO EMAILU)
def Aothur_login(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('/admin/')
        return redirect('Home')

    if request.method == 'POST':
        identifier = request.POST.get('Email')  # To pole w HTML przyjmie login LUB email
        password = request.POST.get('Password')

        # Próba 1: Logowanie tradycyjne (np. wpisujesz 'admin')
        user = authenticate(request, username=identifier, password=password)

        # Próba 2: Jeśli nie wyszło, sprawdzamy czy identifier to e-mail
        if user is None:
            try:
                user_obj = User.objects.get(email=identifier)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None

        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('/admin/')
            return redirect('Home')
        else:
            messages.error(request, "Błędny e-mail/login lub hasło!")

    return render(request, 'Athur_login_page.html')


# 6. REJESTRACJA
def Athur_Register(request):
    if request.user.is_authenticated:
        return redirect('Home')

    if request.method == 'POST':
        email = request.POST.get('Email')
        pwd = request.POST.get('Password')
        cpwd = request.POST.get('Con_password')

        if User.objects.filter(username=email).exists():
            messages.error(request, "Ten adres e-mail jest już zarejestrowany!")
            return render(request, 'Athur_Register_Page.html')

        if pwd != cpwd:
            messages.error(request, "Hasła nie są identyczne!")
            return render(request, 'Athur_Register_Page.html')

        User.objects.create_user(
            username=email,
            email=email,
            password=pwd,
            first_name=request.POST.get('Fname'),
            last_name=request.POST.get('Lname')
        )

        messages.success(request, "Konto utworzone! Możesz się teraz zalogować.")
        return redirect('Aothur_login')

    return render(request, 'Athur_Register_Page.html')


# 7. WYLOGOWANIE
def Logout_user(request):
    logout(request)
    return redirect('Home')