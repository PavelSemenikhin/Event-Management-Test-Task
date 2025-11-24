from django.urls import path, include

from rest_framework.routers import DefaultRouter

from event_management.views import EventViewSet

app_name = "event_management"

router = DefaultRouter()
router.register("events", EventViewSet, basename="events")


urlpatterns = [
    path("", include(router.urls)),
]
