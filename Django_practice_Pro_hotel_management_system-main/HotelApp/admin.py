from django.contrib import admin
# Importujemy wszystkie modele, które znalazłem w Twoim pliku models.py
from .models import Authorregis, Online_Booking, Offline_Booking, Add_Employee, Add_Room, Add_Salarys

# Rejestrujemy je, żeby pojawiły się w panelu admina
admin.site.register(Authorregis)
admin.site.register(Online_Booking)
admin.site.register(Offline_Booking)
admin.site.register(Add_Employee)
admin.site.register(Add_Room)
admin.site.register(Add_Salarys)