from celery import shared_task


@shared_task
def send_booking_confirmation_email(ticket_id, user_email):
    """
    Celery task for sending booking confirmation emails.

    This task simulates sending a booking confirmation email to a user.
    It takes the ticket ID and user's email as parameters.

    Args:
        ticket_id (int): The ID of the booked ticket.
        user_email (str): The email address of the user.

    Note: This task is asynchronous and executed by a Celery worker.

    Example:
    send_booking_confirmation_email.delay(123, "user@example.com")
    """

    # Simulate sending email confirmation
    print(f"Sending email confirmation for ticket {ticket_id} to {user_email}")


@shared_task
def send_event_update_email(event, customer_email_list):
    """
    Celery task for sending event update notifications.

    This task sends event update notifications to a list of customer emails.
    It takes an event dictionary and a list of customer email addresses as parameters.

    Args:
        event (dict): The updated event details.
        customer_email_list (list): List of customer email addresses.

    Note: This task is asynchronous and executed by a Celery worker.

    Example:
    event_details = {
        "event_name": "Updated Event",
        "event_venue": "New Venue",
        "event_time": "2023-08-28T14:00:00Z"
    }
    customer_emails = ["user1@example.com", "user2@example.com"]
    send_event_update_email.delay(event_details, customer_emails)
    """
    for email in customer_email_list:
        print(
            f"The Event change has been informed to {email} as: {event['event_name'], event['event_venue'], event['event_time']}"
        )
