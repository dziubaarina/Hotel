from django.shortcuts import render, redirect, get_object_or_404

from django.urls import reverse

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required

from django.contrib import messages

from django.views.decorators.http import require_GET, require_POST

from django.http import JsonResponse

from datetime import timedelta
from django.utils import timezone



from .decorators import staff_required, admin_required
from .roles import is_hotel_admin, role_label

from .models import Add_Employee, Add_Room, Online_Booking

from .forms import OnlineBookingForm, StaffRoomForm

from .availability import availability_payload, occupancy_for_period, parse_date
from .staff_users import panel_employee_rows, panel_employees_queryset





def Home(request):
    team_members = Add_Employee.objects.all().order_by("Employee_Id")

    check_in = request.GET.get("check_in", "")

    check_out = request.GET.get("check_out", "")

    rooms = Add_Room.objects.all().order_by("Room_Number")

    room_offers = []

    for idx, room in enumerate(rooms, start=1):

        occ = None

        if check_in and check_out:

            from .availability import occupancy_summary



            occ = occupancy_summary(room.Room_Type, check_in, check_out)

            if occ["full"]:

                continue

        room_offers.append(

            {

                "room": room,

                "room_id": idx,

                "occupancy": occ,

            }

        )

    return render(

        request,

        "Home.html",

        {

            "room_offers": room_offers,

            "filter_check_in": check_in,

            "filter_check_out": check_out,

            "team_members": team_members,

        },

    )





@staff_required
def StaffPanel(request):
    tab = request.GET.get("tab", "przeglad")
    allowed_tabs = ("przeglad", "rezerwacje", "pokoje", "pracownicy")
    if is_hotel_admin(request.user):
        allowed_tabs = allowed_tabs + ("uprawnienia",)
    if tab not in allowed_tabs:
        tab = "przeglad"
    if tab == "uprawnienia" and not is_hotel_admin(request.user):
        tab = "przeglad"

    edit_room = None
    edit_room_form = None
    hotel_admin = is_hotel_admin(request.user)

    today = timezone.localdate()
    occ_from = request.GET.get("occ_from") or today.isoformat()
    occ_to = request.GET.get("occ_to") or (today + timedelta(days=30)).isoformat()
    if parse_date(occ_from) and parse_date(occ_to) and parse_date(occ_from) > parse_date(occ_to):
        occ_from, occ_to = occ_to, occ_from

    if request.method == "POST" and "edit_room" in request.POST:
        if not hotel_admin:
            messages.error(request, "Edycja pokoi jest dostępna tylko dla administratora.")
            return redirect(f"{reverse('StaffPanel')}?tab=pokoje")
        tab = "pokoje"
        room = get_object_or_404(Add_Room, pk=request.POST.get("room_id"))
        edit_room_form = StaffRoomForm(request.POST, request.FILES, instance=room)
        if edit_room_form.is_valid():
            edit_room_form.save()
            messages.success(request, f"Oferta „{room.Room_Type}” została zaktualizowana.")
            return redirect(f"{reverse('StaffPanel')}?tab=pokoje&occ_from={occ_from}&occ_to={occ_to}")
        edit_room = room
        messages.error(request, "Popraw błędy w formularzu edycji.")

    edit_id = request.GET.get("edit")
    if edit_id and tab == "pokoje" and hotel_admin:
        edit_room = get_object_or_404(Add_Room, pk=edit_id)
        edit_room_form = StaffRoomForm(instance=edit_room)
    elif edit_id and tab == "pokoje" and not hotel_admin:
        messages.error(request, "Nie masz uprawnień do edycji ogłoszeń pokoi.")

    bookings = Online_Booking.objects.all().order_by("-Date", "-Id")[:50]
    occupancy_rows = []
    if tab == "pokoje" and parse_date(occ_from) and parse_date(occ_to):
        occupancy_rows = occupancy_for_period(occ_from, occ_to)

    portal_users = []
    if tab == "uprawnienia" and hotel_admin:
        portal_users = [
            {
                "user": u,
                "role": role_label(u),
                "can_revoke": u.is_staff and not u.is_superuser and u.pk != request.user.pk,
            }
            for u in User.objects.all().order_by("-is_superuser", "-is_staff", "email")
        ]

    context = {
        "active_tab": tab,
        "bookings": bookings,
        "booking_count": Online_Booking.objects.count(),
        "room_count": Add_Room.objects.count(),
        "employee_count": panel_employees_queryset().count(),
        "user_count": User.objects.count(),
        "rooms": Add_Room.objects.all().order_by("Room_Number"),
        "panel_employees": panel_employee_rows(),
        "edit_room": edit_room,
        "edit_room_form": edit_room_form,
        "occ_from": occ_from,
        "occ_to": occ_to,
        "occupancy_rows": occupancy_rows,
        "portal_users": portal_users,
        "user_role_label": role_label(request.user),
    }
    return render(request, "staff_panel.html", context)


@staff_required
@admin_required
@require_POST
def StaffGrantEmployee(request):
    identifier = request.POST.get("email", "").strip()
    if not identifier:
        messages.error(request, "Podaj adres e-mail konta użytkownika.")
        return redirect(f"{reverse('StaffPanel')}?tab=uprawnienia")

    target = (
        User.objects.filter(email__iexact=identifier).first()
        or User.objects.filter(username__iexact=identifier).first()
    )
    if not target:
        messages.error(request, f"Nie znaleziono konta: {identifier}")
        return redirect(f"{reverse('StaffPanel')}?tab=uprawnienia")

    if target.is_superuser:
        messages.info(request, f"{target.email} ma już uprawnienia administratora.")
    elif target.is_staff:
        messages.info(request, f"{target.email} jest już pracownikiem panelu.")
    else:
        target.is_staff = True
        target.is_superuser = False
        target.save(update_fields=["is_staff", "is_superuser"])
        messages.success(request, f"Nadano uprawnienia pracownika: {target.email}")

    return redirect(f"{reverse('StaffPanel')}?tab=uprawnienia")


@staff_required
@admin_required
@require_POST
def StaffRevokeEmployee(request, pk):
    target = get_object_or_404(User, pk=pk)
    if target.is_superuser:
        messages.error(request, "Nie można odebrać uprawnień administratorowi.")
        return redirect(f"{reverse('StaffPanel')}?tab=uprawnienia")
    if target.pk == request.user.pk:
        messages.error(request, "Nie możesz odebrać uprawnień samemu sobie.")
        return redirect(f"{reverse('StaffPanel')}?tab=uprawnienia")
    if not target.is_staff:
        messages.info(request, "To konto nie ma już uprawnień pracownika.")
    else:
        target.is_staff = False
        target.save(update_fields=["is_staff"])
        messages.success(request, f"Odebrano uprawnienia pracownika: {target.email}")
    return redirect(f"{reverse('StaffPanel')}?tab=uprawnienia")





@require_GET

def BookingAvailabilityAPI(request):

    check_in = request.GET.get("check_in", "").strip()

    check_out = request.GET.get("check_out", "").strip()

    room_type = request.GET.get("room_type", "").strip() or None

    exclude_id = request.GET.get("exclude_id")

    exclude_booking_id = int(exclude_id) if exclude_id and exclude_id.isdigit() else None

    data = availability_payload(

        check_in=check_in or None,

        check_out=check_out or None,

        room_type=room_type,

        exclude_booking_id=exclude_booking_id,

    )

    return JsonResponse(data)





@staff_required

@require_POST

def StaffDeleteBooking(request, pk):

    booking = get_object_or_404(Online_Booking, pk=pk)

    booking.delete()

    messages.success(request, f"Rezerwacja #{pk} została usunięta.")

    return redirect(f"{reverse('StaffPanel')}?tab=rezerwacje")





@login_required(login_url='Aothur_login')

def MyReservations(request):

    bookings = Online_Booking.objects.filter(Email=request.user.email).order_by('-Check_in')

    return render(request, 'my_reservations.html', {'bookings': bookings})





@login_required(login_url='Aothur_login')

@require_POST

def CancelBooking(request, pk):

    booking = get_object_or_404(Online_Booking, pk=pk, Email=request.user.email)

    booking.delete()

    messages.success(request, "Twoja rezerwacja została pomyślnie anulowana.")

    return redirect('MyReservations')





def OnlineBooking(request):

    rooms = list(Add_Room.objects.all().order_by("Room_Number"))

    if request.method == "POST":

        form = OnlineBookingForm(request.POST, user=request.user)

        if form.is_valid():

            booking = form.save(commit=False)

            if request.user.is_authenticated:

                booking.Email = request.user.email

            else:

                booking.Email = form.cleaned_data["contact_email"]

            booking.save()

            messages.success(

                request,

                "Dziękujemy! Rezerwacja została przyjęta. Na podany adres e-mail wyślemy potwierdzenie.",

            )

            if request.user.is_authenticated:

                return redirect("MyReservations")

            return redirect("Home")

        messages.error(request, "Popraw pola oznaczone jako wymagane i spróbuj ponownie.")

    else:

        initial = {}

        if request.user.is_authenticated:

            initial["Name"] = request.user.first_name or ""

            initial["Surname"] = request.user.last_name or ""

        ci = request.GET.get("check_in", "")

        co = request.GET.get("check_out", "")

        if ci:

            initial["Check_in"] = ci

        if co:

            initial["Check_out"] = co

        form = OnlineBookingForm(user=request.user, initial=initial)



    return render(

        request,

        "online_booking_page.html",

        {

            "form": form,

            "catalog_rooms": rooms,

        },

    )





def Aothur_login(request):

    if request.user.is_authenticated:

        if request.user.is_staff:

            return redirect('StaffPanel')

        return redirect('Home')



    if request.method == 'POST':

        identifier = request.POST.get('Email')

        password = request.POST.get('Password')



        user = authenticate(request, username=identifier, password=password)



        if user is None:

            try:

                user_obj = User.objects.get(email=identifier)

                user = authenticate(request, username=user_obj.username, password=password)

            except User.DoesNotExist:

                user = None



        if user is not None:

            login(request, user)

            next_url = request.GET.get('next') or request.POST.get('next')

            if next_url and next_url.startswith('/'):

                return redirect(next_url)

            if user.is_staff:

                return redirect('StaffPanel')

            return redirect('Home')

        messages.error(request, "Błędny e-mail/login lub hasło!")



    return render(request, 'Athur_login_page.html')





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





@require_POST

def Logout_user(request):

    logout(request)

    return redirect('Home')

