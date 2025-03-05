from rest_framework.serializers import ModelSerializer, ValidationError, SerializerMethodField
from .models import Event, EventRegistration, EventCategory
from django.utils import timezone

class EventCategorySerializer(ModelSerializer):
    class Meta:
        model = EventCategory
        fields = ['id', 'name', 'description', 'slug', 'created_at', 'updated_at', 'active']

class EventSerializer(ModelSerializer):
    is_full = SerializerMethodField()

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date', 'time', 'location', 'price', 'capacity', 'organizer', 'is_full']

    def get_is_full(self, obj):
        return obj.is_full()

    def validate_date(self, value):
        if value < timezone.now():
            raise ValidationError("The event date must be in the future.")
        return value

class AdminEventRegistrationSerializer(ModelSerializer):
    get_total_revenue = SerializerMethodField()
    get_total_attendees = SerializerMethodField()

    class Meta:
        model = EventRegistration
        fields = ['id', 'event', 'user', 'registration_date', 'is_full', 'is_registered', 'get_total_revenue', 'get_total_attendees']

    def get_total_revenue(self, obj):
        return obj.get_total_revenue()

    def get_total_attendees(self, obj):
        return obj.get_total_attendees()

class EventRegistrationSerializer(ModelSerializer):
    class Meta:
        model = EventRegistration
        fields = ['id', 'event', 'user', 'registration_date', 'is_registered']
        read_only_fields = ['user', 'is_registered']

    def create(self, validated_data):
        event = validated_data.get('event')
        if event.is_full():
            raise ValidationError("Cannot register for this event. Event is full.")
        return super().create(validated_data)

