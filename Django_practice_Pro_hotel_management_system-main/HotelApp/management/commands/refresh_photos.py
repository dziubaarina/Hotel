"""Pobiera zdjęcia wg scripts/download_hotel_images.py i aktualizuje wersję cache."""
import importlib.util
import time
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Pobiera zdjęcia hotelowe do static/Allfiles/Photo/ (wg download_hotel_images.py)."

    def handle(self, *args, **options):
        script = Path(settings.BASE_DIR) / "scripts" / "download_hotel_images.py"
        spec = importlib.util.spec_from_file_location("download_hotel_images", script)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        ok, fail = 0, 0
        for name, url in module.IMAGES.items():
            try:
                module.download_image(name, url)
                ok += 1
            except Exception as exc:
                self.stderr.write(self.style.ERROR(f"FAIL {name}: {exc}"))
                fail += 1

        version_file = (
            Path(settings.BASE_DIR) / "static" / "Allfiles" / "Photo" / ".asset_version"
        )
        version_file.write_text(str(int(time.time())), encoding="utf-8")

        self.stdout.write(self.style.SUCCESS(f"Zaktualizowano {ok} plików, błędów: {fail}."))
        if fail:
            self.stdout.write("Sprawdź FAIL w download_hotel_images.py (np. zły link Unsplash).")
        self.stdout.write("Odśwież stronę: Ctrl+F5.")
