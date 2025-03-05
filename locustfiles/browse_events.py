from locust import HttpUser, TaskSet, task, between
from django.utils import timezone
import json

import os
import django

# Set the settings module manually
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_reg_sys.settings')  # Change 'your_project' to your actual project name

# Initialize Django
django.setup()
from django.contrib.auth import get_user_model


User = get_user_model()

class EventManagementTasks(TaskSet):
    def on_start(self):
        # Authenticate user
        self.login()

    def login(self):
        response = self.client.post("/auth/jwt/create/", json={
            "email": "ayobamioduola13@gmail.com",
            "password": "secret"
        })
        self.token = response.json()["access"]
        self.client.headers.update({"Authorization": f"JWT {self.token}"})

    @task(1)
    def view_events(self):
        self.client.get("/events/")

    @task(2)
    def create_event(self):
        event_data = {
            "title": "Performance Test Event",
            "description": "This is a test event for performance testing.",
            "date": (timezone.now() + timezone.timedelta(days=1)).isoformat(),
            "time": "10:00:00",
            "location": "Test Location",
            "price": "10.00",
            "capacity": 100,
            "organizer": 1  # Assuming the organizer ID is 1
        }
        self.client.post("/events/", json=event_data)

    @task(3)
    def register_for_event(self):
        # Assuming the event ID is 1
        registration_data = {
            "event": 1,
            "user": User.objects.get(id=1).id
        }
        self.client.post("/registrations/", json=registration_data)

    @task(4)
    def search_events(self):
        self.client.get("/events/?search=Performance")

    @task(5)
    def filter_events(self):
        self.client.get("/events/?date_gt=2025-03-01")

class EventManagementUser(HttpUser):
    tasks = [EventManagementTasks]
    wait_time = between(1, 5)