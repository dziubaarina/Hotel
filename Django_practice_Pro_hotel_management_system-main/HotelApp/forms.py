from django import forms
from . import models
from .availability import can_book


class OnlineBookingForm(forms.ModelForm):
    contact_email = forms.EmailField(
        required=False,
        label="Adres e-mail",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "jan.kowalski@example.pl",
            "autocomplete": "email",
        }),
    )

    class Meta:
        model = models.Online_Booking
        fields = [
            "Check_in", "Check_out", "Room_Type", "ADULT", "CHILDREN",
            "Name", "Surname", "Phone_Number", "City", "Country",
        ]
        widgets = {
            "Phone_Number": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "+48 123 456 789 lub dowolny format",
                "autocomplete": "tel",
            }),
        }

    def __init__(self, *args, user=None, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        if user and getattr(user, "is_authenticated", False):
            self.fields["contact_email"].required = False
            self.fields["contact_email"].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get("Check_in")
        check_out = cleaned_data.get("Check_out")
        if check_in and check_out and str(check_in) >= str(check_out):
            raise forms.ValidationError("Data wyjazdu musi być późniejsza niż data przyjazdu.")
        room_type = cleaned_data.get("Room_Type")
        if room_type and check_in and check_out:
            if not can_book(room_type, check_in, check_out):
                raise forms.ValidationError(
                    f"Brak wolnych miejsc w kategorii „{room_type}” w wybranym terminie. "
                    "Wybierz inne daty lub typ pokoju."
                )
        user = self.user
        if not user or not getattr(user, "is_authenticated", False):
            if not cleaned_data.get("contact_email"):
                self.add_error(
                    "contact_email",
                    "Podaj adres e-mail — wyślemy na niego potwierdzenie rezerwacji.",
                )
        return cleaned_data

    def clean_Phone_Number(self):
        raw = self.cleaned_data.get("Phone_Number")
        if raw is None:
            return raw
        value = str(raw).strip()
        if len(value) < 3:
            raise forms.ValidationError("Podaj numer telefonu (min. 3 znaki).")
        if len(value) > 64:
            raise forms.ValidationError("Numer telefonu jest za długi (max. 64 znaki).")
        return value


class offline_Booking_form(forms.ModelForm):
    class Meta:
        model = models.Offline_Booking
        fields = "__all__"


class Add_Employee_form(forms.ModelForm):
    class Meta:
        model = models.Add_Employee
        fields = "__all__"


class StaffRoomForm(forms.ModelForm):
    """Edycja ogłoszenia pokoju (opis, cena, limit, zdjęcie) — bez dodawania nowych typów."""

    class Meta:
        model = models.Add_Room
        fields = [
            "Room_Price",
            "Room_Facility",
            "Room_Capacity",
            "Room_Image",
        ]
        widgets = {
            "Room_Price": forms.TextInput(attrs={"class": "form-control", "placeholder": "1200"}),
            "Room_Facility": forms.Textarea(
                attrs={"class": "form-control", "rows": 4, "placeholder": "Opis oferty na stronie…"}
            ),
            "Room_Capacity": forms.NumberInput(
                attrs={"class": "form-control", "min": 1, "max": 99}
            ),
            "Room_Image": forms.FileInput(attrs={"class": "form-control"}),
        }
        labels = {
            "Room_Facility": "Opis / ogłoszenie",
            "Room_Capacity": "Limit pokoi tego typu (na noc)",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["Room_Image"].required = False
        if self.instance and self.instance.pk:
            self.fields["Room_Capacity"].help_text = (
                f"Typ: {self.instance.Room_Type} · numer katalogowy {self.instance.Room_Number}"
            )


class Add_Room_form(forms.ModelForm):
    class Meta:
        model = models.Add_Room
        fields = "__all__"


class Add_salary_form(forms.ModelForm):
    class Meta:
        model = models.Add_Salarys
        fields = "__all__"
