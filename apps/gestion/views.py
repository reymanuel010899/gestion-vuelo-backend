# views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.permissions import AllowAny, IsAuthenticated 
from .models import Destination, Airport,  FlightRequest, Notification
from .serializers import DestinationSerializer, AirportSerializer, FlightRequestSerializer, NotificationSerializer

class AirportListView(generics.ListAPIView): # <--- NUEVA VISTA
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

class FlightRequestListCreateView(generics.ListCreateAPIView):
    serializer_class = FlightRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return FlightRequest.objects.all()
        return FlightRequest.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

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
