from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from unittest.mock import patch
from unittest import mock
from django.contrib.auth.models import User
from ebs_app.models.bookings import Booking
from ebs_app.models.tickets import Ticket
from ebs_app.models.events import Event
from ebs_app.tests.factories import CustomerFactory, UserFactory, EventOrganiserFactory
from ebs_app.exceptions import (
    NoTicketAPIException,
    TicketNotAvailableAPIException,
    BookedMoreSeatAPIException,
    NotAValidUserAPIException,
)


class BookingViewSetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer_user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            email="test@email.com",
        )

        self.customer = CustomerFactory(user=self.customer_user)

        self.event_organiser_user = User.objects.create_user(
            username="testuser_event",
            password="testpassword",
            email="event_org_test@email.com",
        )

        self.event_organiser = EventOrganiserFactory(user=self.event_organiser_user)

        self.event = Event.objects.create(
            event_name="Test Event",
            event_description="Test Event Description",
            event_date_time="2023-08-25T20:00Z",
            venue="CP",
            event_organiser=self.event_organiser,
        )

        self.ticket = Ticket.objects.create(
            event=self.event,
            ticket_type="PREMIUM",
            total_allotment=150,
            availability=125,
            price=149,
        )

        self.ticket_not_available = Ticket.objects.create(
            event=self.event,
            ticket_type="PREMIUM",
            total_allotment=150,
            availability=0,
            price=149,
        )

        self.valid_payload = {
            "ticket": self.ticket.id,
            "count": 2,
        }
        self.client.force_authenticate(user=self.customer_user)

    def mock_send_booking_confirmation_email(self, ticket_id, user_email):
        data = {"email": f"Booking Successful for {ticket_id}, {user_email}."}
        return data

    def test_create_booking(self):
        with mock.patch(
            "ebs_app.views.bookings_views.send_booking_confirmation_email.delay",
            new=self.mock_send_booking_confirmation_email,
        ):
            url = reverse("bookings-list")
            response = self.client.post(url, self.valid_payload, format="json")
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Booking.objects.count(), 1)
            self.assertEqual(
                Booking.objects.first().customer, self.customer_user.customer
            )

    @patch("ebs_app.tasks.send_booking_confirmation_email.delay")
    def test_create_booking_confirmation_email(self, mock_send_email):
        url = reverse("bookings-list")

        response = self.client.post(url, self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        mock_send_email.assert_called_once_with(
            self.ticket.id, self.customer_user.email
        )

    def test_create_booking_no_customer(self):
        # No customer is associated with the user for this test
        client = APIClient()
        self.user = UserFactory()
        client.force_authenticate(user=self.user)
        with mock.patch(
            "ebs_app.views.bookings_views.send_booking_confirmation_email.delay",
            new=self.mock_send_booking_confirmation_email,
        ):
            url = reverse("bookings-list")
            response = client.post(url, self.valid_payload, format="json")
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            self.assertEqual(Booking.objects.count(), 0)

    def test_create_no_ticket(self):
        """
        Test raising NoTicketAPIException when ticket is not provided.
        """
        url = reverse("bookings-list")
        payload = {
            "count": 2,
        }

        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["detail"], NoTicketAPIException.default_detail)
        self.assertEqual(Booking.objects.count(), 0)

    def test_create_ticket_not_available(self):
        """
        Test raising TicketNotAvailableAPIException when ticket availability is 0.
        """
        self.client.force_authenticate(user=self.customer_user)
        url = reverse("bookings-list")
        payload = {
            "ticket": self.ticket_not_available.id,
            "count": 2,
        }

        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()["detail"], TicketNotAvailableAPIException.default_detail
        )
        self.assertEqual(Booking.objects.count(), 0)

    def test_perform_create_booked_more_seats(self):
        """
        Test raising BookedMoreSeatAPIException when booking count exceeds ticket availability.
        """
        self.client.force_authenticate(user=self.customer_user)
        url = reverse("bookings-list")
        payload = {
            "ticket": self.ticket.id,
            "count": 200,
        }

        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()["detail"], BookedMoreSeatAPIException.default_detail
        )
        self.assertEqual(Booking.objects.count(), 0)

    def test_get_queryset_as_customer(self):
        """
        Test retrieving bookings as a customer.
        """
        url = reverse("bookings-list")
        Booking.objects.create(
            customer=self.customer, count=2, ticket=self.ticket, status="BOOKED"
        )

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Booking.objects.count(), 1)

    def test_get_queryset_as_event_organiser(self):
        """
        Test retrieving bookings as an event organiser.
        """
        self.client.force_authenticate(user=self.event_organiser.user)
        url = reverse("bookings-list")
        Booking.objects.create(
            customer=self.customer, count=2, ticket=self.ticket, status="BOOKED"
        )

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Booking.objects.count(), 1)

    def test_get_queryset_invalid_user(self):
        """
        Test raising NotAValidUserAPIException for an invalid user role.
        """
        client = APIClient()
        self.user = UserFactory()
        client.force_authenticate(user=self.user)  # A user without any valid role
        url = reverse("bookings-list")

        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()["detail"], NotAValidUserAPIException.default_detail
        )
        self.assertEqual(Booking.objects.count(), 0)


class CancelBookingTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer_user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            email="test@email.com",
        )

        self.customer = CustomerFactory(user=self.customer_user)

        self.event = Event.objects.create(
            event_name="Test Event",
            event_description="Test Event Description",
            event_date_time="2023-08-25T20:00Z",
            venue="CP",
        )

        self.ticket = Ticket.objects.create(
            event=self.event,
            ticket_type="PREMIUM",
            total_allotment=150,
            availability=125,
            price=149,
        )

        self.booking = Booking.objects.create(
            customer=self.customer, ticket=self.ticket, count=2, status="BOOKED"
        )

        self.client.force_authenticate(user=self.customer_user)

    def test_cancel_booking(self):
        url = reverse("cancel_booking", kwargs={"pk": self.booking.id})

        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the booking status and ticket availability are updated
        self.booking.refresh_from_db()
        self.ticket.refresh_from_db()
        self.assertEqual(self.booking.status, "CANCELLED")
        self.assertTrue(self.booking.is_cancelled)
        self.assertEqual(self.ticket.availability, 127)

    def test_cancel_booking_not_owner(self):
        # Create another customer user
        another_customer_user = User.objects.create_user(
            username="anotheruser",
            password="testpassword",
            email="another@email.com",
        )

        self.client.force_authenticate(user=another_customer_user)
        url = reverse("cancel_booking", kwargs={"pk": self.booking.id})

        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cancel_booking_no_customer(self):
        # Create a non-customer user
        non_customer_user = UserFactory()
        self.client.force_authenticate(user=non_customer_user)
        url = reverse("cancel_booking", kwargs={"pk": self.booking.id})

        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cancel_nonexistent_booking(self):
        url = reverse("cancel_booking", kwargs={"pk": 999})

        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
