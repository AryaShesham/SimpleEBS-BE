from rest_framework import viewsets, permissions
from ebs_app.models.tickets import Ticket
from ebs_app.models.events import Event
from users.customer.models import Customer
from users.permissions import IsEventOrganiser
from ebs_app.exceptions import NoEventAPIException

from ebs_app.serializers.ticket_serializers import TicketSerializer
from ebs_app.exceptions import NoCustomerAPIException

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    
    
    def get_permissions(self):
        if self.action in ['create', 'delete']:
            permission_classes = [permissions.IsAuthenticated, IsEventOrganiser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        customer = Customer.objects.get(user=self.request.user)

        if customer is None:
            raise NoCustomerAPIException()

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
        serializer.save()
        return super().perform_update(serializer)
