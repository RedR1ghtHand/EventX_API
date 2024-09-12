from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User

from events.models import Event, EventRegistration


class EventModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.event = Event.objects.create(
            title='Test Event',
            description='This is a test description for the event.',
            date=timezone.now(),
            location='Test Location',
            organizer=self.user
        )

    def test_event_creation(self):
        self.assertEqual(self.event.title, 'Test Event')
        self.assertEqual(self.event.description, 'This is a test description for the event.')
        self.assertEqual(Event.objects.count(), 1)

    def test_event_str_method(self):
        self.assertEqual(str(self.event), 'Test Event')

    def test_event_update(self):
        self.event.title = 'Updated Event Title'
        self.event.save()
        updated_event = Event.objects.get(id=self.event.id)
        self.assertEqual(updated_event.title, 'Updated Event Title')

    def test_event_deletion(self):
        event_id = self.event.id
        self.event.delete()
        with self.assertRaises(Event.DoesNotExist):
            Event.objects.get(id=event_id)

    def test_event_filter(self):
        Event.objects.create(
            title='Another Event',
            description='Another test event',
            date=timezone.now(),
            location='Another Location',
            organizer=self.user
        )
        events = Event.objects.filter(organizer=self.user)
        self.assertEqual(events.count(), 2)


class EventRegistrationModelTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password')
        self.user2 = User.objects.create_user(username='user2', password='password')

        self.event = Event.objects.create(
            title="Test Event",
            description="Test Event Description",
            date=timezone.now(),
            location="Test Location",
            organizer=self.user1
        )

    def test_create_registration(self):
        registration = EventRegistration.objects.create(user=self.user1, event=self.event)
        self.assertEqual(EventRegistration.objects.count(), 1)
        self.assertEqual(registration.user, self.user1)
        self.assertEqual(registration.event, self.event)

    def test_unique_registration(self):
        EventRegistration.objects.create(user=self.user1, event=self.event)
        with self.assertRaises(Exception):
            EventRegistration.objects.create(user=self.user1, event=self.event)

    def test_delete_registration(self):
        registration = EventRegistration.objects.create(user=self.user1, event=self.event)
        registration_id = registration.id
        registration.delete()
        with self.assertRaises(EventRegistration.DoesNotExist):
            EventRegistration.objects.get(id=registration_id)

    def test_filter_registration_by_user(self):
        EventRegistration.objects.create(user=self.user1, event=self.event)
        EventRegistration.objects.create(user=self.user2, event=self.event)
        registrations = EventRegistration.objects.filter(user=self.user1)
        self.assertEqual(registrations.count(), 1)

    def test_filter_registration_by_event(self):
        EventRegistration.objects.create(user=self.user1, event=self.event)
        registrations = EventRegistration.objects.filter(event=self.event)
        self.assertEqual(registrations.count(), 1)

