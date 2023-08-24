from django.contrib import admin
from ebs_app.models.events import Event
from ebs_app.models.bookings import Booking
from ebs_app.models.tickets import Ticket

# Register your models here.
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["id", "event_name", "event_date_time", "venue"]


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ["id", "customer", "ticket", "count", "status"]


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ["id", "event", "ticket_type", "availability", "price"]
