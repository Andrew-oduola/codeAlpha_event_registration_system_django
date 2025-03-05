import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model

from events.models import Event  

from model_bakery import baker
from faker import Faker

User = get_user_model()

fake = Faker()

class Command(BaseCommand):
    help = "Populate the database with fake event data"

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help="Number of events to create")

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        
        self.stdout.write(self.style.SUCCESS(f'Generating {count} fake events...'))
        
        for _ in range(count):
            event = baker.make(Event,
                               title=fake.sentence(nb_words=6),  # Generates a 6-word event title
                               description=fake.paragraph(nb_sentences=3),  # 3-sentence description
                               location=fake.city(),  # Generates a random city name
                               date= timezone.now() + timezone.timedelta(days=random.randint(1, 60)), # Generates a random date between now and 60 days from now
                               organizer=User.objects.get(id=1))  # Generates random event data
            self.stdout.write(self.style.SUCCESS(f'Created event: {event}'))

        self.stdout.write(self.style.SUCCESS(f'Successfully populated {count} events!'))
