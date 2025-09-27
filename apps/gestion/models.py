from django.db import models
from apps.users.models import User


class Destination(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    

class FlightRequest(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("reserved", "Reserved"),
        ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="flight_requests")
    destination = models.ForeignKey("Destination", on_delete=models.PROTECT, related_name="flight_requests")
    travel_date = models.DateField()
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