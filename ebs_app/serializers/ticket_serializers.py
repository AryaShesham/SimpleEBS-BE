"""
Ticket Serializer
"""

from rest_framework.serializers import ModelSerializer
from ebs_app.models.tickets import Ticket


class TicketSerializer(ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"
