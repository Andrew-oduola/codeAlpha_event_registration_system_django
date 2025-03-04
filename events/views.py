
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend

import pandas as pd
import csv

from .models import Event, EventRegistration
from .serializers import EventSerializer, EventRegistrationSerializer, \
    AdminEventRegistrationSerializer
from .filters import EventFilter, EventRegistrationFilter

# Create your views here.
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EventFilter
    permission_classes = [IsAuthenticated]

class EventRegistrationViewSet(viewsets.ModelViewSet):
    queryset = EventRegistration.objects.all()
    serializer_class = EventRegistrationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EventRegistrationFilter   

    def get_queryset(self):
        if self.request.user.is_staff:
            return EventRegistration.objects.all()
        return EventRegistration.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return AdminEventRegistrationSerializer
        return EventRegistrationSerializer
    
    # Custom action to export event registrations to CSV (admin only)
    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def export_csv(self, request):
        # Get all event registrations
        registrations = EventRegistration.objects.all()

        # Calculate additional information
        total_registrations = registrations.count()
        total_canceled = registrations.filter(status='cancelled').count()
        total_revenue = sum(reg.event.price for reg in registrations if reg.status == 'registered')

        # Create a DataFrame
        data = []
        for reg in registrations:
            data.append({
                'Event': reg.event.title,
                'User': reg.user.email,
                'Status': reg.status,
                'Registration Date': reg.registration_date,
            })
        df = pd.DataFrame(data)

        # Add additional information to the DataFrame
        summary_data = {
            'Total Registrations': [total_registrations],
            'Total Canceled': [total_canceled],
            'Total Revenue': [total_revenue],
        }
        summary_df = pd.DataFrame(summary_data)

        # Convert DataFrame to CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="event_registrations.csv"'
        df.to_csv(path_or_buf=response, index=False)
        summary_df.to_csv(path_or_buf=response, index=False, mode='a')

        return response
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        instance.unregister()

    


