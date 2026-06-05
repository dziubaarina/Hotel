from django.core.management.base import BaseCommand

from HotelApp.models import Add_Room
from HotelApp.room_data import ROOM_CATALOG


class Command(BaseCommand):
    help = "Dodaje 6 pokoi hotelowych (zgodnych ze stroną główną), jeśli ich jeszcze nie ma."

    def handle(self, *args, **options):
        created = 0
        updated = 0
        for item in ROOM_CATALOG:
            room, was_created = Add_Room.objects.update_or_create(
                Room_Number=item["Room_Number"],
                defaults={
                    "Room_Type": item["Room_Type"],
                    "Room_Floor": item["Room_Floor"],
                    "Room_Price": item["Room_Price"],
                    "Room_Facility": item["Room_Facility"],
                    "Room_Capacity": item.get("Room_Capacity", 3),
                },
            )
            if was_created:
                created += 1
            else:
                updated += 1
        self.stdout.write(
            self.style.SUCCESS(
                f"Pokoje: {created} nowych, {updated} zaktualizowanych (łącznie {Add_Room.objects.count()})."
            )
        )
