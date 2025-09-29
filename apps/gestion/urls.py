
from django.urls import path
from . import views

app_name = 'gestion'
urlpatterns = [
    # Destinations
    path("api/destinations/", views.DestinationListCreateView.as_view(), name="destination-list-create"),
    path("api/destinations/<int:pk>/", views.DestinationRetrieveUpdateDestroyView.as_view(), name="destination-detail"),

    # Flight Requests
    path("api/flight-requests/", views.TripsListCreateView.as_view(), name="flight-request-list-create"),
    path("api/flight-requests/<int:pk>/", views.FlightRequestRetrieveView.as_view(), name="flight-request-detail"),
    path("api/flight-requests/<int:pk>/mark_reserved/", views.FlightRequestMarkReservedView.as_view(), name="flight-request-mark-reserved"),

    # Notifications
    path("api/notifications/", views.NotificationListView.as_view(), name="notification-list"),
    path("api/notifications/<int:pk>/", views.NotificationRetrieveView.as_view(), name="notification-detail"),

    # Airports
    path("api/airports/", views.AirportListView.as_view(), name="airport-list"),

    # Trips
     path("api/trips/", views.TripsListView.as_view(), name="airport-list"),
]
