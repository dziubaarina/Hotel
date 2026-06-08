# Aladu — Hotel Aladu

System rezerwacji i zarządzania hotelem (Django). Szczegółowa dokumentacja:

*[Django_practice_Pro_hotel_management_system-main/README.md](Django_practice_Pro_hotel_management_system-main/README.md)*

## Szybki start (Windows)

Set-Location "Django_practice_Pro_hotel_management_system-main"
& "..\venv\Scripts\python.exe" -m pip install -r requirements.txt
& "..\venv\Scripts\python.exe" manage.py migrate
& "..\venv\Scripts\python.exe" manage.py seed_rooms
& "..\venv\Scripts\python.exe" manage.py seed_team
& "..\venv\Scripts\python.exe" manage.py createsuperuser
& "..\venv\Scripts\python.exe" manage.py runserver

Strona: http://127.0.0.1:8000/ · Panel: http://127.0.0.1:8000/panel/
