from django.core.management.base import BaseCommand
from HarborHop.models import Port, Route, Vessel, Schedule
from datetime import timedelta
from django.utils import timezone

class Command(BaseCommand):
    help = 'Creates a complete Boracay route with test data'

    def handle(self, *args, **kwargs):
        # Create ports
        manila_port, _ = Port.objects.get_or_create(
            name='Manila Port',
            defaults={'capacity': 1000}
        )
        
        boracay_port, _ = Port.objects.get_or_create(
            name='Boracay Port',  # Changed from Caticlan Port to match the query
            defaults={'capacity': 500}
        )
        
        # Create vessel
        vessel, _ = Vessel.objects.get_or_create(
            name='FastCat Boracay Express',
            defaults={
                'current_port': 'Manila Port',
                'destination_port': 'Boracay Port',
                'seating_capacity': 150
            }
        )
        
        # Create route
        route, _ = Route.objects.get_or_create(
            departure_port=manila_port,
            arrival_port=boracay_port,
            defaults={
                'base_price': 999.00,
                'distance': 315.00,
                'duration': timedelta(hours=4),
                'is_active': True
            }
        )

        # Create schedules for the next 7 days
        today = timezone.now()
        for i in range(7):
            # Morning schedule - 8 AM
            morning_departure = today + timedelta(days=i)
            morning_departure = morning_departure.replace(hour=8, minute=0, second=0, microsecond=0)
            morning_arrival = morning_departure + route.duration
            
            Schedule.objects.get_or_create(
                route=route,
                vessel=vessel,
                departure_time=morning_departure,
                arrival_time=morning_arrival,
                defaults={
                    'available_seats': vessel.seating_capacity,
                    'status': 'SCHEDULED'
                }
            )
            
            # Afternoon schedule - 2 PM
            afternoon_departure = today + timedelta(days=i)
            afternoon_departure = afternoon_departure.replace(hour=14, minute=0, second=0, microsecond=0)
            afternoon_arrival = afternoon_departure + route.duration
            
            Schedule.objects.get_or_create(
                route=route,
                vessel=vessel,
                departure_time=afternoon_departure,
                arrival_time=afternoon_arrival,
                defaults={
                    'available_seats': vessel.seating_capacity,
                    'status': 'SCHEDULED'
                }
            )
        
        self.stdout.write(self.style.SUCCESS('Successfully created Boracay route with schedules'))