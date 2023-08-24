"""
Module: ebs_app.views.event_views

This module contains views for managing events within the Event Booking System (EBS) application.

It includes viewsets and custom views to handle event-related operations, such as creation and update.
The views are designed to manage permissions based on user roles and perform specific actions on events.

Contents:
- EventViewSet: A viewset managing event-related operations.
  - Allows creation, updating, and deleting events with proper permissions.
  - Retrieves event data based on user roles.
  - Custom methods to create and update events while handling permissions and notifications.

Note: This module is part of the ebs_app package and should be imported accordingly.
"""


from copy import copy
from rest_framework import viewsets, permissions
from ebs_app.models.events import Event
from ebs_app.models.bookings import Booking
from users.permissions import IsEventOrganiser
from users.event_organiser.models import EventOrganiser
from ebs_app.serializers.event_serializers import EventSerializer
from ebs_app.tasks import send_event_update_email

from ebs_app.exceptions import NotAuthorisedAPIException


class EventViewSet(viewsets.ModelViewSet):
    """
    Event ViewSet:

    This viewset manages event-related operations.

    Attributes:
    - queryset: A queryset containing all Event objects.
    - serializer_class: The serializer class for Event objects.

    Permissions:
    - For actions "create", "update", "partial_update", and "delete",
      only authenticated Event Organizers are allowed.
    - For other actions, authentication is required for all users.

    Methods:
    - perform_create(serializer): Custom method to create an event.
      Requires the user to be an authenticated Event Organizer.

    - perform_update(serializer): Custom method to update an event.
      Sends email notifications to customers who have booked the event.
    """

    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_permissions(self):
        """
        Get the list of permission classes based on the action.

        Returns:
            list: A list of permission classes based on the action.
        """
        if self.action in ["create", "update", "partial_update", "delete"]:
            permission_classes = [permissions.IsAuthenticated, IsEventOrganiser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """
        Perform custom event creation.

        Payload Structure:
        {
            "event_name": "Friday Party",                       # Name of the event
            "event_description": "A casual event on Friday",    # Description of the event
            "event_date_time": "2023-08-25T20:00",              # Date and time of the event
            "venue": "CP"                                       # Venue of the event
        }

        Raises:
            NotAuthorisedAPIException: If the user is not an authenticated Event Organizer.
        """
        event_organiser = EventOrganiser.objects.get(user=self.request.user)

        if event_organiser is None:
            raise NotAuthorisedAPIException()

        if serializer.is_valid(raise_exception=True):
            serializer.save(
                event_organiser=event_organiser,
            )
        return super().perform_create(serializer)

    def perform_update(self, serializer):
        """
        Perform custom event update.

        Sends email notifications to customers who have booked the event.

        Args:
            serializer: The serializer instance for the event.
        """
        event = self.get_object()
        event_bookings = (
            Booking.objects.filter(ticket__event=event)
            .values_list("customer__user__email")
            .distinct()
        )
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
