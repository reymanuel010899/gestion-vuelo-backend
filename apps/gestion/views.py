# views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.permissions import AllowAny, IsAuthenticated 
from .models import  DepartureTime, Destination, Airport,  FlightRequest, Notification, Trips
from .serializers import DepartureTimeSerializer, DestinationSerializer, AirportSerializer, FlightRequestSerializer, NotificationSerializer, TripSerializer

class AirportListView(generics.ListAPIView):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = [AllowAny] # Permite a cualquier usuario buscar aeropuertos

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.query_params.get('q', None)
        if query:
            # Filtra por nombre, código, ciudad o país
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
        destination_to=destination, is_active=True)

class FlightRequestRetrieveView(generics.RetrieveAPIView):
    queryset = FlightRequest.objects.all()
    serializer_class = FlightRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

class FlightRequestMarkReservedView(generics.UpdateAPIView):
    queryset = FlightRequest.objects.all()
    serializer_class = FlightRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        flight_request = self.get_object()
        flight_request.status = "reserved"
        flight_request.save()
        return Response({"status": "marked as reserved"}, status=status.HTTP_200_OK)

class TripsListView(generics.ListAPIView):
    queryset = Trips.objects.all()
    serializer_class = TripSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        destination = self.request.query_params.get('to', None)
        origin = self.request.query_params.get('from', None)
        if destination and origin:
            queryset = queryset.filter(
              destination_from__name=origin, destination_to__name=destination
            )
            return queryset
        else:
            return []

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
