"""
Pobiera zdjęcia hotelowe z Unsplash do static/Allfiles/Photo/.

Uruchom z katalogu projektu:
python scripts/download_hotel_images.py
"""

from pathlib import Path
import urllib.request

BASE = Path(__file__).resolve().parent.parent / "static" / "Allfiles" / "Photo"
BASE.mkdir(parents=True, exist_ok=True)


def unsplash(photo_id: str, width: int = 1600) -> str:
    """
    Link do pobrania zdjęcia z Unsplash.
    Używamy endpointu /download, żeby nie wpisywać ręcznie długich CDN-owych URL-i.
    """
    return f"https://unsplash.com/photos/{photo_id}/download?force=true&w={width}"


IMAGES = {
    # Slider — Kraków, kamienice, miejski klimat, elegancki hotel
    "slider-1.jpg": unsplash("pfPdTlPNU5g", 1920),      # fasada w Krakowie
    "slider-2.jpg": unsplash("4YndQ8JI-oM", 1920),      # Rynek / stare miasto w Krakowie
    "slider-3.jpg": unsplash("2af7-TNSGzo", 1920),      # krakowska ulica
    "slider-4.jpg": unsplash("rB3Xmbu_2ww", 1920),      # budynek w Krakowie
    "slider-5.jpg": unsplash("V4ix9DJT0js", 1920),      # klimatyczne wejście / kawiarnia w Krakowie

    # Pokoje — neutralne, hotelowe, bez tropikalnego resortu
    "room-1.jpg": unsplash("CMHgRFDANH8", 1200),        # pokój w Polsce
    "room-2.jpg": "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?auto=format&fit=crop&w=1200&q=85",
    "room-3.jpg": "https://images.unsplash.com/photo-1590490360182-c33d57733427?auto=format&fit=crop&w=1200&q=85",
    "room-4.jpg": "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=1200&q=85",
    "room-5.jpg": "https://images.unsplash.com/photo-1618773928121-c32242e63f39?auto=format&fit=crop&w=1200&q=85",
    "room-6.jpg": "https://images.unsplash.com/photo-1566665797739-1674de7a421a?auto=format&fit=crop&w=1200&q=85",

    # Galeria — Kraków, restauracja, miejskie wnętrza
    "gallery-1.jpg": unsplash("V4ix9DJT0js", 900),      # wejście / lokal w Krakowie
    "gallery-2.jpg": unsplash("lt9_cvP9LNE", 900),      # kawiarnia / stare miasto Kraków
    "gallery-3.jpg": unsplash("qmIANkRwbkg", 900),      # restauracja w Krakowie
    "gallery-4.jpg": unsplash("ZpjIDWJboVA", 900),      # restauracja w Krakowie

    "gallery-1-pop.jpg": unsplash("V4ix9DJT0js", 1600),
    "gallery-2-pop.jpg": unsplash("lt9_cvP9LNE", 1600),
    "gallery-3-pop.jpg": unsplash("qmIANkRwbkg", 1600),
    "gallery-4-pop.jpg": unsplash("ZpjIDWJboVA", 1600),

    # Inne zdjęcia na stronę
    "video_pic.jpg": unsplash("4YndQ8JI-oM", 1200),
    "hotel-about.jpg": unsplash("pfPdTlPNU5g", 1200),
    "bg1.jpg": unsplash("2af7-TNSGzo", 1920),

    # Udogodnienia — bardziej hotelowo, mniej egzotycznie
    "service-1.png": unsplash("WL-OWCmg0zY", 800),      # basen hotelowy w Polsce
    "service-2.png": "https://images.unsplash.com/photo-1544161515-4ab6ce6db874?auto=format&fit=crop&w=800&q=85",
    "service-3.png": unsplash("ZpjIDWJboVA", 800),      # restauracja
    "service-4.png": unsplash("i_mxlC9hScU", 800),      # sala/event/wnętrze

    "swim.png": unsplash("WL-OWCmg0zY", 500),
    "spa.png": "https://images.unsplash.com/photo-1544161515-4ab6ce6db874?auto=format&fit=crop&w=500&q=85",
    "restaurent.png": unsplash("qmIANkRwbkg", 500),
    "conference.png": unsplash("i_mxlC9hScU", 500),

    # Portrety zespołu — zostawione neutralne biznesowe
    "team1.jpg": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=600&q=85",
    "team2.jpg": "https://images.unsplash.com/photo-1560250097-0b93528c311a?auto=format&fit=crop&w=600&q=85",
    "team3.jpg": "https://images.unsplash.com/photo-1580489944761-15a19d654956?auto=format&fit=crop&w=600&q=85",
    "team4.jpg": "https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?auto=format&fit=crop&w=600&q=85",
    "team5.jpg": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?auto=format&fit=crop&w=600&q=85",
}


def download_image(name: str, url: str) -> None:
    dest = BASE / name

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 AladuHotelAssetBot/1.0"
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            dest.write_bytes(response.read())

        print(f"OK   {name}")

    except Exception as error:
        print(f"FAIL {name}: {error}")


def main() -> None:
    for name, url in IMAGES.items():
        download_image(name, url)


if __name__ == "__main__":
    main()