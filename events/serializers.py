from rest_framework.serializers import ModelSerializer
from .models import Event, EventRegistration

class EventSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date', 'time', 'location', 'price', 'capacity', 'organizer']

class AdminEventRegistrationSerializer(ModelSerializer):
    class Meta:
        model = EventRegistration
        fields = ['id', 'event', 'user', 'registration_date', 'is_full', 'is_registered', 'get_total_revenue', 'get_total_attendees']

class EventRegistrationSerializer(ModelSerializer):
    class Meta:
        model = EventRegistration
        fields = ['id', 'event', 'user', 'registration_date', 'is_registered']

        