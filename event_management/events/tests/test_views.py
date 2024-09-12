from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework import status

from django.contrib.auth.models import User
from django.test import TestCase

from events.views import EventListCreateView


class EventViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.token = Token.objects.create(user=self.user)
        self.factory = APIRequestFactory()

    def test_create_event(self):
        request = self.factory.post('/events/', {
            "title": "Test Event",
            "description": "This is a test event",
            "date": "2024-10-10T10:00:00Z",
            "location": "Test Location",
        }, format='json')

        force_authenticate(request, user=self.user, token=self.token)
        view = EventListCreateView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['organizer'], self.user.id)

