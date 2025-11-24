from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins, permissions

from accounts.serializers import RegistrationSerializer

User = get_user_model()


class RegisterViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Endpoint for registering new users."""

    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = (permissions.AllowAny,)
