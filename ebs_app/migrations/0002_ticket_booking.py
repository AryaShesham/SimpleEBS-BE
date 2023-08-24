# Generated by Django 4.2.4 on 2023-08-22 12:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("customer", "0001_initial"),
        ("ebs_app", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Ticket",
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
                (
                    "ticket_type",
                    models.CharField(
                        choices=[
                            ("GENERAL_ADMISSION", "General Admission"),
                            ("VIP", "VIP"),
                            ("PREMIUM", "Premium"),
                            ("SUPER_DELUX", "Super Delux"),
                            ("ROYAL", "Royal"),
                        ],
                        default="GENERAL_ADMISSION",
                        max_length=51,
                    ),
                ),
                ("availability", models.IntegerField(default=0)),
                ("price", models.IntegerField(default=0)),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="ebs_app.event"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Booking",
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
                ("count", models.IntegerField(default=0)),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="customer.customer",
                    ),
                ),
                (
                    "ticket",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="ebs_app.ticket"
                    ),
                ),
            ],
        ),
    ]
