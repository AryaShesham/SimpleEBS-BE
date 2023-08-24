from rest_framework import viewsets, permissions
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from ebs_app.models.bookings import Booking
from ebs_app.models.tickets import Ticket
from users.customer.models import Customer
from users.event_organiser.models import EventOrganiser
from users.permissions import IsCustomer
from ebs_app.serializers.booking_serializers import BookingSerializer
from ebs_app.tasks import send_booking_confirmation_email
from ebs_app.exceptions import (NoCustomerAPIException,
                                NoTicketAPIException,
                                TicketNotAvailableAPIException,
                                BookedMoreSeatAPIException,
                                NotAValidUserAPIException,
                                CancellationNotAllowedAPIException)

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    http_method_names = ["get", "post"]

    def get_permissions(self):
        if self.action in ["create"]:
            permission_classes = [permissions.IsAuthenticated, IsCustomer]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        customer = Customer.objects.get(user=self.request.user)
        if customer is None:
            raise NoCustomerAPIException()

        ticket_id = self.request.data.get("ticket")
        ticket = Ticket.objects.get(
            id=ticket_id
            ) if "ticket" in self.request.data else None

        count = self.request.data.get("count")

        if ticket is None:
            raise NoTicketAPIException()

        ticket_current_count = ticket.availability
        if ticket_current_count == 0:
            raise TicketNotAvailableAPIException()

        if count > ticket_current_count:
            raise BookedMoreSeatAPIException()

        available_tickets = ticket_current_count - count
        ticket.availability = available_tickets
        user_email = "test@email.com"
        breakpoint()
        send_booking_confirmation_email.delay(ticket_id, user_email)

        if serializer.is_valid(raise_exception=True):
            ticket.save()
            serializer.save(
                customer=customer,
                ticket=ticket
            )
        return super().perform_create(serializer)

    def get_queryset(self):
        event_organiser = hasattr(self.request.user, 'eventorganiser')
        customer = hasattr(self.request.user, 'customer')
        if customer:
            customer = Customer.objects.get(user=self.request.user)
            return Booking.objects.filter(customer=customer)
        elif event_organiser:
            event_organiser = EventOrganiser.objects.get(user=self.request.user)
            return Booking.objects.filter(ticket__event__event_organiser=event_organiser)
        else:
            raise NotAValidUserAPIException()


class CancelBooking(GenericAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated, IsCustomer]

    def patch(self, request, pk):
        user_is_customer = hasattr(self.request.user, 'customer')
        if user_is_customer:
            customer = Customer.objects.get(user=self.request.user)
            booking = Booking.objects.get(id=pk)
            if booking.customer == customer:
                count = booking.count
                ticket = booking.ticket
                new_availability = ticket.availability+count
                booking.status = "CANCELLED"
                booking.is_cancelled = True
                booking.save()
                ticket.availability = new_availability
                ticket.save()
            else:
                raise CancellationNotAllowedAPIException()
        else:
            raise NoCustomerAPIException()
        return Response({"status": "Cancelled Successfully"})