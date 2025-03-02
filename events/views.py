from django.shortcuts import render

from rest_framework import viewsets
from .models import Event, EventRegistration
from .serializers import EventSerializer, EventRegistrationSerializer, AdminEventRegistrationSerializer


# Create your views here.
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventRegistrationViewSet(viewsets.ModelViewSet):
    queryset = EventRegistration.objects.all()
    serializer_class = EventRegistrationSerializer

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return AdminEventRegistrationSerializer
        return EventRegistrationSerializer


