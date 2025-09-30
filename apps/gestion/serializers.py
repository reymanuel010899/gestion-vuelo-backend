from apps.users.models import User
from rest_framework import serializers
from .models import Airlines, City, DepartureTime, Destination, FlightRequest, Notification, Airport, Trips

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
class AirlinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airlines
        fields = ['id', 'name', 'description']

class DepartureTimeSerializer(serializers.ModelSerializer):
    airlines= AirlinesSerializer()
    origin = DestinationSerializer()
    destination = DestinationSerializer()
    airport = AirportSerializer()
    class Meta:
        model = DepartureTime
        fields = ['id', 'airlines','origin', 'destination', 'duration', 'airport',  'price', 'time', 'is_active', 'created_at', 'updated_at']

class DestiationSerializerRelate(serializers.Serializer):
    name = serializers.CharField(read_only=True)

class TripSerializer(serializers.ModelSerializer): 
    destination_from = DestiationSerializerRelate(read_only=True)
    destination_to = DestiationSerializerRelate(read_only=True)
    class Meta:
        model = Trips
        fields = ['id','destination_from', 'destination_to', 'passengers', 'exit_date', 'return_date', 'is_active', 'created_at', 'updated_at']  

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'is_staff', 'gmail']


class FlightRequestSerializer(serializers.ModelSerializer):
    trip = TripSerializer()
    user = UserSerializer(read_only=True)  
    class Meta:
        model = FlightRequest
        fields = ["id", "user", 'trip', "status", "created_at"]
        read_only_fields = ["user", "status", "created_at"]

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["id", "flight_request", "sent_at", "message"]
