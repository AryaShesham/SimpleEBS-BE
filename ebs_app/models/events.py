from django.db import models
from users.event_organiser.models import EventOrganiser


class Event(models.Model):
    event_name = models.CharField(max_length=128, null=False, blank=False)
    event_description = models.TextField(blank=True)
    event_date_time = models.DateTimeField(null=False, blank=False)
    venue = models.CharField(max_length=512, null=False, blank=True)
    event_organiser = models.ForeignKey(EventOrganiser, null=True, on_delete=models.CASCADE)

    def __self__(self):
        return f"{self.id} - {self.event_name}"
