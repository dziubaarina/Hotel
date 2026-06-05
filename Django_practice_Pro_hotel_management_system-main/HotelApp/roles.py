"""Role w panelu: administrator (superuser) vs pracownik (is_staff)."""


def is_hotel_admin(user):
    return user.is_authenticated and user.is_superuser


def is_hotel_employee(user):
    return user.is_authenticated and user.is_staff and not user.is_superuser


def is_hotel_staff(user):
    return user.is_authenticated and user.is_staff


def role_label(user):
    if not user.is_authenticated:
        return "Gość"
    if is_hotel_admin(user):
        return "Administrator"
    if is_hotel_employee(user):
        return "Pracownik"
    return "Gość"
