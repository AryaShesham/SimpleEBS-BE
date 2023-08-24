"""
Collection of all the choices used under ebs_app
"""
from django.db import models


class TicketChoices(models.TextChoices):
    GENERAL_ADMISSION = "GENERAL_ADMISSION", "General Admission"
    VIP = "VIP", "VIP"
    PREMIUM = "PREMIUM", "Premium"
    SUPER_DELUX = "SUPER_DELUX", "Super Delux"
    ROYAL = "ROYAL", "Royal"


class BookingStatus(models.TextChoices):
    BOOKED = "BOOKED", "Booked"
    CANCELLED = "CANCELLED", "Cancelled"
    PENDING = "PENDING", "Pending"