from django.db import models
from ebs_app.models.choices import TicketChoices
from ebs_app.models.events import Event


class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=False, blank=False)
    ticket_type = models.CharField(max_length=51,
                                   choices=TicketChoices.choices,
                                   default=TicketChoices.GENERAL_ADMISSION)
    total_allotment = models.IntegerField(default=100, null=False, blank=False)
    availability = models.IntegerField(default=0, null=False, blank=False)
    price = models.IntegerField(default=0, null=False, blank=False)

    def __str__(self):
        return f"{self.ticket_type} - {self.event.event_name}"
