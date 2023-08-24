"""
Event Model
"""

from django.db import models
from users.event_organiser.models import EventOrganiser


class Event(models.Model):
    """
    Event Model:

    Represents an event organized by an event organiser.

    Fields:
    - event_name (CharField): The name of the event.
    - event_description (TextField): A description of the event (optional).
    - event_date_time (DateTimeField): The date and time of the event.
    - venue (CharField): The venue where the event will take place.
    - event_organiser (ForeignKey): The event organiser associated with the event.

    Methods:
    - __str__(): Returns a formatted string representation of the event.

    Example Usage:
    event = Event.objects.get(pk=1)
    print(event)  # Output: "1 - Event Name"
    """

    event_name = models.CharField(max_length=128, null=False, blank=False)
    event_description = models.TextField(blank=True)
    event_date_time = models.DateTimeField(null=False, blank=False)
    venue = models.CharField(max_length=512, null=False, blank=True)
    event_organiser = models.ForeignKey(EventOrganiser, null=True, on_delete=models.CASCADE)

    def __self__(self):
        return f"{self.id} - {self.event_name}"
