from rest_framework.exceptions import APIException
from rest_framework import status


class NotAuthorisedAPIException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "You're not authorised to perform this."


class NoEventAPIException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "You have not provided the event."


class NoCustomerAPIException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "You are not a customer."


class NoEventOrganiserAPIException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "You are not an event organiser."


class NoTicketAPIException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "You have not provided a valid ticket."


class TicketNotAvailableAPIException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Seat not available."


class BookedMoreSeatAPIException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "You're booking more than available seats."


class NotAValidUserAPIException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Not a valid user."


class CancellationNotAllowedAPIException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "You are not authorised to cancel this booking."
