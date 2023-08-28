# Generated by Django 4.2.4 on 2023-08-28 12:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ebs_app", "0010_remove_ticket_is_locked"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="booking",
            name="count",
        ),
        migrations.RemoveField(
            model_name="booking",
            name="ticket",
        ),
        migrations.AddField(
            model_name="booking",
            name="sub_bookings",
            field=models.JSONField(default=list),
        ),
    ]