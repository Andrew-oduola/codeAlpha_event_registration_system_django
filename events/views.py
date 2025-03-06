from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.exceptions import ValidationError
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from django_filters.rest_framework import DjangoFilterBackend

import pandas as pd
import csv
import logging

from .models import Event, EventRegistration
from .serializers import EventSerializer, EventRegistrationSerializer, AdminEventRegistrationSerializer
from .filters import EventFilter, EventRegistrationFilter

logger = logging.getLogger(__name__)

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
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    @method_decorator(cache_page(60 * 1))
    def list(self, request, *args, **kwargs):
        logger.info("Listing events")
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error listing events: {e}")
            raise

    def create(self, request, *args, **kwargs):
        logger.info("Creating an event")
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            logger.error(f"Validation error creating event: {e}")
            raise
        except Exception as e:
            logger.error(f"Error creating event: {e}")
            raise

    def update(self, request, *args, **kwargs):
        logger.info(f"Updating event with ID {kwargs.get('pk')}")
        try:
            return super().update(request, *args, **kwargs)
        except ValidationError as e:
            logger.error(f"Validation error updating event with ID {kwargs.get('pk')}: {e}")
            raise
        except Exception as e:
            logger.error(f"Error updating event with ID {kwargs.get('pk')}: {e}")
            raise

    def destroy(self, request, *args, **kwargs):
        logger.info(f"Deleting event with ID {kwargs.get('pk')}")
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error deleting event with ID {kwargs.get('pk')}: {e}")
            raise

class EventRegistrationViewSet(viewsets.ModelViewSet):
    queryset = EventRegistration.objects.all().select_related('event', 'user')
    serializer_class = EventRegistrationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = EventRegistrationFilter
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    search_fields = ['event__title', 'user__email']
    ordering_fields = ['registration_date', 'status']
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    @method_decorator(cache_page(60 * 1))
    def get_queryset(self):
        try:
            if self.request.user.is_staff:
                logger.info("Fetching all event registrations for admin user")
                return EventRegistration.objects.all().select_related('event', 'user')
            logger.info(f"Fetching event registrations for user {self.request.user.email}")
            return EventRegistration.objects.filter(user=self.request.user).select_related('event', 'user')
        except Exception as e:
            logger.error(f"Error fetching event registrations: {e}")
            raise

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return AdminEventRegistrationSerializer
        return EventRegistrationSerializer
    
    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def export_csv(self, request):
        logger.info("Exporting event registrations to CSV")
        try:
            registrations = EventRegistration.objects.all().select_related('event', 'user')

            total_registrations = registrations.count()
            total_canceled = registrations.filter(status='cancelled').count()
            total_revenue = sum(reg.event.price for reg in registrations if reg.status == 'registered')

            data = registrations.values('event__title', 'user__email', 'status', 'registration_date')
            df = pd.DataFrame(data)

            summary_data = {
                'Total Registrations': [total_registrations],
                'Total Canceled': [total_canceled],
                'Total Revenue': [total_revenue],
            }
            summary_df = pd.DataFrame(summary_data)

            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="event_registrations.csv"'
            df.to_csv(path_or_buf=response, index=False)
            summary_df.to_csv(path_or_buf=response, index=False, mode='a')

            logger.info("Event registrations exported to CSV successfully")
            return response
        except Exception as e:
            logger.error(f"Error exporting event registrations to CSV: {e}")
            raise
    
    def perform_create(self, serializer):
        try:
            logger.info(f"Registering user {self.request.user.email} for event {serializer.validated_data['event'].title}")
            serializer.save(user=self.request.user)
        except ValidationError as e:
            logger.error(f"Validation error registering user {self.request.user.email} for event: {e}")
            raise
        except Exception as e:
            logger.error(f"Error registering user {self.request.user.email} for event: {e}")
            raise

    def perform_update(self, serializer):
        try:
            logger.info(f"Updating registration for user {self.request.user.email} for event {serializer.validated_data['event'].title}")
            serializer.save(user=self.request.user)
        except ValidationError as e:
            logger.error(f"Validation error updating registration for user {self.request.user.email} for event: {e}")
            raise
        except Exception as e:
            logger.error(f"Error updating registration for user {self.request.user.email} for event: {e}")
            raise

    def perform_destroy(self, instance):
        try:
            logger.info(f"Unregistering user {instance.user.email} from event {instance.event.title}")
            instance.unregister()
        except Exception as e:
            logger.error(f"Error unregistering user {instance.user.email} from event {instance.event.title}: {e}")
            raise
