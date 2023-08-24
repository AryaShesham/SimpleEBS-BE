"""
Booking Serializer
"""

from rest_framework.serializers import ModelSerializer
from ebs_app.models.bookings import Booking
from users.customer.serializers import CustomerSerializers
from ebs_app.serializers.ticket_serializers import TicketSerializer


class BookingSerializer(ModelSerializer):
    customer = CustomerSerializers(read_only=True)
    ticket = TicketSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = ["id", "customer",
                  "ticket", "count",
                  "status", "total_price"]
