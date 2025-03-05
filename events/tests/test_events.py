from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.utils import timezone
from events.models import Event, EventRegistration
from model_bakery import baker

User = get_user_model()

class TestCreateEvent(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='testuser@gmail.com', password='testpass')
        self.client.force_authenticate(user=self.user)

    def test_if_user_if_not_authenticated_return_401(self):
        client = APIClient()
        response = client.post('/events/', {'title': 'a'})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_authenticated_user_can_create_event(self):
        response = self.client.post('/events/', {
            'title': 'Test Event',
            'description': 'Test Description',
            'date': timezone.now() + timezone.timedelta(days=1),  # Ensure the date is in the future
            'time': '10:00:00',
            'location': 'Test Location',
            'price': '10.00',
            'capacity': 100,
            'organizer': self.user.id
        })
        assert response.status_code == status.HTTP_201_CREATED

    def test_if_event_creation_fails_with_invalid_data(self):
        response = self.client.post('/events/', {
            'title': '',
            'description': 'Test Description',
            'date': 'invalid-date',
            'time': 'invalid-time',
            'location': 'Test Location',
            'price': 'invalid-price',
            'capacity': -1,
            'organizer': self.user.id
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestRetrieveEvent(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='testuser@gmail.com', password='testpass')
        self.client.force_authenticate(user=self.user)

    def test_if_authenticated_user_can_retrieve_event_list(self):
        baker.make(Event, organizer=self.user, 
                   date = timezone.now() + timezone.timedelta(days=1)) # Ensure the date is in the future)
        response = self.client.get('/events/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) > 0

    def test_if_authenticated_user_can_retrieve_single_event(self):
        event = baker.make(Event, organizer=self.user,
                           date=timezone.now() + timezone.timedelta(days=1))
        response = self.client.get(f'/events/{event.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == event.title


class TestUpdateEvent(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='testuser@gmail.com', password='testpass')
        self.client.force_authenticate(user=self.user)

    def test_if_authenticated_user_can_update_event(self):
        event = baker.make(Event, organizer=self.user,
                           date = timezone.now() + timezone.timedelta(days=1))
        response = self.client.put(f'/events/{event.id}/', {
            'title': 'Updated Event',
            'description': 'Updated Description',
            'date': timezone.now() + timezone.timedelta(days=1),  # Ensure the date is in the future
            'time': '11:00:00',
            'location': 'Updated Location',
            'price': '20.00',
            'capacity': 200,
            'organizer': self.user.id
        })
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Updated Event'


class TestDeleteEvent(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='testuser@gmail.com', password='testpass')
        self.client.force_authenticate(user=self.user)

    def test_if_authenticated_user_can_delete_event(self):
        event = baker.make(Event, organizer=self.user,
                           date=timezone.now() + timezone.timedelta(days=1))
        response = self.client.delete(f'/events/{event.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Event.objects.count() == 0


class TestEventRegistration(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='testuser@gmail.com', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.event = baker.make(Event, organizer=self.user, 
                                date=timezone.now() + timezone.timedelta(days=1))

    def test_if_user_can_register_for_event(self):
        response = self.client.post('/registrations/', {
            'event': self.event.id,
            'status': 'registered'
        })
        assert response.status_code == status.HTTP_201_CREATED

    def test_if_registration_fails_when_event_is_full(self):
        self.event.capacity = 0
        self.event.save()
        response = self.client.post('/registrations/', {
            'event': self.event.id,
            'status': 'registered'
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'Cannot register for this event. Event is full.' in str(response.data)

    def test_if_user_can_cancel_registration(self):
        registration = baker.make(EventRegistration, event=self.event, user=self.user, status='registered')
        response = self.client.delete(f'/registrations/{registration.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert EventRegistration.objects.count() == 0

    def test_if_admin_can_export_registrations_to_csv(self):
        self.user.is_staff = True
        self.user.save()
        self.client.force_authenticate(user=self.user)
        baker.make(EventRegistration, event=self.event, user=self.user, status='registered')
        response = self.client.get('/registrations/export_csv/')
        assert response.status_code == status.HTTP_200_OK
        assert response['Content-Type'] == 'text/csv'
        assert 'attachment; filename="event_registrations.csv"' in response['Content-Disposition']

