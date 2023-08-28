"""
Ticket Booking Model
"""
from django.db import models
from users.customer.models import Customer
from ebs_app.models.tickets import Ticket
from ebs_app.models.choices import BookingStatus



class SubBooking(models.Model):
    ticket = models.ForeignKey(
        Ticket, null=False, blank=False, on_delete=models.CASCADE
    )
    count = models.IntegerField(default=0, null=False, blank=False)

    def __str__(self):
        return f"{self.ticket.id} - {self.count}"



class Booking(models.Model):
    """
    Booking Model:

    Represents a booking made by a customer for a specific ticket and event.

    Fields:
    - customer (ForeignKey):
        The associated customer who made the booking.
    - ticket (ForeignKey):
        The associated ticket for which the booking is made.
    - count (IntegerField):
        The number of tickets purchased in the booking.
    - status (CharField):
        The current status of the booking (e.g., PENDING, CONFIRMED).
    - is_cancelled (BooleanField):
        Indicates whether the booking has been cancelled.

    Properties:
    - total_price (property):
        Calculates and returns the total price of the booking.

    Methods:
    - __str__():
        Returns a formatted string representation of the booking.

    Example Usage:
    booking = Booking.objects.get(pk=1)
    print(booking)  # Output: "1 - John"
    """

    customer = models.ForeignKey(
        Customer, null=False, blank=False, on_delete=models.CASCADE
    )
    sub_bookings = models.ManyToManyField(SubBooking, related_name="bookings")
    status = models.CharField(
        max_length=20,
        choices=BookingStatus.choices,
        default=BookingStatus.PENDING,
        blank=False,
    )
    total_price = models.IntegerField(default=0)
    is_cancelled = models.BooleanField(default=False)

    # @property
    # def total_price(self):
    #     """
    #     Calculate the total price of the booking.

    #     Returns:
    #         int: The calculated total price of the booking.
    #     """
    #     ticket_price = self.ticket.price
    #     count = self.count
    #     total_price = ticket_price * count
    #     return total_price

    def __str__(self):
        return f"{self.id} - {self.customer.user.first_name}"
