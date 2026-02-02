"""
Management command to load initial emission sources data
Load initial emission sources data
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from ghg.models_emission_sources import (
    EmissionScope, EmissionCategory, EmissionSource, EmissionFactorData
)


class Command(BaseCommand):
    help = 'Load initial emission sources and factors data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Loading emission sources data...'))
        
        # Get or create admin user
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        
        # Create Scopes
        self.stdout.write('📊 Creating Scopes...')
        scope1, _ = EmissionScope.objects.get_or_create(
            scope_number='1',
            defaults={
                'name_en': 'Direct Emissions',
                'name_tr': 'Doğrudan Emisyonlar',
                'description_en': 'Direct GHG emissions from sources owned or controlled by the organization',
                'description_tr': 'Kuruluşa ait veya kontrol edilen kaynaklardan doğrudan sera gazı emisyonları',
                'icon': '🔥',
                'color': '#ef4444',
                'display_order': 1,
                'created_by': admin_user
            }
        )
        
        scope2, _ = EmissionScope.objects.get_or_create(
            scope_number='2',
            defaults={
                'name_en': 'Indirect Emissions (Energy)',
                'name_tr': 'Dolaylı Emisyonlar (Enerji)',
                'description_en': 'Indirect GHG emissions from purchased electricity, heat, or steam',
                'description_tr': 'Satın alınan elektrik, ısı veya buhardan dolaylı sera gazı emisyonları',
                'icon': '⚡',
                'color': '#f59e0b',
                'display_order': 2,
                'created_by': admin_user
            }
        )
        
        scope3, _ = EmissionScope.objects.get_or_create(
            scope_number='3',
            defaults={
                'name_en': 'Other Indirect Emissions',
                'name_tr': 'Diğer Dolaylı Emisyonlar',
                'description_en': 'All other indirect GHG emissions in the value chain',
                'description_tr': 'Değer zincirindeki diğer tüm dolaylı sera gazı emisyonları',
                'icon': '🌍',
                'color': '#3b82f6',
                'display_order': 3,
                'created_by': admin_user
            }
        )
        
        self.stdout.write(self.style.SUCCESS('✅ Scopes created'))
        
        # ============================================
        # SCOPE 1 - Categories and Sources
        # ============================================
        self.stdout.write('🔥 Creating Scope 1 categories and sources...')
        
        # Stationary Combustion
        cat_stationary, _ = EmissionCategory.objects.get_or_create(
            scope=scope1,
            code='stationary',
            defaults={
                'name_en': 'Stationary Combustion',
                'name_tr': 'Sabit Yanma',
                'description_en': 'Emissions from fuel combustion in stationary equipment',
                'description_tr': 'Sabit ekipmanlarda yakıt yanmasından kaynaklanan emisyonlar',
                'icon': '🏭',
                'display_order': 1,
                'created_by': admin_user
            }
        )
        
        # Natural Gas
        source_ng, _ = EmissionSource.objects.get_or_create(
            category=cat_stationary,
            code='natural-gas',
            defaults={
                'name_en': 'Natural Gas',
                'name_tr': 'Doğal Gaz',
                'description_en': 'Natural gas combustion',
                'description_tr': 'Doğal gaz yanması',
                'default_unit': 'm³',
                'alternative_units': ['kg', 'GJ', 'kWh'],
                'icon': '🔥',
                'display_order': 1,
                'created_by': admin_user
            }
        )
        
        # Add emission factors for Natural Gas
        EmissionFactorData.objects.get_or_create(
            source=source_ng,
            country_code='turkey',
            defaults={
                'country_name': 'Turkey',
                'factor_value': 2.03,
                'unit': 'm³',
                'reference_source': 'Turkey 2025 Official Factors',
                'reference_year': 2025,
                'is_active': True,
                'is_default': True,
                'data_quality_rating': 'high',
                'created_by': admin_user
            }
        )
        
        EmissionFactorData.objects.get_or_create(
            source=source_ng,
            country_code='global',
            defaults={
                'country_name': 'Global',
                'factor_value': 2.0,
                'unit': 'm³',
                'reference_source': 'IPCC 2006',
                'reference_year': 2006,
                'is_active': True,
                'is_default': False,
                'data_quality_rating': 'medium',
                'created_by': admin_user
            }
        )
        
        # Diesel
        source_diesel, _ = EmissionSource.objects.get_or_create(
            category=cat_stationary,
            code='diesel',
            defaults={
                'name_en': 'Diesel',
                'name_tr': 'Dizel',
                'description_en': 'Diesel fuel combustion',
                'description_tr': 'Dizel yakıt yanması',
                'default_unit': 'liters',
                'alternative_units': ['kg', 'GJ'],
                'icon': '⛽',
                'display_order': 2,
                'created_by': admin_user
            }
        )
        
        EmissionFactorData.objects.get_or_create(
            source=source_diesel,
            country_code='turkey',
            defaults={
                'country_name': 'Turkey',
                'factor_value': 2.68,
                'unit': 'liters',
                'reference_source': 'Turkey 2025 Official Factors',
                'reference_year': 2025,
                'is_active': True,
                'is_default': True,
                'data_quality_rating': 'high',
                'created_by': admin_user
            }
        )
        
        # Mobile Combustion
        cat_mobile, _ = EmissionCategory.objects.get_or_create(
            scope=scope1,
            code='mobile',
            defaults={
                'name_en': 'Mobile Combustion',
                'name_tr': 'Hareketli Yanma',
                'description_en': 'Emissions from fuel combustion in mobile sources',
                'description_tr': 'Hareketli kaynaklarda yakıt yanmasından kaynaklanan emisyonlar',
                'icon': '🚗',
                'display_order': 2,
                'created_by': admin_user
            }
        )
        
        # Petrol
        source_petrol, _ = EmissionSource.objects.get_or_create(
            category=cat_mobile,
            code='petrol',
            defaults={
                'name_en': 'Petrol/Gasoline',
                'name_tr': 'Benzin',
                'description_en': 'Petrol/Gasoline combustion in vehicles',
                'description_tr': 'Araçlarda benzin yanması',
                'default_unit': 'liters',
                'alternative_units': ['kg', 'GJ'],
                'icon': '⛽',
                'display_order': 1,
                'created_by': admin_user
            }
        )
        
        EmissionFactorData.objects.get_or_create(
            source=source_petrol,
            country_code='turkey',
            defaults={
                'country_name': 'Turkey',
                'factor_value': 2.31,
                'unit': 'liters',
                'reference_source': 'Turkey 2025 Official Factors',
                'reference_year': 2025,
                'is_active': True,
                'is_default': True,
                'data_quality_rating': 'high',
                'created_by': admin_user
            }
        )
        
        self.stdout.write(self.style.SUCCESS('✅ Scope 1 data loaded'))
        
        # ============================================
        # SCOPE 2 - Categories and Sources
        # ============================================
        self.stdout.write('⚡ Creating Scope 2 categories and sources...')
        
        # Electricity
        cat_electricity, _ = EmissionCategory.objects.get_or_create(
            scope=scope2,
            code='electricity',
            defaults={
                'name_en': 'Purchased Electricity',
                'name_tr': 'Satın Alınan Elektrik',
                'description_en': 'Emissions from purchased electricity',
                'description_tr': 'Satın alınan elektrikten kaynaklanan emisyonlar',
                'icon': '⚡',
                'display_order': 1,
                'created_by': admin_user
            }
        )
        
        # Grid Electricity
        source_elec, _ = EmissionSource.objects.get_or_create(
            category=cat_electricity,
            code='grid-electricity',
            defaults={
                'name_en': 'Grid Electricity',
                'name_tr': 'Şebeke Elektriği',
                'description_en': 'Electricity from national grid',
                'description_tr': 'Ulusal şebekeden elektrik',
                'default_unit': 'kWh',
                'alternative_units': ['MWh', 'GJ'],
                'icon': '🔌',
                'display_order': 1,
                'created_by': admin_user
            }
        )
        
        EmissionFactorData.objects.get_or_create(
            source=source_elec,
            country_code='turkey',
            defaults={
                'country_name': 'Turkey',
                'factor_value': 0.452,
                'unit': 'kWh',
                'reference_source': 'Turkey 2025 Grid Factor',
                'reference_year': 2025,
                'is_active': True,
                'is_default': True,
                'data_quality_rating': 'high',
                'created_by': admin_user
            }
        )
        
        EmissionFactorData.objects.get_or_create(
            source=source_elec,
            country_code='global',
            defaults={
                'country_name': 'Global',
                'factor_value': 0.5,
                'unit': 'kWh',
                'reference_source': 'IEA Global Average',
                'reference_year': 2023,
                'is_active': True,
                'is_default': False,
                'data_quality_rating': 'medium',
                'created_by': admin_user
            }
        )
        
        self.stdout.write(self.style.SUCCESS('✅ Scope 2 data loaded'))
        
        # ============================================
        # SCOPE 3 - Categories and Sources
        # ============================================
        self.stdout.write('🌍 Creating Scope 3 categories and sources...')
        
        # Business Travel
        cat_travel, _ = EmissionCategory.objects.get_or_create(
            scope=scope3,
            code='business-travel',
            defaults={
                'name_en': 'Business Travel',
                'name_tr': 'İş Seyahati',
                'description_en': 'Emissions from business travel',
                'description_tr': 'İş seyahatinden kaynaklanan emisyonlar',
                'icon': '✈️',
                'display_order': 1,
                'created_by': admin_user
            }
        )
        
        # Air Travel
        source_air, _ = EmissionSource.objects.get_or_create(
            category=cat_travel,
            code='air-travel',
            defaults={
                'name_en': 'Air Travel',
                'name_tr': 'Hava Yolu Seyahati',
                'description_en': 'Emissions from air travel',
                'description_tr': 'Hava yolu seyahatinden kaynaklanan emisyonlar',
                'default_unit': 'km',
                'alternative_units': ['miles', 'passenger-km'],
                'icon': '✈️',
                'display_order': 1,
                'created_by': admin_user
            }
        )
        
        EmissionFactorData.objects.get_or_create(
            source=source_air,
            country_code='global',
            defaults={
                'country_name': 'Global',
                'factor_value': 0.255,
                'unit': 'km',
                'reference_source': 'DEFRA 2024',
                'reference_year': 2024,
                'is_active': True,
                'is_default': True,
                'data_quality_rating': 'high',
                'created_by': admin_user
            }
        )
        
        self.stdout.write(self.style.SUCCESS('✅ Scope 3 data loaded'))
        
        # Summary
        self.stdout.write(self.style.SUCCESS('\n' + '='*50))
        self.stdout.write(self.style.SUCCESS('📊 Summary:'))
        self.stdout.write(f'   Scopes: {EmissionScope.objects.count()}')
        self.stdout.write(f'   Categories: {EmissionCategory.objects.count()}')
        self.stdout.write(f'   Sources: {EmissionSource.objects.count()}')
        self.stdout.write(f'   Emission Factors: {EmissionFactorData.objects.count()}')
        self.stdout.write(self.style.SUCCESS('='*50))
        self.stdout.write(self.style.SUCCESS('\n✅ All data loaded successfully!'))
        self.stdout.write(self.style.WARNING('\n💡 You can now add more sources via Django Admin Panel'))
