import django_filters
from django_filters import CharFilter, DateFilter, NumberFilter

from .models import Event, EventRegistration
from django.contrib.auth import get_user_model

User = get_user_model()


class EventFilter(django_filters.FilterSet):
    title = CharFilter(field_name='title', lookup_expr='icontains')
    date = DateFilter(field_name='date', lookup_expr='exact')
    date_gt = DateFilter(field_name='date', lookup_expr='gt')
    date_lt = DateFilter(field_name='date', lookup_expr='lt')
    location = CharFilter(field_name='location', lookup_expr='icontains')
    price = NumberFilter(field_name='price', lookup_expr='exact')
    price_gt = NumberFilter(field_name='price', lookup_expr='gt')
    price_lt = NumberFilter(field_name='price', lookup_expr='lt')
    capacity = NumberFilter(field_name='capacity', lookup_expr='exact')
    capacity_gt = NumberFilter(field_name='capacity', lookup_expr='gt')
    capacity_lt = NumberFilter(field_name='capacity', lookup_expr='lt')

    class Meta:
        model = Event
        fields = ['title', 'date', 'location', 'price', 'capacity']

class EventRegistrationFilter(django_filters.FilterSet):
    event = django_filters.ModelChoiceFilter(queryset=Event.objects.all())
    user = django_filters.ModelChoiceFilter(queryset=User.objects.all())
    status = CharFilter(field_name='status', lookup_expr='exact')
    registration_date = DateFilter(field_name='registration_date', lookup_expr='exact')
    registration_date_gt = DateFilter(field_name='registration_date', lookup_expr='gt')
    registration_date_lt = DateFilter(field_name='registration_date', lookup_expr='lt')

    class Meta:
        model = EventRegistration
        fields = ['event', 'user', 'status', 'registration_date']