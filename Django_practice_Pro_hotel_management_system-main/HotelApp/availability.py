"""Obłożenie pokoi wg typu i zakresu dat (nocleg: check_in włącznie, check_out wyłącznie)."""

from datetime import date, datetime, timedelta

from .models import Add_Room, Online_Booking

DATE_FMT = "%Y-%m-%d"
CANCEL_MIN_DAYS_BEFORE_ARRIVAL = 2


def parse_date(value):
    if value is None:
        return None
    if isinstance(value, date):
        return value
    text = str(value).strip()[:10]
    for fmt in (DATE_FMT, "%d.%m.%Y", "%d/%m/%Y"):
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            continue
    return None


def guest_can_cancel_booking(check_in, min_days=CANCEL_MIN_DAYS_BEFORE_ARRIVAL):
    """Gość może anulować tylko gdy do przyjazdu zostało więcej niż min_days dni."""
    check_in_date = parse_date(check_in)
    if not check_in_date:
        return False
    from django.utils import timezone

    today = timezone.localdate()
    return (check_in_date - today).days > min_days


def iter_nights(check_in, check_out):
    start = parse_date(check_in)
    end = parse_date(check_out)
    if not start or not end or start >= end:
        return
    night = start
    while night < end:
        yield night
        night += timedelta(days=1)


def _booking_covers_night(booking, night):
    start = parse_date(booking.Check_in)
    end = parse_date(booking.Check_out)
    if not start or not end:
        return False
    return start <= night < end


def count_on_night(room_type, night, exclude_booking_id=None):
    qs = Online_Booking.objects.filter(Room_Type=room_type)
    if exclude_booking_id:
        qs = qs.exclude(Id=exclude_booking_id)
    return sum(1 for b in qs if _booking_covers_night(b, night))


def get_capacity(room_type):
    room = Add_Room.objects.filter(Room_Type=room_type).first()
    if room and getattr(room, "Room_Capacity", None):
        return int(room.Room_Capacity)
    from .room_data import ROOM_TYPE_CAPACITY

    return int(ROOM_TYPE_CAPACITY.get(room_type, 1))


def can_book(room_type, check_in, check_out, exclude_booking_id=None):
    capacity = get_capacity(room_type)
    if capacity < 1:
        return False
    for night in iter_nights(check_in, check_out):
        if count_on_night(room_type, night, exclude_booking_id) >= capacity:
            return False
    return True


def peak_occupancy(room_type, check_in, check_out, exclude_booking_id=None):
    peak = 0
    for night in iter_nights(check_in, check_out):
        peak = max(peak, count_on_night(room_type, night, exclude_booking_id))
    return peak


def occupancy_summary(room_type, check_in, check_out, exclude_booking_id=None):
    capacity = get_capacity(room_type)
    occupied = peak_occupancy(room_type, check_in, check_out, exclude_booking_id)
    free = max(0, capacity - occupied)
    return {
        "room_type": room_type,
        "capacity": capacity,
        "occupied": occupied,
        "free": free,
        "full": occupied >= capacity,
        "label": f"{occupied}/{capacity}",
    }


def all_room_types():
    types = list(
        Add_Room.objects.order_by("Room_Number").values_list("Room_Type", flat=True)
    )
    if types:
        return types
    from .room_data import ROOM_CATALOG

    return [item["Room_Type"] for item in ROOM_CATALOG]


def occupancy_for_period(check_in, check_out):
    results = []
    for room_type in all_room_types():
        results.append(occupancy_summary(room_type, check_in, check_out))
    return results


def blocked_checkin_dates(room_type, days_ahead=365, exclude_booking_id=None):
    """Daty, w których nie można rozpocząć pobytu (ta noc już pełna)."""
    capacity = get_capacity(room_type)
    today = date.today()
    blocked = []
    for i in range(days_ahead):
        night = today + timedelta(days=i)
        if count_on_night(room_type, night, exclude_booking_id) >= capacity:
            blocked.append(night.strftime(DATE_FMT))
    return blocked


def blocked_checkout_dates(room_type, check_in, days_ahead=365, exclude_booking_id=None):
    """Daty wyjazdu, przy których któraś noc w [check_in, check_out) przekroczy limit."""
    start = parse_date(check_in)
    if not start:
        return []
    capacity = get_capacity(room_type)
    blocked = []
    for i in range(1, days_ahead + 1):
        end = start + timedelta(days=i)
        ok = True
        for night in iter_nights(start, end):
            if count_on_night(room_type, night, exclude_booking_id) >= capacity:
                ok = False
                break
        if not ok:
            blocked.append(end.strftime(DATE_FMT))
    return blocked


def blocked_checkin_all_types(days_ahead=365, exclude_booking_id=None):
    """Daty, w których wszystkie kategorie są pełne (żadnej nie można zacząć pobytu)."""
    today = date.today()
    types = all_room_types()
    blocked = []
    for i in range(days_ahead):
        night = today + timedelta(days=i)
        if not types:
            continue
        all_full = True
        for rt in types:
            if count_on_night(rt, night, exclude_booking_id) < get_capacity(rt):
                all_full = False
                break
        if all_full:
            blocked.append(night.strftime(DATE_FMT))
    return blocked


def availability_payload(check_in=None, check_out=None, room_type=None, exclude_booking_id=None):
    types_data = []
    for rt in all_room_types():
        cap = get_capacity(rt)
        if check_in and check_out:
            summary = occupancy_summary(rt, check_in, check_out, exclude_booking_id)
            available = not summary["full"] and can_book(
                rt, check_in, check_out, exclude_booking_id
            )
        else:
            summary = {"occupied": 0, "free": cap, "full": False, "label": f"0/{cap}"}
            available = True
        types_data.append(
            {
                "room_type": rt,
                "capacity": cap,
                "occupied": summary["occupied"],
                "free": summary["free"],
                "full": summary["full"],
                "label": summary["label"],
                "available": available,
            }
        )

    payload = {
        "check_in": check_in or "",
        "check_out": check_out or "",
        "room_types": types_data,
        "blocked_checkin_all": blocked_checkin_all_types(
            exclude_booking_id=exclude_booking_id
        ),
    }

    if room_type:
        payload["blocked_checkin"] = blocked_checkin_dates(
            room_type, exclude_booking_id=exclude_booking_id
        )
        if check_in:
            payload["blocked_checkout"] = blocked_checkout_dates(
                room_type, check_in, exclude_booking_id=exclude_booking_id
            )
        else:
            payload["blocked_checkout"] = []

    return payload
