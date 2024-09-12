import pytest
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

from events.models import Event


@pytest.mark.django_db
class TestEventAPI:

    @pytest.fixture
    def client(self):
        return APIClient()

    @pytest.fixture
    def user_and_token(self):
        user = User.objects.create_user(username='testuser', password='password')
        token = Token.objects.create(user=user)
        return user, token

    @pytest.fixture
    def event_data(self):
        return {
            "title": "Test Event",
            "description": "This is a test description.",
            "date": timezone.now(),
            "location": "Test Location",
            "organizer": "Test Organizer"
        }

    def test_create_event(self, client, user_and_token, event_data):
        user, token = user_and_token
        url = reverse('event-list-create')
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        response = client.post(url, event_data, format='json')
        assert response.status_code == 201
        assert Event.objects.count() == 1
        assert Event.objects.get().title == event_data['title']

    def test_get_event_list(self, client):
        Event.objects.create(
            title="Existing Event",
            description="Description for existing event",
            date=timezone.now(),
            location="Somewhere",
            organizer="Organizer"
        )
        url = reverse('event-list-create')
        response = client.get(url)
        assert response.status_code == 200
        assert len(response.data) == 1

    def test_event_detail(self, client):
        event = Event.objects.create(
            title="Event Detail",
            description="This is a test event detail",
            date=timezone.now(),
            location="Test Location",
            organizer="Test Organizer"
        )
        url = reverse('event-detail', kwargs={'pk': event.pk})
        response = client.get(url)
        assert response.status_code == 200
        assert response.data['title'] == event.title

    def test_event_update(self, client, event_data, user_and_token):
        user, token = user_and_token
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        event = Event.objects.create(
            title="Event to update",
            description="This is a test event for updating",
            date=timezone.now(),
            location="Test Location",
            organizer="Test Organizer"
        )
        url = reverse('event-detail', kwargs={'pk': event.pk})
        updated_data = event_data.copy()
        updated_data['title'] = 'Updated Event Title'
        response = client.put(url, updated_data, format='json')
        assert response.status_code == 200
        event.refresh_from_db()
        assert event.title == updated_data['title']

    def test_event_delete(self, client, user_and_token):
        user, token = user_and_token
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        event = Event.objects.create(
            title="Event to delete",
            description="This is a test event for deletion",
            date=timezone.now(),
            location="Test Location",
            organizer="Test Organizer"
        )
        url = reverse('event-detail', kwargs={'pk': event.pk})
        response = client.delete(url)
        assert response.status_code == 204
        assert Event.objects.count() == 0