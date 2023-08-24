"""
Module: ebs_app.views.tickets_views

This module contains views for managing tickets within the Event Booking System (EBS) application.

It includes viewsets to handle ticket-related operations such as creation and updating.
Permissions are managed based on user roles, ensuring authorized access to specific actions.

Contents:
- TicketViewSet: A viewset managing ticket-related operations.
  - Allows creation and retrieval of tickets with proper permissions.
  - Custom methods to perform ticket creation and updating.
  
Note: This module is part of the ebs_app package and should be imported accordingly.
"""

from rest_framework import viewsets, permissions
from ebs_app.models.tickets import Ticket
from ebs_app.models.events import Event
from users.event_organiser.models import EventOrganiser
from users.permissions import IsEventOrganiser
from ebs_app.exceptions import NoEventAPIException

from ebs_app.serializers.ticket_serializers import TicketSerializer
from ebs_app.exceptions import NoEventOrganiserAPIException

class TicketViewSet(viewsets.ModelViewSet):
    """
    Ticket ViewSet:

    This viewset manages ticket-related operations.

    Attributes:
    - queryset: A queryset containing all Ticket objects.
    - serializer_class: The serializer class for Ticket objects.

    Permissions:
    - For actions "create" and "delete", only authenticated Event Organizers are allowed.
    - For other actions, authentication is required for all users.

    Methods:
    - perform_create(serializer): Custom method to create a ticket through the API.
    - perform_update(serializer): Custom method to update a ticket through the API.
    """

    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    
    
    def get_permissions(self):
        """
        Get the list of permission classes based on the action.

        This method dynamically assigns permission classes based on the action being performed.
        - For the "create" and "delete" actions, only authenticated event organizers are allowed.
        - For other actions, authentication is required for all users.

        Returns:
            list: A list of permission classes based on the action.
        """

        if self.action in ['create', 'update', 'partial_update', 'delete']:
            permission_classes = [permissions.IsAuthenticated, IsEventOrganiser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """
        Custom method for creating an object using a serializer.

        This method handles the creation of a new object using the provided serializer.
        It retrieves the associated event, if provided, and raises a NoEventAPIException
        if the event is missing. The method then saves the object using the serializer.

        Args:
            serializer: The serializer instance used to validate and create the object.
            
        Payload Structure:
            {
                "event": 1,                   # ID of the associated event
                "ticket_type": "PREMIUM",     # Type of the ticket (e.g., PREMIUM, STANDARD)
                "availability": 125,          # Number of available tickets
                "total_allotment": 150,       # Total number of tickets allotted
                "price": 149                  # Price of the ticket
            }

        Raises:
            NoEventAPIException: If the associated event is not provided.

        Returns:
            The result of the superclass's perform_create method.
        """

        event = Event.objects.get(
            id=self.request.data.get("event")
            ) if "event" in self.request.data else None

        if event is None:
            raise NoEventAPIException()
        
        if serializer.is_valid(raise_exception=True):
            serializer.save(
                event=event,
            )
        return super().perform_create(serializer)

    def perform_update(self, serializer):
        """
        Custom method for updating a ticket through the API.

        Args:
            serializer: The serializer instance used to validate and update the ticket.
        """

        serializer.save()
        return super().perform_update(serializer)
