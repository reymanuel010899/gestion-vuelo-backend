
from django.urls import path
from .views import (
    DestinationListCreateView,
    DestinationRetrieveUpdateDestroyView,
    FlightRequestListCreateView,
    FlightRequestRetrieveView,
    FlightRequestMarkReservedView,
    NotificationListView,
    NotificationRetrieveView
)

app_name = 'gestion'
urlpatterns = [
    # Destinations
    path("api/destinations/", DestinationListCreateView.as_view(), name="destination-list-create"),
    path("api/destinations/<int:pk>/", DestinationRetrieveUpdateDestroyView.as_view(), name="destination-detail"),

    # Flight Requests
    path("api/flight-requests/", FlightRequestListCreateView.as_view(), name="flight-request-list-create"),
    path("api/flight-requests/<int:pk>/", FlightRequestRetrieveView.as_view(), name="flight-request-detail"),
    path("api/flight-requests/<int:pk>/mark_reserved/", FlightRequestMarkReservedView.as_view(), name="flight-request-mark-reserved"),

    # Notifications
    path("api/notifications/", NotificationListView.as_view(), name="notification-list"),
    path("api/notifications/<int:pk>/", NotificationRetrieveView.as_view(), name="notification-detail"),
]
