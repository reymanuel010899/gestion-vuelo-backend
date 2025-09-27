# views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Destination, FlightRequest, Notification
from .serializers import DestinationSerializer, FlightRequestSerializer, NotificationSerializer


class DestinationListCreateView(generics.ListCreateAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    permission_classes = [permissions.IsAdminUser]

class DestinationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    permission_classes = [permissions.IsAdminUser]


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
    permission_classes = [permissions.IsAdminUser]

    def patch(self, request, *args, **kwargs):
        flight_request = self.get_object()
        flight_request.status = "reserved"
        flight_request.save()
        return Response({"status": "marked as reserved"}, status=status.HTTP_200_OK)


class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Notification.objects.filter(flight_request__user=user)

class NotificationRetrieveView(generics.RetrieveAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
