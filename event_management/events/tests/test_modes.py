from django.test import TestCase
from django.utils import timezone

from events.models import Event


class EventModelTestCase(TestCase):
    def setUp(self):
        self.event = Event.objects.create(
            title='Test Event',
            description='This is a test description for the event.',
            date=timezone.now(),
            location='Test Location',
            organizer='Test Organizer'
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
            organizer='Another Organizer'
        )
        events = Event.objects.filter(organizer='Test Organizer')
        self.assertEqual(events.count(), 1)
