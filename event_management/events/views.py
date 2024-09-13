from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import generics, filters

from django_filters.rest_framework import DjangoFilterBackend

from .serializers import UserSerializer, EventSerializer, EventRegistrationSerializer
from .models import Event, EventRegistration
from .utils import send_registration_email


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]

    filterset_fields = ['date', 'location', 'organizer']

    search_fields = ['title', 'description']

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)


class EventRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(organizer=self.get_object().organizer)


class EventRegistrationView(generics.CreateAPIView):
    queryset = EventRegistration.objects.all()
    serializer_class = EventRegistrationSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        event_id = request.data.get('event_id')
        event = Event.objects.get(id=event_id)

        if EventRegistration.objects.filter(user=request.user, event=event).exists():
            return Response({"detail": "Ви вже зареєстровані на цю подію."}, status=status.HTTP_400_BAD_REQUEST)

        registration = EventRegistration.objects.create(user=request.user, event=event)
        send_registration_email(request.user, event)

        serializer = self.get_serializer(registration)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class EventRegistrationsListView(generics.ListAPIView):
    serializer_class = EventRegistrationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        event_id = self.kwargs['event_id']
        return EventRegistration.objects.filter(event_id=event_id)

