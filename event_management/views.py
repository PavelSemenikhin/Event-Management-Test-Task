from django.db import IntegrityError
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from event_management.models import Event, EventRegistration
from event_management.serializers import (
    EventCreateSerializer,
    EventReadSerializer,
    EventRegistrationSerializer,
)
from event_management.tasks import send_event_registration_email


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["title", "location"]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return EventCreateSerializer
        return EventReadSerializer

    @extend_schema(
        request=None,
        responses={201: EventRegistrationSerializer},
    )
    @action(detail=True, methods=["post"])
    def register(self, request, pk=None):  # noqa
        event = self.get_object()
        user = self.request.user

        try:
            reg = EventRegistration.objects.create(event=event, user=user)
        except IntegrityError:
            return Response(
                {"detail": "Already registered"},
                status=status.HTTP_409_CONFLICT,
            )

        serializer = EventRegistrationSerializer(reg)
        data = serializer.data
        data["detail"] = "Event registered successfully"

        send_event_registration_email.delay(
            user_email=user.email,
            event_title=event.title,
            event_date=str(event.date),
            event_location=event.location,
            event_description=event.description,
        )

        return Response(data, status=status.HTTP_201_CREATED)

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [permissions.IsAdminUser()]
        if self.action == "register":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]
