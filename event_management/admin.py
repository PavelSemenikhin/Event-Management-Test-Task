from django.contrib import admin

from event_management.models import Event, EventRegistration


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "location", "organizer")


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ("user", "event__title", "created_at")
