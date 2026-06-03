from pathlib import Path

p = Path(__file__).resolve().parent.parent / "templates" / "Home.html"
t = p.read_text(encoding="utf-8")

t = t.replace(
    '                         <h1 >{% trans "welcome to" %} <span class="late">Aladu Hotel</span> </h1>\n'
    '                         <p> {% trans "Welcome to Hotel Booking Management, your one-stop solution for hassle-free hotel reservations.Quickly find the perfect hotel for your next stay. Use our search tool to browse and book hotels in the area." %}</p>\n'
    '                          <motion></motion>\n'
    '                          <div class="slider-btn">\n'
    '                               <a class="default-btn" href="#OUR_ROOMS" >{% trans "explore" %}</a>\n'
    '                          </div>',
    '                         <span class="hero-badge">Hotel 5★ · Kraków</span>\n'
    '                         <h1>Witamy w <span class="late">Hotelu Aladu</span></h1>\n'
    '                         <p>Przestronne pokoje, restauracja z kuchnią autorską i obsługa na najwyższym poziomie. Przeglądaj ofertę bez logowania.</p>\n'
    '                          <div class="slider-btn">\n'
    '                               <a class="default-btn" href="#OUR_ROOMS">Poznaj pokoje</a>\n'
    '                               <a class="default-btn btn-outline-light" href="{% url \'OnlineBooking\' %}">Zarezerwuj pobyt</a>\n'
    '                          </div>',
    1,
)

replacements = [
    ('{% trans "Enjoy a luxury experience" %}', 'Luksus w sercu Krakowa'),
    ('<h4> {% trans "Hotel" %}</h4>', '<p>Basen, spa i restauracja — kilka kroków od Rynku Głównego.</p>'),
    ('{% trans "Spend Quality Holidays With Us" %}', 'Wyjątkowe chwile z bliskimi'),
    ('{% trans "The best way to spend your precious time and cherish every moment with your loved ones. Join Today!" %}', 'Komfort od pierwszej chwili. Bezpieczna rezerwacja online.'),
    ('{% trans "About Us" %}', 'O hotelu'),
    ('{% trans "EXPLORE OUR ROOMS" %}', 'Nasze pokoje'),
    ('{% trans "OUR AWESOME SERVICES" %}', 'Udogodnienia hotelu'),
    ('{% trans "OUR GALLERY" %}', 'Galeria'),
    ('{% trans "OUR SPECIAL STAFF" %}', 'Nasz zespół'),
    ('{% trans "Couple Room" %}', 'Pokój dla par'),
    ('{% trans "Single Room" %}', 'Pokój jednoosobowy'),
    ('{% trans "Double Room" %}', 'Pokój dwuosobowy'),
    ('{% trans "Luxury Room" %}', 'Apartament luksusowy'),
    ('{% trans "Family Room" %}', 'Apartament rodzinny'),
    ('{% trans "Presidential Room" %}', 'Apartament prezydencki'),
    ('{% trans "BOOKING Now" %}', 'Zarezerwuj'),
    ('{% trans "Swimming Pool" %}', 'Basen i strefa relaksu'),
    ('{% trans "Spa, beauty & Health" %}', 'Spa i wellness'),
    ('{% trans "Restaurant" %}', 'Restauracja'),
    ('{% trans "Conference Hall" %}', 'Sale konferencyjne'),
    ('{% trans "Manager" %}', 'Dyrektor hotelu'),
    ('{% trans "Reception Officer" %}', 'Recepcja'),
    ('{% trans "Master Chef" %}', 'Szef kuchni'),
    ('{% trans "Housekeeping" %}', 'Housekeeping'),
    ('Shirley Gibson', 'Anna Kowalska'),
    ('Ronald Long', 'Marek Nowak'),
    ('Ashley Sanchez', 'Katarzyna Wiśniewska'),
    ('Jessica Watson', 'Ewa Zielińska'),
    ('{% trans "Happy Clients" %}', 'Zadowolonych gości'),
    ('{% trans "New Friendships" %}', 'Powracających klientów'),
    ('{% trans "Five Start Ratings" %}', 'Ocen pięć gwiazdek'),
    ('{% trans "Served Breakfast" %}', 'Śniadań serwowanych'),
]

for old, new in replacements:
    t = t.replace(old, new)

p.write_text(t.replace("<motion></motion>", "").replace("</motion>", ""), encoding="utf-8")
print("done")
