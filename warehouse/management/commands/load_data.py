import pandas as pd
from django.core.management.base import BaseCommand
from warehouse.models import *

class Command(BaseCommand):
    help = 'Load flight data into warehouse'

    def handle(self, *args, **kwargs):

        # Load CSVs
        self.stdout.write('Loading airlines...')
        airlines_df = pd.read_csv('airlines.csv')
        for _, row in airlines_df.iterrows():
            DimAirline.objects.get_or_create(
                airline_code=row['IATA_CODE'],
                defaults={'airline_name': row['AIRLINE']}
            )

        self.stdout.write('Loading airports...')
        airports_df = pd.read_csv('airports.csv')
        for _, row in airports_df.iterrows():
            DimAirport.objects.get_or_create(
                airport_code=row['IATA_CODE'],
                defaults={
                    'airport_name': row['AIRPORT'],
                    'city': row['CITY'],
                    'state': row['STATE']
                }
            )

        # Cancellation reasons
        reasons = {
            'A': 'Airline/Carrier',
            'B': 'Weather',
            'C': 'NAS/National Air System',
            'D': 'Security'
        }
        for code, desc in reasons.items():
            DimCancellation.objects.get_or_create(
                reason_code=code,
                defaults={'reason_description': desc}
            )

        self.stdout.write('Loading flights (this may take a while)...')
        # Load only first 100,000 rows to keep it manageable
        flights_df = pd.read_csv('flights.csv', nrows=100000)

        for _, row in flights_df.iterrows():
            try:
                date, _ = DimDate.objects.get_or_create(
                    year=int(row['YEAR']),
                    month=int(row['MONTH']),
                    day=int(row['DAY'])
                )
                airline = DimAirline.objects.filter(airline_code=row['AIRLINE']).first()
                origin = DimAirport.objects.filter(airport_code=row['ORIGIN_AIRPORT']).first()
                destination = DimAirport.objects.filter(airport_code=row['DESTINATION_AIRPORT']).first()

                if not airline or not origin or not destination:
                    continue

                cancellation = None
                if pd.notna(row.get('CANCELLATION_REASON')):
                    cancellation = DimCancellation.objects.filter(
                        reason_code=row['CANCELLATION_REASON']
                    ).first()

                FactFlights.objects.create(
                    date=date,
                    airline=airline,
                    origin=origin,
                    destination=destination,
                    cancellation=cancellation,
                    departure_delay=row.get('DEPARTURE_DELAY'),
                    arrival_delay=row.get('ARRIVAL_DELAY'),
                    distance=row.get('DISTANCE'),
                    air_time=row.get('AIR_TIME'),
                    cancelled=bool(row.get('CANCELLED', 0))
                )
            except Exception as e:
                continue

        self.stdout.write(self.style.SUCCESS('✅ Data loaded successfully!'))