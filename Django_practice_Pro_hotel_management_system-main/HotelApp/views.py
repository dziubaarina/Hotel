from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


# Strona główna
def Home(request):
    return render(request, 'Home.html')


# Formularz rezerwacji dla gości (żeby żółty przycisk "Booking Now" działał)
def OnlineBooking(request):
    return render(request, 'online_booking_page.html')


# NASZE NOWE, ŁADNE LOGOWANIE
def Aothur_login(request):
    # Jeśli jesteś już zalogowana, od razu rzucamy Cię do panelu
    if request.user.is_authenticated:
        return redirect('/admin/')

    error_message = None

    if request.method == 'POST':
        # Pobieramy dane wpisane przez Ciebie w ładnym formularzu
        email = request.POST.get('Email')
        password = request.POST.get('Password')

        # Próbujemy zalogować (traktujemy Email jako Login)
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('/admin/')  # Sukces! Lądujesz w panelu Jazzmin
        else:
            error_message = "Nieprawidłowy e-mail lub hasło!"

    # Wyświetlamy ładną stronę logowania ze zdjęciem
    return render(request, 'Athur_login_page.html', {'error': error_message})