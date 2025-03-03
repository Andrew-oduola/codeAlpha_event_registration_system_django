from django.shortcuts import render

from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from .models import Event, EventRegistration
from .serializers import EventSerializer, EventRegistrationSerializer, AdminEventRegistrationSerializer
from .filters import EventFilter, EventRegistrationFilter

# Create your views here.
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EventFilter


class EventRegistrationViewSet(viewsets.ModelViewSet):
    queryset = EventRegistration.objects.all()
    serializer_class = EventRegistrationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EventRegistrationFilter   

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return AdminEventRegistrationSerializer
        return EventRegistrationSerializer


