from django.urls import path
from rest_framework.authtoken import views as auth_views
from .views import (
    UserRegistrationView,
    UserProfileView,
    EventListCreateView,
    EventRetrieveUpdateDestroyView,
    EventRegistrationView,
    EventRegistrationsListView,
)

urlpatterns = [
    path('auth/register/', UserRegistrationView.as_view(), name='user-register'),
    path('auth/login/', auth_views.obtain_auth_token, name='user-login'),
    path('auth/profile/', UserProfileView.as_view(), name='user-profile'),
    path('events/', EventListCreateView.as_view(), name='event-list-create'),
    path('events/<int:pk>/', EventRetrieveUpdateDestroyView.as_view(), name='event-detail'),
    path('events/register/', EventRegistrationView.as_view(), name='event-register'),
    path('events/<int:event_id>/registrations/', EventRegistrationsListView.as_view(), name='event-registrations'),
]
