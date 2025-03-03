import django_filters

from .models import Event, EventRegistration

class EventFilter(django_filters.FilterSet):
    class Meta:
        model = Event
        fields = {
            'title': ['icontains'],
            'date': ['exact', 'gt', 'lt'],
            'location': ['icontains'],
            'price': ['exact', 'gt', 'lt'],
            'capacity': ['exact', 'gt', 'lt'],
        }

class EventRegistrationFilter(django_filters.FilterSet):
    class Meta:
        model = EventRegistration
        fields = {
            'event': ['exact'],
            'user': ['exact'],
            'status': ['exact'],
            'registration_date': ['exact', 'gt', 'lt'],
        }