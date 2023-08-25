"""
Ticket Model
"""

from django.db import models
from ebs_app.models.choices import TicketChoices
from ebs_app.models.events import Event


class Ticket(models.Model):
    """
    Ticket Model:

    Represents a ticket for an event.

    Fields:
    - event (ForeignKey):
        The associated event for which the ticket is created.
    - ticket_type (CharField):
        The type of the ticket (e.g., GENERAL_ADMISSION, PREMIUM).
    - total_allotment (IntegerField):
        The total number of tickets allotted for this type.
    - availability (IntegerField):
        The current number of available tickets for booking.
    - price (IntegerField):
        The price of the ticket.

    Methods:
    - __str__(): Returns a formatted string representation of the ticket.

    Example Usage:
    ticket = Ticket.objects.get(pk=1)
    print(ticket)  # Output: "GENERAL_ADMISSION - Friday Party"
    """

    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=False, blank=False)
    ticket_type = models.CharField(
        max_length=51,
        choices=TicketChoices.choices,
        default=TicketChoices.GENERAL_ADMISSION,
    )
    total_allotment = models.IntegerField(default=100, null=False, blank=False)
    availability = models.IntegerField(default=0, null=False, blank=False)
    price = models.IntegerField(default=0, null=False, blank=False)

    def __str__(self):
        return f"{self.ticket_type} - {self.event.event_name}"
