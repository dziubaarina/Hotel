from functools import wraps

from django.contrib.auth.views import redirect_to_login
from django.contrib import messages
from django.shortcuts import redirect

from .roles import is_hotel_admin, is_hotel_staff


def staff_required(view_func):
    """Dostęp dla personelu (pracownik lub administrator)."""

    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        user = request.user
        if is_hotel_staff(user):
            return view_func(request, *args, **kwargs)
        return redirect_to_login(request.get_full_path(), "Aothur_login")

    return _wrapped


def admin_required(view_func):
    """Tylko administrator hotelu (superuser)."""

    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return redirect_to_login(request.get_full_path(), "Aothur_login")
        if not is_hotel_admin(user):
            messages.error(request, "Ta operacja wymaga uprawnień administratora.")
            return redirect("StaffPanel")
        return view_func(request, *args, **kwargs)

    return _wrapped
