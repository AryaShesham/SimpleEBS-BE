from rest_framework.serializers import ModelSerializer
from users.event_organiser.models import EventOrganiser
from users.serliazers import UserSerializer


class EventOrganiserSerializers(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = EventOrganiser
        fields = "__all__"
