from django.contrib import admin
from ebs_app.models.events import Event
from ebs_app.models.bookings import Booking
from ebs_app.models.tickets import Ticket

# Register your models here.
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """
    Admin class for managing Event models.

    This admin class allows managing Event objects in the Django admin interface.
    It defines the list display fields to be shown in the admin list view.

    List Display Fields:
    - id: The primary key of the event.
    - event_name: The name of the event.
    - event_date_time: The date and time of the event.
    - venue: The venue where the event will take place.
    """

    list_display = ["id", "event_name", "event_date_time", "venue"]


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """
    Admin class for managing Booking models.

    This admin class allows managing Booking objects in the Django admin interface.
    It defines the list display fields to be shown in the admin list view.

    List Display Fields:
    - id: The primary key of the booking.
    - customer: The customer who made the booking.
    - ticket: The ticket associated with the booking.
    - count: The number of seats booked.
    - status: The booking status.
    """

    list_display = ["id", "customer", "ticket", "count", "status"]


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    """
    Admin class for managing Ticket models.

    This admin class allows managing Ticket objects in the Django admin interface.
    It defines the list display fields to be shown in the admin list view.

    List Display Fields:
    - id: The primary key of the ticket.
    - event: The event associated with the ticket.
    - ticket_type: The type of the ticket.
    - availability: The number of available tickets.
    - price: The price of the ticket.
    """

    list_display = ["id", "event", "ticket_type", "availability", "price"]
