from django.contrib import admin
from  .models import Destination, DepartureTime, Airlines, Trips, FlightRequest, Notification, Airport, City
# Register your models here.

class FlightRequestAdmin(admin.ModelAdmin):
    list_display = ('id',)

admin.site.register(Destination)
admin.site.register(FlightRequest, FlightRequestAdmin)
admin.site.register(Notification)
admin.site.register(Airport)
admin.site.register(City)
admin.site.register(DepartureTime)
admin.site.register(Airlines)
admin.site.register(Trips)
