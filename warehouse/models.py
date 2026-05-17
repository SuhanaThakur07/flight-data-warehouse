from django.db import models

# Create your models here.
# from django.db import models

# Dimension Tables
class DimDate(models.Model):
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()

    class Meta:
        unique_together = ('year', 'month', 'day')

class DimAirline(models.Model):
    airline_code = models.CharField(max_length=10, unique=True)
    airline_name = models.CharField(max_length=100)

class DimAirport(models.Model):
    airport_code = models.CharField(max_length=10, unique=True)
    airport_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)

class DimCancellation(models.Model):
    reason_code = models.CharField(max_length=5, unique=True)
    reason_description = models.CharField(max_length=100)

# Fact Table
class FactFlights(models.Model):
    date = models.ForeignKey(DimDate, on_delete=models.CASCADE)
    airline = models.ForeignKey(DimAirline, on_delete=models.CASCADE)
    origin = models.ForeignKey(DimAirport, on_delete=models.CASCADE, related_name='departures')
    destination = models.ForeignKey(DimAirport, on_delete=models.CASCADE, related_name='arrivals')
    cancellation = models.ForeignKey(DimCancellation, on_delete=models.CASCADE, null=True, blank=True)
    departure_delay = models.FloatField(null=True, blank=True)
    arrival_delay = models.FloatField(null=True, blank=True)
    distance = models.FloatField(null=True, blank=True)
    air_time = models.FloatField(null=True, blank=True)
    cancelled = models.BooleanField(default=False)
