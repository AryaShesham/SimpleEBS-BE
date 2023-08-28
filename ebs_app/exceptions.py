from rest_framework.exceptions import APIException
from rest_framework import status


class NotAuthorisedAPIException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "You're not authorised to perform this."


class NoEventAPIException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "You have not provided the event."


class NoCustomerAPIException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "You are not a customer."


class NoEventOrganiserAPIException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "You are not an event organiser."


class NoTicketAPIException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "You have not provided a valid ticket."


class SimultaneousUpdateError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Simultaneous Update is happening."


class TicketNotAvailableAPIException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Ticket not available."


class BookedMoreSeatAPIException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "You're booking more than available seats."


class NotAValidUserAPIException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Not a valid user."


class CancellationNotAllowedAPIException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "You are not authorised to cancel this booking."


class ContentNotFoundAPIException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Content not found."


class TicketNotFoundAPIException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Ticket not found."


class InvalidSubBookingDataAPIException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Please provide valid bookings."


class AlreadyCancelledAPIException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Ticket is already cancelled."
