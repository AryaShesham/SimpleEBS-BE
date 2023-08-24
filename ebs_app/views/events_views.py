from copy import copy
from rest_framework import viewsets, permissions
from ebs_app.models.events import Event
from ebs_app.models.bookings import Booking
from users.customer.models import Customer
from users.permissions import IsEventOrganiser
from users.event_organiser.models import EventOrganiser
from ebs_app.serializers.event_serializers import EventSerializer
from ebs_app.tasks import send_event_update_email

from ebs_app.exceptions import NotAuthorisedAPIException

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "delete"]:
            permission_classes = [permissions.IsAuthenticated, IsEventOrganiser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        event_organiser = EventOrganiser.objects.get(user=self.request.user)
        
        if event_organiser == None:
            raise NotAuthorisedAPIException()
        
        if serializer.is_valid(raise_exception=True):
            serializer.save(
                event_organiser=event_organiser,
            )
        return super().perform_create(serializer)

    def perform_update(self, serializer):

        event = self.get_object()
        breakpoint()
        event_bookings = Booking.objects.filter(ticket__event=event).values_list("customer__user__email").distinct()
        customer_email_list = [i[0] for i in event_bookings]

        serializer.save()
        serializer_copy = copy(serializer)
        updated_event = serializer_copy.data
        event_dict = {
        "event_name": updated_event["event_name"],
        "event_venue": updated_event["venue"],
        "event_time": updated_event["event_date_time"],
        }
        send_event_update_email.delay(event_dict, customer_email_list)
        return super().perform_update(serializer)