from django.core import mail
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from django.db import OperationalError

from unittest.mock import patch

from events.models import Event, EventRegistration
from events.utils import send_registration_email


class PositiveEmailNotificationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password', email='testuser@example.com')

        self.event = Event.objects.create(
            title='Test Event',
            description='This is a test event',
            date=timezone.now(),
            location='Test Location',
            organizer=self.user
        )

    def test_send_single_email(self):
        send_registration_email(self.user, self.event)

        self.assertEqual(len(mail.outbox), 1)

        email = mail.outbox[0]
        self.assertEqual(email.subject, f'Registration for {self.event.title}')
        self.assertIn(self.event.title, email.body)
        self.assertIn(self.user.username, email.body)
        self.assertEqual(email.to, [self.user.email])

    def test_send_multiple_emails(self):
        for i in range(5):
            send_registration_email(self.user, self.event)

        self.assertEqual(len(mail.outbox), 5)

    def test_email_backend_usage(self):
        send_registration_email(self.user, self.event)
        self.assertEqual(len(mail.outbox), 1)

        email = mail.outbox[0]
        self.assertEqual(email.to, [self.user.email])

    def test_email_sender(self):
        send_registration_email(self.user, self.event)

        email = mail.outbox[0]
        self.assertEqual(email.from_email, settings.DEFAULT_FROM_EMAIL)


class NegativeEmailNotificationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password', email='validuser@example.com')
        self.event = Event.objects.create(
            title="Test Event",
            description="Test Description",
            date="2024-10-10T10:00:00Z",
            location="Test Location",
            organizer=self.user
        )

    @patch('events.utils.send_mail')
    def test_email_not_sent_due_to_invalid_user_email(self, mock_send_mail):
        user_no_email = User.objects.create_user(username='noemailuser', password='password', email='')

        registration = EventRegistration.objects.create(user=user_no_email, event=self.event)
        send_registration_email(user_no_email, self.event)

        self.assertEqual(len(mail.outbox), 0)
        mock_send_mail.assert_not_called()

    @patch('events.utils.send_mail')
    def test_email_not_sent_due_to_invalid_email_format(self, mock_send_mail):
        user_invalid_email = User.objects.create_user(username='invalidemailuser', password='password', email='invalidemail')

        registration = EventRegistration.objects.create(user=user_invalid_email, event=self.event)
        send_registration_email(user_invalid_email, self.event)

        self.assertEqual(len(mail.outbox), 0)
        mock_send_mail.assert_not_called()

    @patch('events.utils.send_mail')
    @patch('events.models.EventRegistration.objects.create')
    def test_email_send_skipped_if_database_error(self, mock_create_registration, mock_send_mail):
        mock_create_registration.side_effect = OperationalError("Database is unavailable")

        with self.assertRaises(OperationalError):
            EventRegistration.objects.create(user=self.user, event=self.event)

        mock_send_mail.assert_not_called()

