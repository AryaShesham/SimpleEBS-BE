# Generated by Django 4.2.4 on 2023-08-28 11:35

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("ebs_app", "0009_ticket_is_locked"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="ticket",
            name="is_locked",
        ),
    ]
