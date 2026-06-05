"""Mapowanie pokoi na zdjęcia statyczne (spójne ze stroną główną)."""

ROOM_CATALOG = [
    {
        "Room_Number": "101",
        "Room_Type": "Pokój dla par",
        "Room_Floor": "1",
        "Room_Price": "1200",
        "Room_Capacity": 3,
        "Room_Facility": "Widok na Stare Miasto, łóżko king-size, minibar, śniadanie w cenie.",
        "photo": "room-1.jpg",
    },
    {
        "Room_Number": "102",
        "Room_Type": "Pokój jednoosobowy",
        "Room_Floor": "1",
        "Room_Price": "950",
        "Room_Capacity": 4,
        "Room_Facility": "Biurko, szybki internet, idealny dla podróży służbowych.",
        "photo": "room-2.jpg",
    },
    {
        "Room_Number": "201",
        "Room_Type": "Pokój dwuosobowy",
        "Room_Floor": "2",
        "Room_Price": "1100",
        "Room_Capacity": 4,
        "Room_Facility": "Dwa łóżka, balkon, przestrzeń dla dziecka.",
        "photo": "room-3.jpg",
    },
    {
        "Room_Number": "301",
        "Room_Type": "Apartament luksusowy",
        "Room_Floor": "3",
        "Room_Price": "1800",
        "Room_Capacity": 2,
        "Room_Facility": "Salon, wanna z hydromasażem, concierge 24/7.",
        "photo": "room-4.jpg",
    },
    {
        "Room_Number": "302",
        "Room_Type": "Apartament rodzinny",
        "Room_Floor": "3",
        "Room_Price": "2200",
        "Room_Capacity": 3,
        "Room_Facility": "Dwie sypialnie, aneks kuchenny, sofa.",
        "photo": "room-5.jpg",
    },
    {
        "Room_Number": "401",
        "Room_Type": "Apartament prezydencki",
        "Room_Floor": "4",
        "Room_Price": "3500",
        "Room_Capacity": 2,
        "Room_Facility": "Taras, salon jadalny, dedykowany concierge.",
        "photo": "room-6.jpg",
    },
]

ROOM_TYPE_CAPACITY = {item["Room_Type"]: item["Room_Capacity"] for item in ROOM_CATALOG}

ROOM_TYPE_PHOTOS = {item["Room_Type"]: item["photo"] for item in ROOM_CATALOG}


def static_photo_filename(room):
    """Nazwa pliku w Allfiles/Photo/ dla pokoju."""
    if room.Room_Type in ROOM_TYPE_PHOTOS:
        return ROOM_TYPE_PHOTOS[room.Room_Type]
    for item in ROOM_CATALOG:
        if item["Room_Number"] == room.Room_Number:
            return item["photo"]
    return "room-1.jpg"
