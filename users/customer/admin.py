from django.contrib import admin
from users.customer.models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["id", "user"]
