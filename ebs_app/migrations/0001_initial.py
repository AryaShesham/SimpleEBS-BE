# Generated by Django 4.2.4 on 2023-08-22 10:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("event_organiser", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Event",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("event_name", models.CharField(max_length=128)),
                ("event_description", models.TextField(blank=True)),
                ("event_date_time", models.DateTimeField()),
                ("venue", models.CharField(blank=True, max_length=512)),
                (
                    "event_organiser",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="event_organiser.eventorganiser",
                    ),
                ),
            ],
        ),
    ]
