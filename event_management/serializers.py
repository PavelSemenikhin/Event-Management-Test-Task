from rest_framework import serializers

from event_management.models import Event, EventRegistration


class EventCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ("id", "title", "description", "date", "location", "organizer")
        read_only_fields = ("id",)


class EventReadSerializer(serializers.ModelSerializer):
    organizer = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
    )

    class Meta:
        model = Event
        fields = ("id", "title", "description", "date", "location", "organizer")
        read_only_fields = ("id",)


class EventRegistrationSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field="username")
    event = serializers.SlugRelatedField(read_only=True, slug_field="title")

    class Meta:
        model = EventRegistration
        fields = ("id", "user", "event", "created_at")
        read_only_fields = fields
