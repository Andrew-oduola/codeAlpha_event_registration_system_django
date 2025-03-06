from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend

import pandas as pd
import csv

from .models import Event, EventRegistration
from .serializers import EventSerializer, EventRegistrationSerializer, AdminEventRegistrationSerializer
from .filters import EventFilter, EventRegistrationFilter

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = EventFilter
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['date', 'price', 'capacity']

class EventRegistrationViewSet(viewsets.ModelViewSet):
    queryset = EventRegistration.objects.all().select_related('event', 'user') # Use select_related to reduce the number of queries
    serializer_class = EventRegistrationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = EventRegistrationFilter
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    search_fields = ['event__title', 'user__email']
    ordering_fields = ['registration_date', 'status']

    def get_queryset(self):
        if self.request.user.is_staff:
            return EventRegistration.objects.all().select_related('event', 'user')
        return EventRegistration.objects.filter(user=self.request.user).select_related('event', 'user')

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return AdminEventRegistrationSerializer
        return EventRegistrationSerializer
    
    # Custom action to export event registrations to CSV (admin only)
    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def export_csv(self, request):
        # Get all event registrations
        registrations = EventRegistration.objects.all().select_related('event', 'user')

        # Calculate additional information
        total_registrations = registrations.count()
        total_canceled = registrations.filter(status='cancelled').count()
        total_revenue = sum(reg.event.price for reg in registrations if reg.status == 'registered')

        # Create a DataFrame
        data = registrations.values('event__title', 'user__email', 'status', 'registration_date') # QuerySet to list of dictionaries
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
