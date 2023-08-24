from celery import shared_task

@shared_task
def send_booking_confirmation_email(ticket_id, user_email):
    # Simulate sending email confirmation
    print(f"Sending email confirmation for ticket {ticket_id} to {user_email}")

@shared_task
def send_event_update_email(event, customer_email_list):
    for email in customer_email_list:
        print(f"The Event change has been informed to {email} as: {event['event_name'], event['event_venue'], event['event_time']}")