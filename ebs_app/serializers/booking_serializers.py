"""
Booking Serializer
"""

from rest_framework.serializers import ModelSerializer
from ebs_app.models.bookings import Booking, SubBooking
from users.customer.serializers import CustomerSerializers
from ebs_app.serializers.ticket_serializers import TicketSerializer


class SubBookingSerializer(ModelSerializer):
    class Meta:
        model = SubBooking
        fields = "__all__"


class BookingSerializer(ModelSerializer):
    customer = CustomerSerializers(read_only=True)
    sub_bookings = SubBookingSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Booking
        fields = ["id", "customer", "sub_bookings", "status", "total_price"]
