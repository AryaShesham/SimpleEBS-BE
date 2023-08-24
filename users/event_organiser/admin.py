from django.contrib import admin
from users.event_organiser.models import EventOrganiser


@admin.register(EventOrganiser)
class EventOrganiserAdmin(admin.ModelAdmin):
    list_display = ["id", "user"]
