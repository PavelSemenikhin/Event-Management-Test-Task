from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_event_registration_email(
    user_email,
    event_title,
    event_date,
    event_location,
    event_description,
):
    subject = "Your Event Register Confirmation"

    message = (
        f"Hello!\n\n"
        f"You have successfully registered for the event:\n\n"
        f"Title: {event_title}\n"
        f"Date: {event_date}\n"
        f"Location: {event_location}\n"
        f"Description: {event_description}\n\n"
        f"Thank you for your registration!"
    )
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list)
    print(f"Email sent to {user_email} for event {event_title}")
