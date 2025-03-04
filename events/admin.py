from django.contrib import admin
from .models import Event, EventRegistration, EventCategory

# Register your models here.
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass

@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    pass

@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    pass
