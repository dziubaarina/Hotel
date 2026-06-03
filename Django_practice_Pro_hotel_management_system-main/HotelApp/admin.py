from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.html import format_html

from .models import Add_Employee, Add_Room, Add_Salarys, Offline_Booking, Online_Booking


@admin.register(Online_Booking)
class OnlineBookingAdmin(admin.ModelAdmin):
    list_display = (
        "booking_id",
        "guest_full_name",
        "Room_Type",
        "Check_in",
        "Check_out",
        "Phone_Number",
        "Email",
        "Date",
    )
    list_filter = ("Room_Type", "Date", "Country", "City")
    search_fields = ("Name", "Surname", "Email", "Phone_Number", "Room_Type")
    readonly_fields = ("Date", "Time")
    ordering = ("-Date", "-Id")
    list_per_page = 20
    date_hierarchy = "Date"

    fieldsets = (
        ("Pobyt", {
            "fields": ("Check_in", "Check_out", "Room_Type", "ADULT", "CHILDREN"),
        }),
        ("Gość", {
            "fields": ("Name", "Surname", "Email", "Phone_Number"),
        }),
        ("Adres", {
            "fields": ("City", "Country", "Address", "Nid_No"),
            "classes": ("collapse",),
        }),
        ("Inne", {
            "fields": ("Img", "Date", "Time"),
            "classes": ("collapse",),
        }),
    )

    @admin.display(description="ID", ordering="Id")
    def booking_id(self, obj):
        return f"#{obj.Id}"

    @admin.display(description="Gość", ordering="Surname")
    def guest_full_name(self, obj):
        return f"{obj.Name} {obj.Surname}".strip()


@admin.register(Offline_Booking)
class OfflineBookingAdmin(admin.ModelAdmin):
    list_display = (
        "Customer_Id",
        "guest_name",
        "Select_Room",
        "Room_Number",
        "Check_in",
        "Check_out",
        "Email",
        "Date",
    )
    list_filter = ("Select_Room", "Gender", "Country", "Date")
    search_fields = (
        "First_Name",
        "Last_Name",
        "Email",
        "Room_Number",
        "Personal_Identity",
    )
    readonly_fields = ("Date", "Time")
    ordering = ("-Date",)

    @admin.display(description="Gość")
    def guest_name(self, obj):
        return f"{obj.First_Name} {obj.Last_Name}"


@admin.register(Add_Room)
class AddRoomAdmin(admin.ModelAdmin):
    list_display = (
        "Room_Number",
        "Room_Type",
        "Room_Floor",
        "Room_Price",
        "room_preview",
        "Date",
    )
    list_filter = ("Room_Type", "Room_Floor")
    search_fields = ("Room_Number", "Room_Type", "Room_Facility")
    readonly_fields = ("Date", "Time", "room_image_preview")
    ordering = ("Room_Number",)

    fieldsets = (
        ("Pokój", {
            "fields": (
                "Room_Number",
                "Room_Type",
                "Room_Floor",
                "Room_Price",
                "Room_Facility",
            ),
        }),
        ("Zdjęcie", {
            "fields": ("Room_Image", "room_image_preview"),
        }),
        ("Meta", {
            "fields": ("Date", "Time"),
            "classes": ("collapse",),
        }),
    )

    @admin.display(description="Zdjęcie")
    def room_preview(self, obj):
        if obj.Room_Image:
            return format_html(
                '<img src="{}" style="height:40px;width:60px;object-fit:cover;border-radius:4px;" />',
                obj.Room_Image.url,
            )
        return "—"

    @admin.display(description="Podgląd")
    def room_image_preview(self, obj):
        if obj.Room_Image:
            return format_html(
                '<img src="{}" style="max-width:320px;border-radius:8px;" />',
                obj.Room_Image.url,
            )
        return "Brak zdjęcia"


@admin.register(Add_Employee)
class AddEmployeeAdmin(admin.ModelAdmin):
    list_display = (
        "Employee_Id",
        "First_Name",
        "Last_Name",
        "Departments",
        "Email",
        "Mobile_Number",
        "Joining_Date",
    )
    list_filter = ("Departments", "Gender", "Blood_Group")
    search_fields = (
        "Employee_Id",
        "First_Name",
        "Last_Name",
        "Email",
        "Personal_Identity",
    )
    readonly_fields = ("Date", "Time")
    ordering = ("Departments", "Last_Name")


@admin.register(Add_Salarys)
class AddSalaryAdmin(admin.ModelAdmin):
    list_display = (
        "Employee_Id",
        "Employee_Name",
        "Departments",
        "Salary",
        "Email",
        "Date",
    )
    list_filter = ("Departments", "Date")
    search_fields = ("Employee_Name", "Email", "Employee_Id__Employee_Id")
    readonly_fields = ("Date", "Time")
    autocomplete_fields = ("Employee_Id",)


def aladu_admin_dashboard_context(request):
    """Statystyki na stronie głównej panelu admina."""
    return {
        "booking_count": Online_Booking.objects.count(),
        "room_count": Add_Room.objects.count(),
        "employee_count": Add_Employee.objects.count(),
        "user_count": User.objects.count(),
    }


# Rozszerzenie domyślnego widoku index admina o statystyki
_original_admin_index = admin.site.index


def aladu_admin_index(request, extra_context=None):
    extra_context = extra_context or {}
    extra_context.update(aladu_admin_dashboard_context(request))
    return _original_admin_index(request, extra_context)


admin.site.index = aladu_admin_index
