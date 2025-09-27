from rest_framework import serializers
from .models import Destination, FlightRequest, Notification

class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = ["id", "name"]

class FlightRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlightRequest
        fields = ["id", "user", "destination", "travel_date", "status", "created_at"]
        read_only_fields = ["user", "status", "created_at"]

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["id", "flight_request", "sent_at", "message"]
