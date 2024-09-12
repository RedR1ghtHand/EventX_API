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
    def event(self, user_and_token):
        user, _ = user_and_token
        return Event.objects.create(
            title="Test Event",
            description="Test description",
            date=timezone.now(),
            location="Test Location",
            organizer=user
        )

    def test_get_event_list(self, client, user_and_token, event):
        user, token = user_and_token
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        url = reverse('event-list-create')
        response = client.get(url)
        assert response.status_code == 200

    def test_event_detail(self, client, user_and_token, event):
        user, token = user_and_token
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        url = reverse('event-detail', kwargs={'pk': event.pk})
        response = client.get(url)
        assert response.status_code == 200
        assert response.data['title'] == event.title

    def test_event_update(self, client, user_and_token, event):
        user, token = user_and_token
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        url = reverse('event-detail', kwargs={'pk': event.pk})
        updated_data = {
            "title": "Updated Event",
            "description": "Updated description",
            "date": timezone.now(),
            "location": "New Location",
            "organizer": user.id
        }
        response = client.put(url, updated_data, format='json')
        assert response.status_code == 200
        event.refresh_from_db()
        assert event.title == "Updated Event"

    def test_event_delete(self, client, user_and_token, event):
        user, token = user_and_token
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        url = reverse('event-detail', kwargs={'pk': event.pk})
        response = client.delete(url)
        assert response.status_code == 204
        assert not Event.objects.filter(id=event.pk).exists()
