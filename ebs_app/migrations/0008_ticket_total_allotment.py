# Generated by Django 4.2.4 on 2023-08-24 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ebs_app", "0007_alter_booking_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="ticket",
            name="total_allotment",
            field=models.IntegerField(default=100),
        ),
    ]