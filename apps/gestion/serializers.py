from rest_framework import serializers
from .models import City, DepartureTime, Destination, FlightRequest, Notification, Airport, Trips

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'

class AirportSerializer(serializers.ModelSerializer):
    city = CitySerializer()
    class Meta:
        model = Airport
        fields = ['city', 'destination', 'code', 'fee', 'name', 'description', ]

class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = ["id", "name", "description", "image", "price", "duration", "is_active", "created_at", "updated_at"]

class DepartureTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartureTime
        fields = ['id', 'airlines', 'trip', 'price', 'time', 'is_active', 'created_at', 'updated_at']

class DestiationSerializerRelate(serializers.Serializer):
    name = serializers.CharField(read_only=True)

class TripSerializer(serializers.ModelSerializer): 
    destination_from = DestiationSerializerRelate(read_only=True)
    destination_to = DestiationSerializerRelate(read_only=True)
    class Meta:
        model = Trips
        fields = ['destination_from', 'destination_to', 'passengers', 'exit_date', 'return_date', 'is_active', 'created_at', 'updated_at']  


class FlightRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlightRequest
        fields = ["id", "user", "destination", "travel_date", "status", "created_at"]
        read_only_fields = ["user", "status", "created_at"]

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["id", "flight_request", "sent_at", "message"]
