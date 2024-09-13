from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.conf import settings

import logging

logger = logging.getLogger(__name__)


def send_registration_email(user, event):
    if not user.email:
        logger.warning(f"User {user.username} does not have an email. Skipping notification.")
        return

    try:
        validate_email(user.email)
    except ValidationError:
        logger.warning(f"Invalid email for user {user.username}: {user.email}. Skipping notification.")
        return

    subject = f"Registration for {event.title}"
    message = f"Dear {user.username},\n\nYou have successfully registered for the event '{event.title}' " \
              f"on {event.date} at {event.location}."

    recipient_list = [user.email]

    send_mail(
        subject,
        message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipient_list,
        fail_silently=False,
    )
