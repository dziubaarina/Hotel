from pathlib import Path

from django.conf import settings

from .roles import is_hotel_admin, is_hotel_employee, is_hotel_staff


def asset_version(request):
    """Wersja cache zdjęć statycznych (?v=) po refresh_photos."""
    version_file = (
        Path(settings.BASE_DIR) / "static" / "Allfiles" / "Photo" / ".asset_version"
    )
    version = "1"
    if version_file.is_file():
        version = version_file.read_text(encoding="utf-8").strip() or "1"
    return {"PHOTO_CACHE_VERSION": version}


def hotel_roles(request):
    user = request.user
    if not user.is_authenticated:
        return {
            "is_hotel_admin": False,
            "is_hotel_employee": False,
            "is_hotel_staff": False,
        }
    return {
        "is_hotel_admin": is_hotel_admin(user),
        "is_hotel_employee": is_hotel_employee(user),
        "is_hotel_staff": is_hotel_staff(user),
    }
