"""
Module: ebs_app.views.bookings_views

This module contains views for managing bookings within the Event Booking System (EBS) application.

It includes viewsets and custom views to handle booking-related operations such as creating, updating,
and cancelling bookings. Permissions are managed based on user roles, ensuring authorized access
to specific actions.

Contents:
- BookingViewSet: A viewset managing booking-related operations.
  - Allows creation and retrieval of bookings with proper permissions.
  - Retrieves booking data based on user roles.
  - Custom methods to perform booking creation and retrieve filtered queries.

- CancelBooking: A custom view for cancelling bookings.
  - Allows cancellation of bookings by customers.
  - Updates booking status and ticket availability accordingly.

Note: This module is part of the ebs_app package and should be imported accordingly.
"""
from django.db import transaction
from rest_framework import viewsets, permissions
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from ebs_app.models.bookings import Booking
from ebs_app.models.tickets import Ticket
from users.customer.models import Customer
from users.permissions import IsCustomer
from ebs_app.serializers.booking_serializers import BookingSerializer, SubBookingSerializer
from ebs_app.tasks import send_booking_confirmation_email
from ebs_app.exceptions import (
    NoCustomerAPIException,
    TicketNotAvailableAPIException,
    BookedMoreSeatAPIException,
    NotAValidUserAPIException,
    CancellationNotAllowedAPIException,
    ContentNotFoundAPIException,
    InvalidSubBookingDataAPIException,
    TicketNotFoundAPIException,
    AlreadyCancelledAPIException
)


class BookingViewSet(viewsets.ModelViewSet):
    """
    Booking View:

    This view handles booking-related operations.

    [Authentication Required]

    Allowed Methods:
    - POST: Exclusive to Customers.
      Creates a booking with the provided payload:
        payload: {
            "ticket": <ticket_id>,
            "count": <INT>
        }
      Returns Booking object.

    - GET: Accessible by both Event Organizers and Customers.
      Returns filtered booking data based on the user role:
        - If the user is a Customer, retrieves all bookings made by the requesting customer.
        - If the user is an Event Organizer,
          retrieves booking details for events organized by the requesting event organizer.
    """

    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    http_method_names = ["get", "post"]

    def get_permissions(self):
        """
        Get the list of permission classes based on the action.

        This method dynamically assigns permission classes based on the action being performed.
        - For the "create" action, only authenticated customers are allowed.
        - For other actions, authentication is required for all users.

        Returns:
            list: A list of permission classes based on the action.
        """
        if self.action in ["create"]:
            permission_classes = [permissions.IsAuthenticated, IsCustomer]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]


    @transaction.atomic
    def perform_create(self, serializer):
        """
        Custom method for creating a booking through the API.

        This method performs the booking creation process, including:
        - Retrieving the customer associated with the request user.
        - Fetching the selected ticket and its availability.
        - Checking and updating ticket availability based on booking count.
        - Sending a booking confirmation email asynchronously.
        - Saving the booking data and updating ticket availability.

        Args:
            serializer: The serializer instance used to validate and create the booking.

        Payload Structure:
        {
            "ticket": 123,   # ID of the ticket to be booked
            "count": 2       # Number of tickets to be booked
        }

        Raises:
            NoCustomerAPIException: When someone who is not a customer,
                tries to do the things authorised for customer only.
            NoTicketAPIException: When ticket is not provided and it is a required field.
            TicketNotAvailableAPIException: If the selected ticket is not available for booking.
            BookedMoreSeatAPIException: If the booking count exceeds the available ticket count.

        Returns:
            Response: The response after performing the booking creation process.
        """
        customer = Customer.objects.get(user=self.request.user)
        if customer is None:
            raise NoCustomerAPIException()

        sub_bookings = self.request.data.get("sub_bookings")

        if not isinstance(sub_bookings, list):
            raise InvalidSubBookingDataAPIException()

        validated_sub_bookings = []
        for sub_booking in sub_bookings:
            ticket_id = sub_booking.get("ticket")
            count = sub_booking.get("count")

            if not ticket_id or count is None or count <= 0:
                raise InvalidSubBookingDataAPIException()

            # select_for_update() should be used with the database which must support transactions and locks.
            ticket = Ticket.objects.select_for_update().filter(id=ticket_id).first()
            
            if not ticket:
                raise TicketNotFoundAPIException()

            validated_sub_bookings.append({'ticket': ticket, 'count': count})

        for sub_booking in validated_sub_bookings:
            ticket = sub_booking['ticket']
            count = sub_booking['count']

            ticket_current_count = ticket.availability

            if ticket_current_count == 0:
                raise TicketNotAvailableAPIException()

            if count > ticket_current_count:
                raise BookedMoreSeatAPIException()

            available_tickets = ticket_current_count - count
            ticket.availability = available_tickets
            ticket.save()

        sub_booking_serializer = SubBookingSerializer(data=sub_bookings, many=True)
        sub_booking_serializer.is_valid(raise_exception=True)
        saved_sub_bookings = sub_booking_serializer.save()
        sub_booking_id_list = [i.id for i in saved_sub_bookings]
        price_list = [i.ticket.price*i.count for i in saved_sub_bookings]

        if serializer.is_valid(raise_exception=True):
            booking = serializer.save(customer=customer, status="BOOKED", total_price=sum(price_list))
            booking.sub_bookings.set(sub_booking_id_list)

        user_email = "test@email.com"
        send_booking_confirmation_email.delay(ticket_id, user_email)
        return super().perform_create(serializer)


    def get_queryset(self):
        """
        Custom method to get the queryset for the Booking model based on the user's role.

        This method determines the user's role (either a customer or an event organizer),
        and returns a filtered queryset of bookings associated with that role.

        Returns:
            QuerySet: A filtered queryset of bookings based on the user's role.

        Raises:
            NotAValidUserAPIException: If the user's role cannot be determined or is invalid.
        """
        event_organiser = hasattr(self.request.user, "eventorganiser")
        customer = hasattr(self.request.user, "customer")
        if customer:
            customer = Customer.objects.get(user=self.request.user)
            return Booking.objects.filter(customer=customer)
        elif event_organiser:
            # event_organiser = EventOrganiser.objects.get(user=self.request.user)
            return Booking.objects.all()
        else:
            raise NotAValidUserAPIException()


class CancelBooking(GenericAPIView):
    """
    API endpoint to cancel a booking.

    This view allows a customer to cancel their booking. The booking status is changed to "CANCELLED",
    and the availability of the associated ticket is updated accordingly.

    Permissions:
    - Requires the user to be authenticated and identified as a customer.

    Args:
        pk: The primary key of the booking to be cancelled.

    Raises:
        CancellationNotAllowedAPIException: If the current user is not the owner of the booking.
        NoCustomerAPIException: If the current user is not identified as a customer.
        ContentNotFoundAPIException: If the specified booking does not exist.

    Returns:
        Response: A response indicating the success of the cancellation.
    """

    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated, IsCustomer]

    def patch(self, request, pk):
        user_is_customer = hasattr(self.request.user, "customer")
        if user_is_customer:
            customer = Customer.objects.get(user=self.request.user)
            try:
                booking = Booking.objects.get(id=pk)
                if booking.customer == customer:
                    if booking.status == "CANCELLED":
                        raise AlreadyCancelledAPIException()
                    sub_bookings = booking.sub_bookings.all()
                    for i in sub_bookings:
                        count = i.count
                        ticket = i.ticket
                        new_availability = ticket.availability + count
                        ticket.availability = new_availability
                        ticket.save()
                    booking.status = "CANCELLED"
                    booking.is_cancelled = True
                    booking.save()
                else:
                    raise CancellationNotAllowedAPIException()
            except Booking.DoesNotExist:
                raise ContentNotFoundAPIException()
        else:
            raise NoCustomerAPIException()
        return Response({"status": "Cancelled Successfully"})
