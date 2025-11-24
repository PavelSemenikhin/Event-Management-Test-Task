from django.db import IntegrityError
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, request, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from event_management.models import Event, EventRegistration
from event_management.serializers import (
    EventCreateSerializer,
    EventReadSerializer,
    EventRegistrationSerializer,
)


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return EventCreateSerializer
        return EventReadSerializer

    @extend_schema(
        request=None,
        responses={201: EventRegistrationSerializer},
    )
    @action(detail=True, methods=["post"])
    def register(self, request, pk=None):
        event = self.get_object()
        user = self.request.user

        try:
            EventRegistration.objects.create(event=event, user=user)
        except IntegrityError:
            return Response(
                {"detail": "Already registered"},
                status=status.HTTP_409_CONFLICT,
            )
        return Response(
            {"detail": "Event registered successfully"},
            status=status.HTTP_201_CREATED,
        )

    def get_permissions(self):
        if self.action == "register":
            return [permissions.IsAuthenticated()]
        return super().get_permissions()
