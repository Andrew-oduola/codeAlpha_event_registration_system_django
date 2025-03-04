from django.db import models
from django.core.exceptions import ValidationError


class EventCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)


    def __str__(self):
        return self.name

# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(EventCategory, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField()
    time = models.TimeField()
    location = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.PositiveIntegerField()
    organizer = models.ForeignKey('customusers.CustomUser', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    def is_full(self):
        return self.capacity <= EventRegistration.objects.filter(event=self).count()
        


class EventRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    user = models.ForeignKey('customusers.CustomUser', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, 
                              default='registered', 
                              choices=[
                                  ('pending', 'Pending'),  
                                  ('registered', 'Registered'),
                                  ('cancelled', 'Cancelled')
                                  ])
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.event}'
    
    class Meta:
        unique_together = ('event', 'user')

    def is_full(self):
        return self.event.capacity <= EventRegistration.objects.filter(event=self.event).count()
    
    def is_registered(self):
        return EventRegistration.objects.filter(event=self.event, user=self.user).exists()
    
    def register(self):
        if not self.is_full() and not self.is_registered():
            self.save()
            return True
        return False
    
    def unregister(self):
        if self.is_registered():
            self.delete()
            return True
        return False
    
    def get_total_revenue(self):
        return EventRegistration.objects.filter(event=self.event).count() * self.event.price
    
    def get_total_attendees(self):
        return EventRegistration.objects.filter(event=self.event).count()
    
    def save(self, *args, **kwargs):
        if self.is_full():
            raise ValidationError('Cannot register for this event. Event is full.')
        super().save(*args, **kwargs)
