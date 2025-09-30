
from django.urls import path
from . import views

app_name = 'gestion'
urlpatterns = [
    # Destinations
    path("api/destinations/", views.DestinationListCreateView.as_view(), name="destination-list-create"),
    path("api/destinations/<int:pk>/", views.DestinationRetrieveUpdateDestroyView.as_view(), name="destination-detail"),

    # Flight Requests
    path("api/flight-requests/", views.TripsListCreateView.as_view(), name="flight-request-list-create"),
    path('api/flight-requests/mark-reserved/<int:pk>/', views.FlightRequestMarkReservedView.as_view(), name='flight-mark-reserved'),
    path("api/flight-requests-list/", views.FlightRequestListView.as_view(), name="flight-request-list"),
    path("api/flight-requests/<int:pk>/", views.FlightRequestRetrieveView.as_view(), name="flight-request-detail"),

    # Notifications
    path("api/notifications/", views.NotificationListView.as_view(), name="notification-list"),
    path("api/notifications/<int:pk>/", views.NotificationRetrieveView.as_view(), name="notification-detail"),

    # Airports
    path("api/airports/", views.AirportListView.as_view(), name="airport-list"),

    # Departure-time
    path("api/departure-time/", views.DepartureTimeListView.as_view(), name="departure-time-list"),
    path("api/departure-time/trips-buy/<int:pk>/", views.TripBuyView.as_view(), name="departure-time-list")
]
