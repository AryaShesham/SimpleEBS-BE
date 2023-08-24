"""
Event Serializer
"""

from rest_framework.serializers import ModelSerializer
from ebs_app.models.events import  Event
from users.event_organiser.serializers import EventOrganiserSerializers

class EventSerializer(ModelSerializer):

    event_organiser = EventOrganiserSerializers(read_only=True)
    class Meta:
        model = Event
        fields = "__all__"