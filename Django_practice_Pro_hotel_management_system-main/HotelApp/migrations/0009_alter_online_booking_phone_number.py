from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("HotelApp", "0008_online_booking_room_type_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="online_booking",
            name="Phone_Number",
            field=models.CharField(max_length=64),
        ),
    ]
