from django import template
from django.templatetags.static import static

from HotelApp.room_data import static_photo_filename
from HotelApp.team_data import static_team_photo

register = template.Library()


@register.simple_tag
def room_photo_url(room):
    if room.Room_Image:
        return room.Room_Image.url
    name = static_photo_filename(room)
    return static(f"Allfiles/Photo/{name}")


@register.simple_tag
def team_photo_url(employee):
    if employee.Upload_Image:
        return employee.Upload_Image.url
    name = static_team_photo(employee) or "team1.jpg"
    return static(f"Allfiles/Photo/{name}")
