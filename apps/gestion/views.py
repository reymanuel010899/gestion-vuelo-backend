from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db.models import Q
from .models import  DepartureTime, Destination, Airport,  FlightRequest, Notification, Trips
from .serializers import DepartureTimeSerializer, DestinationSerializer, AirportSerializer, FlightRequestSerializer, NotificationSerializer, TripSerializer

class AirportListView(generics.ListAPIView):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = [permissions.AllowAny] 
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.query_params.get('q', None)
        if query:
            queryset = queryset.filter(
                Q(destination__name__icontains=query) |
                Q(name__icontains=query) |
                Q(code__icontains=query) 
            )
        return queryset

class DestinationListCreateView(generics.ListCreateAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    permission_classes = [permissions.AllowAny]

class DestinationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    permission_classes = [permissions.IsAuthenticated]

class TripsListCreateView(generics.ListCreateAPIView):
    serializer_class = TripSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Trips.objects.all()
        return Trips.objects.filter(user=user)

    def perform_create(self, serializer):
        airport_from = Airport.objects.get(name__icontains=self.request.data.get('destination_from', {}).get('name'))
        airport_to = Airport.objects.get(name__icontains=self.request.data.get('destination_to', {}).get('name'))
        origin = Destination.objects.get(name=airport_from.destination.name)
        destination = Destination.objects.get(name=airport_to.destination.name)
        serializer.save(user=self.request.user, destination_from=origin,
        destination_to=destination, airport=airport_from, is_active=True)

class FlightRequestListView(generics.ListAPIView):
    serializer_class = FlightRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return FlightRequest.objects.all().order_by('-created_at')[:10]

        return FlightRequest.objects.filter(user=user, status='pending')

class FlightRequestRetrieveView(generics.RetrieveAPIView):
    queryset = FlightRequest.objects.all()
    serializer_class = FlightRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

class FlightRequestMarkReservedView(generics.GenericAPIView):
    queryset = FlightRequest.objects.all()
    serializer_class = FlightRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        flight_request = self.get_object()
        flight_request.status = "reserved"
        flight_request.save()
        return Response({"status": "marked as reserved"}, status=status.HTTP_200_OK)

class DepartureTimeListView(generics.ListAPIView):
    queryset = DepartureTime.objects.all()
    serializer_class = DepartureTimeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        trips_id = self.request.query_params.get("tripsId")

        if trips_id is None:
            return DepartureTime.objects.none()

        try:
            trip = Trips.objects.get(id=int(trips_id))
        except (Trips.DoesNotExist, ValueError):
            return DepartureTime.objects.none()

        return queryset.filter(
            origin=trip.destination_from,
            destination=trip.destination_to,
            airport=trip.airport
        )

class TripBuyView(generics.GenericAPIView):
    queryset = DepartureTime.objects.all()
    serializer_class = DepartureTimeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        depure_time = self.get_object()
        trip = Trips.objects.filter(user=self.request.user, destination_from=depure_time.origin, destination_to=depure_time.destination).order_by('-created_at')[:1]
        flight_request = FlightRequest.objects.get(trip=trip)
        flight_request.status = "pending"
        flight_request.save()
        return Response({"status": "marked as pending"}, status=status.HTTP_200_OK)
    

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        user = self.request.user
        return Notification.objects.filter(flight_request__user=user)

class NotificationRetrieveView(generics.RetrieveAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
