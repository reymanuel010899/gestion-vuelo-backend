from rest_framework import serializers
from .models import City, Destination, FlightRequest, Notification, Airport

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'

class AirportSerializer(serializers.ModelSerializer): # <--- NUEVO SERIALIZADOR
    city = CitySerializer()
    class Meta:
        model = Airport
        fields = ['city', 'destination', 'code', 'fee', 'name', 'description', ]  

class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = ["id", "name", "description", "image", "price", "duration", "is_active", "created_at", "updated_at"]

class FlightRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlightRequest
        fields = ["id", "user", "destination", "travel_date", "status", "created_at"]
        read_only_fields = ["user", "status", "created_at"]

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["id", "flight_request", "sent_at", "message"]
