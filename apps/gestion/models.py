from django.db import models
from apps.users.models import User


class Destination(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="destinations/", null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name
class City(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.PROTECT, related_name="cities", null=True, blank=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="cities/", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    def __str__(self):
        return self.name

class Airlines(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="airlines/", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    def __str__(self):
        return self.name

class Trips(models.Model):
    destination_from = models.ForeignKey(Destination, on_delete=models.PROTECT, related_name="trips_from", null=True, blank=True)
    destination_to = models.ForeignKey(Destination, on_delete=models.PROTECT, related_name="trips_to", null=True, blank=True)
    code = models.CharField(max_length=10, unique=True)
    duration = models.IntegerField(null=True, blank=True)
    image = models.ImageField(upload_to="airplanes/", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    def __str__(self):
        return f"from: {self.destination_from.name} - to:  {self.destination_to.name}"
    
class DepartureTime(models.Model):
    airlines = models.ForeignKey(Airlines, on_delete=models.PROTECT, related_name="departure_times", null=True, blank=True)
    trip = models.ForeignKey(Trips, on_delete=models.PROTECT, related_name="departure_times", null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    def __str__(self):
        return f"{self.price}"

class Airport(models.Model):
    city = models.ForeignKey(City, on_delete=models.PROTECT, related_name="airports", null=True, blank=True)
    destination = models.ForeignKey(Destination, on_delete=models.PROTECT, related_name="airports", null=True, blank=True)
    code = models.CharField(max_length=10, unique=True)
    fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="airports/", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name
    
class FlightRequest(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("reserved", "Reserved"),
        ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="flight_requests")
    destination = models.ForeignKey(Destination, on_delete=models.PROTECT, related_name="flight_requests", null=True, blank=True)
    travel_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    passengers = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} → {self.destination} ({self.status})"
    

class Notification(models.Model):
    flight_request = models.ForeignKey(FlightRequest, on_delete=models.CASCADE, related_name="notifications")
    sent_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField()

    def __str__(self):
        return f"Notification for {self.flight_request} at {self.sent_at}"