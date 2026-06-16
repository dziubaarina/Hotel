# Hotel Aladu — system rezerwacji i zarządzania hotelem

Aplikacja webowa dla butikowego hotelu pięciogwiazdkowego w Krakowie. Goście przeglądają ofertę i rezerwują pokoje online; personel obsługuje rezerwacje i obłożenie w panelu zintegrowanym ze stroną hotelu.

**Stack:** Django 4.2 · SQLite · Bootstrap · Jazzmin (opcjonalny backend `/admin/`)

---

## Wymagania

- Python 3.10 lub nowszy
- Windows / Linux / macOS

---

## Instalacja i uruchomienie

Repozytorium zakłada wirtualne środowisko w katalogu nadrzędnym (`Aladu/venv`).

### Windows (PowerShell)

```powershell
Set-Location "C:\ścieżka\do\Aladu\Django_practice_Pro_hotel_management_system-main"

# Zależności (venv jeden poziom wyżej)
& "..\venv\Scripts\python.exe" -m pip install -r requirements.txt

# Baza danych
& "..\venv\Scripts\python.exe" manage.py migrate

# Dane startowe (pokoje + zespół na stronie głównej)
& "..\venv\Scripts\python.exe" manage.py seed_rooms
& "..\venv\Scripts\python.exe" manage.py seed_team

# Konto administratora (superuser = pełny dostęp do panelu)
& "..\venv\Scripts\python.exe" manage.py createsuperuser

# Serwer deweloperski
& "..\venv\Scripts\python.exe" manage.py runserver
```

### Linux / macOS

```bash
cd Django_practice_Pro_hotel_management_system-main
source ../venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_rooms
python manage.py seed_team
python manage.py createsuperuser
python manage.py runserver
```

Aplikacja: **http://127.0.0.1:8000/**

---

## Adresy w aplikacji

| Strona | URL |
|--------|-----|
| Strona główna | http://127.0.0.1:8000/ |
| Rezerwacja online | http://127.0.0.1:8000/OnlineBooking/ |
| Moje rezerwacje | http://127.0.0.1:8000/moje-rezerwacje/ |
| Logowanie | http://127.0.0.1:8000/Aothur_login/ |
| Rejestracja | http://127.0.0.1:8000/Athur_Register/ |
| Panel zarządzania | http://127.0.0.1:8000/panel/ |
| API dostępności pokoi | http://127.0.0.1:8000/api/dostepnosc/ |
| Wersja angielska | http://127.0.0.1:8000/en/ |
| Django Admin (techniczny) | http://127.0.0.1:8000/admin/ |

---

## Role użytkowników

| Rola | Opis | Dostęp |
|------|------|--------|
| **Gość** | Konto z rejestracji lub rezerwacja bez logowania | Strona publiczna, własne rezerwacje |
| **Pracownik** | `is_staff=True`, bez superusera | Panel: przegląd, rezerwacje, obłożenie pokoi, lista pracowników |
| **Administrator** | `is_superuser=True` | Wszystko u pracownika + edycja ogłoszeń pokoi + nadawanie/odbieranie uprawnień pracownika |

Nadawanie roli pracownika: panel → zakładka **Uprawnienia** (tylko administrator). Wpisz e-mail istniejącego konta gościa.

Po logowaniu personel trafia na `/panel/`.

---

## Główne funkcje

### Strona publiczna
- Prezentacja hotelu: hero, pokoje, udogodnienia, galeria, zespół
- Filtrowanie dostępności pokoi według dat na stronie głównej
- Rezerwacja online z walidacją obłożenia (typ pokoju znika przy pełnym limicie)
- Rejestracja i logowanie gości
- Podgląd i anulowanie własnych rezerwacji
- Język polski i angielski (i18n)

### Obłożenie pokoi
Każdy **typ pokoju** ma limit miejsc na noc (np. 3× „Pokój dla par”). Rezerwacja zajmuje jedno miejsce na każdą noc pobytu. Przy limicie **3/3** dany typ nie jest dostępny w wybranym terminie.

Domyślne limity (po `seed_rooms`):

| Typ pokoju | Limit |
|------------|-------|
| Pokój dla par | 3 |
| Pokój jednoosobowy | 4 |
| Pokój dwuosobowy | 4 |
| Apartament luksusowy | 2 |
| Apartament rodzinny | 3 |
| Apartament prezydencki | 2 |

### Panel zarządzania (`/panel/`)
- **Przegląd** — statystyki rezerwacji, pokoi, kont
- **Rezerwacje** — lista i usuwanie zgłoszeń online
- **Pokoje** — obłożenie w wybranym zakresie dat; administrator edytuje ceny, opisy i limity
- **Pracownicy** — lista kont z uprawnieniami pracownika (e-mail, kontakt)
- **Uprawnienia** — tylko administrator

---

## Komendy zarządzania

```powershell
& "..\venv\Scripts\python.exe" manage.py seed_rooms      # 6 typów pokoi w bazie
& "..\venv\Scripts\python.exe" manage.py seed_team       # 5 osób w sekcji „Nasz zespół”
& "..\venv\Scripts\python.exe" manage.py refresh_photos  # pobranie zdjęć (Unsplash) + wersja cache
```

Skrypt pomocniczy zdjęć: `scripts/download_hotel_images.py`

---

## Struktura projektu

```
Django_practice_Pro_hotel_management_system-main/
├── HotelApp/                 # aplikacja Django
│   ├── models.py             # pokoje, rezerwacje, zespół
│   ├── views.py              # widoki publiczne i panelu
│   ├── availability.py       # logika obłożenia
│   ├── roles.py              # role admin / pracownik
│   └── management/commands/  # seed_rooms, seed_team, refresh_photos
├── HotelManagementSystem/    # settings, urls główne
├── templates/                # szablony HTML (Home, panel, rezerwacja…)
├── static/Allfiles/          # CSS, JS, zdjęcia
├── media/                    # uploady (zdjęcia pokoi)
├── locale/                   # tłumaczenia PL/EN
├── scripts/                  # skrypty pomocnicze
├── db.sqlite3                # baza SQLite (po migrate)
└── requirements.txt
```

---

## Konfiguracja (opcjonalnie)

Zmienne środowiskowe:

| Zmienna | Domyślnie | Opis |
|---------|-----------|------|
| `DJANGO_SECRET_KEY` | klucz deweloperski w settings | Sekret produkcyjny |
| `DJANGO_DEBUG` | `True` | Tryb debug |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1` | Dozwolone hosty |

---

## Uwagi techniczne

- Baza: **SQLite** — wystarczająca do developmentu i prezentacji; na produkcję rozważ PostgreSQL.
- Zdjęcia statyczne: `static/Allfiles/Photo/` — po `refresh_photos` cache busting przez `?v=` w URL.
- Stare szablony admina: `templates/_legacy/`.
- Panel Jazzmin pod `/admin/` pozostaje jako backend techniczny; codzienna praca odbywa się w `/panel/`.

---

## Zespół projektowy

Projekt zespołowy — **Hotel Aladu**, semestr 6, studia.
