from django.db import models
from users.customer.models import Customer
from ebs_app.models.tickets import Ticket
from ebs_app.models.choices import BookingStatus

class Booking(models.Model):
    customer = models.ForeignKey(Customer,
                                 null=False,
                                 blank=False,
                                 on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket,
                               null=False,
                               blank=False,
                               on_delete=models.CASCADE)
    count = models.IntegerField(default=0, null=False, blank=False)
    status = models.CharField(max_length=20,
                              choices=BookingStatus.choices,
                              default=BookingStatus.PENDING,
                              blank=False)
    is_cancelled = models.BooleanField(default=False)

    @property
    def total_price(self):
        ticket_price = self.ticket.price
        count = self.count
        total_price = ticket_price*count
        return total_price

    def __str__(self):
        return f"{self.id} - {self.customer.user.first_name}"
