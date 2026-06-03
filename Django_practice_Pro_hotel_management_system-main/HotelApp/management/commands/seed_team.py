from django.core.management.base import BaseCommand

from HotelApp.models import Add_Employee
from HotelApp.team_data import TEAM_CATALOG


class Command(BaseCommand):
    help = "Dodaje 5 członków zespołu hotelu (jak na stronie głównej)."

    def handle(self, *args, **options):
        created = 0
        updated = 0
        for item in TEAM_CATALOG:
            data = {k: v for k, v in item.items() if k != "photo"}
            _, was_created = Add_Employee.objects.update_or_create(
                Employee_Id=item["Employee_Id"],
                defaults=data,
            )
            if was_created:
                created += 1
            else:
                updated += 1
        self.stdout.write(
            self.style.SUCCESS(
                f"Zespół: {created} nowych, {updated} zaktualizowanych "
                f"(łącznie {Add_Employee.objects.count()})."
            )
        )
