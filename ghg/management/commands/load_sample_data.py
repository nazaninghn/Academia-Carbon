from django.core.management.base import BaseCommand
from ghg.models import Country, EmissionData

class Command(BaseCommand):
    help = 'Load sample GHG emission data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Loading sample data...')
        
        # Create countries
        countries_data = [
            {'name': 'United States', 'code': 'USA'},
            {'name': 'China', 'code': 'CHN'},
            {'name': 'India', 'code': 'IND'},
            {'name': 'Russia', 'code': 'RUS'},
            {'name': 'Japan', 'code': 'JPN'},
            {'name': 'Germany', 'code': 'DEU'},
            {'name': 'Iran', 'code': 'IRN'},
            {'name': 'South Korea', 'code': 'KOR'},
            {'name': 'Saudi Arabia', 'code': 'SAU'},
            {'name': 'Canada', 'code': 'CAN'},
            {'name': 'Turkey', 'code': 'TUR'},
            {'name': 'United Kingdom', 'code': 'GBR'},
            {'name': 'France', 'code': 'FRA'},
            {'name': 'Italy', 'code': 'ITA'},
            {'name': 'Brazil', 'code': 'BRA'},
        ]
        
        for country_data in countries_data:
            country, created = Country.objects.get_or_create(
                code=country_data['code'],
                defaults={'name': country_data['name']}
            )
            if created:
                self.stdout.write(f'Created country: {country.name}')
        
        # Sample emission data
        emissions_data = [
            # USA
            {'country_code': 'USA', 'year': 2020, 'co2': 4713, 'methane': 650, 'nitrous_oxide': 320, 'total': 5683},
            {'country_code': 'USA', 'year': 2021, 'co2': 4850, 'methane': 655, 'nitrous_oxide': 318, 'total': 5823},
            {'country_code': 'USA', 'year': 2022, 'co2': 4920, 'methane': 660, 'nitrous_oxide': 315, 'total': 5895},
            {'country_code': 'USA', 'year': 2023, 'co2': 4880, 'methane': 658, 'nitrous_oxide': 312, 'total': 5850},
            
            # China
            {'country_code': 'CHN', 'year': 2020, 'co2': 10065, 'methane': 1200, 'nitrous_oxide': 580, 'total': 11845},
            {'country_code': 'CHN', 'year': 2021, 'co2': 10500, 'methane': 1220, 'nitrous_oxide': 590, 'total': 12310},
            {'country_code': 'CHN', 'year': 2022, 'co2': 10800, 'methane': 1240, 'nitrous_oxide': 595, 'total': 12635},
            {'country_code': 'CHN', 'year': 2023, 'co2': 11000, 'methane': 1250, 'nitrous_oxide': 600, 'total': 12850},
            
            # India
            {'country_code': 'IND', 'year': 2020, 'co2': 2442, 'methane': 850, 'nitrous_oxide': 420, 'total': 3712},
            {'country_code': 'IND', 'year': 2021, 'co2': 2580, 'methane': 870, 'nitrous_oxide': 425, 'total': 3875},
            {'country_code': 'IND', 'year': 2022, 'co2': 2720, 'methane': 890, 'nitrous_oxide': 430, 'total': 4040},
            {'country_code': 'IND', 'year': 2023, 'co2': 2850, 'methane': 900, 'nitrous_oxide': 435, 'total': 4185},
            
            # Russia
            {'country_code': 'RUS', 'year': 2020, 'co2': 1577, 'methane': 520, 'nitrous_oxide': 180, 'total': 2277},
            {'country_code': 'RUS', 'year': 2021, 'co2': 1620, 'methane': 525, 'nitrous_oxide': 182, 'total': 2327},
            {'country_code': 'RUS', 'year': 2022, 'co2': 1650, 'methane': 530, 'nitrous_oxide': 185, 'total': 2365},
            {'country_code': 'RUS', 'year': 2023, 'co2': 1680, 'methane': 535, 'nitrous_oxide': 187, 'total': 2402},
            
            # Turkey
            {'country_code': 'TUR', 'year': 2020, 'co2': 420, 'methane': 95, 'nitrous_oxide': 45, 'total': 560},
            {'country_code': 'TUR', 'year': 2021, 'co2': 435, 'methane': 98, 'nitrous_oxide': 46, 'total': 579},
            {'country_code': 'TUR', 'year': 2022, 'co2': 448, 'methane': 100, 'nitrous_oxide': 47, 'total': 595},
            {'country_code': 'TUR', 'year': 2023, 'co2': 460, 'methane': 102, 'nitrous_oxide': 48, 'total': 610},
            
            # Iran
            {'country_code': 'IRN', 'year': 2020, 'co2': 672, 'methane': 180, 'nitrous_oxide': 85, 'total': 937},
            {'country_code': 'IRN', 'year': 2021, 'co2': 690, 'methane': 185, 'nitrous_oxide': 87, 'total': 962},
            {'country_code': 'IRN', 'year': 2022, 'co2': 705, 'methane': 188, 'nitrous_oxide': 88, 'total': 981},
            {'country_code': 'IRN', 'year': 2023, 'co2': 720, 'methane': 190, 'nitrous_oxide': 90, 'total': 1000},
        ]
        
        for emission in emissions_data:
            country = Country.objects.get(code=emission['country_code'])
            EmissionData.objects.get_or_create(
                country=country,
                year=emission['year'],
                defaults={
                    'co2_emissions': emission['co2'],
                    'methane_emissions': emission['methane'],
                    'nitrous_oxide': emission['nitrous_oxide'],
                    'total_ghg': emission['total']
                }
            )
        
        self.stdout.write(self.style.SUCCESS('Sample data loaded successfully!'))
