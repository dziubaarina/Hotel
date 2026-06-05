"""Lista kont z uprawnieniami pracownika panelu (is_staff, bez superusera)."""

from django.contrib.auth.models import User

from .models import Add_Employee, Online_Booking


def panel_employees_queryset():
    return User.objects.filter(is_staff=True, is_superuser=False).order_by("email", "username")


def contact_phone_for_user(user):
    email = (user.email or user.username or "").strip()
    if not email:
        return "—"
    hr = Add_Employee.objects.filter(Email__iexact=email).first()
    if hr and hr.Mobile_Number:
        return f"+{hr.Mobile_Number}"
    booking = (
        Online_Booking.objects.filter(Email__iexact=email)
        .exclude(Phone_Number="")
        .order_by("-Date", "-Id")
        .first()
    )
    if booking and booking.Phone_Number:
        return booking.Phone_Number
    return "—"


def panel_employee_rows():
    rows = []
    for user in panel_employees_queryset():
        email = user.email or user.username
        rows.append(
            {
                "user": user,
                "name": user.get_full_name().strip() or "—",
                "email": email,
                "phone": contact_phone_for_user(user),
            }
        )
    return rows
