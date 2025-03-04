from rest_framework.serializers import ModelSerializer, ValidationError
from .models import Event, EventRegistration

class EventSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 
                  'date', 'time', 'location', 
                  'price', 'capacity', 'organizer', 'is_full']

class AdminEventRegistrationSerializer(ModelSerializer):
    class Meta:
        model = EventRegistration
        fields = ['id', 'event', 'user', 'registration_date', 
                  'is_full', 'is_registered', 'get_total_revenue', 
                  'get_total_attendees']

class EventRegistrationSerializer(ModelSerializer):
 
    class Meta:
        model = EventRegistration
        fields = ['id', 'event', 'user', 'registration_date', 
                  'is_registered']
        read_only_fields = ['user', 'is_registered']

    def create(self, validated_data):
        event = validated_data.get('event')
        if event.is_full():
            raise ValidationError("Cannot register for this event. Event is full.")
        return super().create(validated_data)

        