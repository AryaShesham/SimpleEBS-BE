from django.urls import include, path
from rest_framework.routers import DefaultRouter
from ebs_app.views.events_views import EventViewSet
from ebs_app.views.bookings_views import BookingViewSet, CancelBooking
from ebs_app.views.tickets_views import TicketViewSet

router = DefaultRouter()

router.register("events", EventViewSet, basename="events")
router.register("bookings", BookingViewSet, basename="bookings")
router.register("tickets", TicketViewSet, basename="tickets")

urlpatterns = [
    path("", include(router.urls)),
    path("cancel_booking/<str:pk>", CancelBooking.as_view(), name="cancel_booking")
    ]