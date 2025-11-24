from django.db import models

from django.conf import settings
from django.db.models import UniqueConstraint


class Event(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    location = models.CharField(max_length=100, blank=True, null=True)
    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="events",
    )

    class Meta:
        ordering = ["-date"]
        db_table = "events"

    def __str__(self):
        return f"{self.title} ({self.date}, {self.location})"


class EventRegistration(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="event_registrations",
    )
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="registrations"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        db_table = "event_registrations"
        constraints = [
            UniqueConstraint(
                fields=["user", "event"],
                name="event_registration_unique",
            ),
        ]

    def __str__(self):
        return f"{self.user.username} → {self.event.title} at {self.created_at}"
