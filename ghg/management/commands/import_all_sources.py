"""
Import all emission sources from emission_factors.py to database
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from ghg.models_emission_sources import EmissionScope, EmissionCategory, EmissionSource, EmissionFactorData
from ghg import emission_factors
from ghg.source_names_tr import SOURCE_NAMES_TR

class Command(BaseCommand):
    help = 'Import all emission sources from emission_factors.py to database'

    def handle(self, *args, **options):
        self.stdout.write('🚀 Importing all emission sources...\n')
        
        # Get or create admin user
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'admin')
        
        # Create scopes
        scope1, _ = EmissionScope.objects.get_or_create(
            scope_number='1',
            defaults={
                'name_en': 'Direct Emissions',
                'name_tr': 'Doğrudan Emisyonlar',
                'description_en': 'Direct GHG emissions from sources owned or controlled by the organization',
                'description_tr': 'Kuruluşun sahip olduğu veya kontrol ettiği kaynaklardan doğrudan sera gazı emisyonları',
                'icon': '🔥',
                'color': '#ef4444',
                'created_by': admin_user
            }
        )
        
        scope2, _ = EmissionScope.objects.get_or_create(
            scope_number='2',
            defaults={
                'name_en': 'Indirect Emissions (Energy)',
                'name_tr': 'Dolaylı Emisyonlar (Enerji)',
                'description_en': 'Indirect GHG emissions from purchased electricity, heat, or steam',
                'description_tr': 'Satın alınan elektrik, ısı veya buhardan kaynaklanan dolaylı sera gazı emisyonları',
                'icon': '⚡',
                'color': '#3b82f6',
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
                'color': '#10b981',
                'created_by': admin_user
            }
        )
        
        self.stdout.write('✅ Scopes created\n')
        
        # SCOPE 1 CATEGORIES
        cat_stationary, _ = EmissionCategory.objects.get_or_create(
            scope=scope1,
            code='stationary',
            defaults={
                'name_en': 'Stationary Combustion',
                'name_tr': 'Sabit Yanma',
                'description_en': 'Fuel combustion in stationary equipment',
                'description_tr': 'Sabit ekipmanlarda yakıt yanması',
                'icon': '🔥',
                'display_order': 1,
                'created_by': admin_user
            }
        )
        
        cat_mobile, _ = EmissionCategory.objects.get_or_create(
            scope=scope1,
            code='mobile',
            defaults={
                'name_en': 'Mobile Combustion',
                'name_tr': 'Hareketli Yanma',
                'description_en': 'Fuel combustion in mobile sources',
                'description_tr': 'Hareketli kaynaklarda yakıt yanması',
                'icon': '🚗',
                'display_order': 2,
                'created_by': admin_user
            }
        )
        
        cat_fugitive, _ = EmissionCategory.objects.get_or_create(
            scope=scope1,
            code='fugitive',
            defaults={
                'name_en': 'Fugitive Emissions',
                'name_tr': 'Kaçak Emisyonlar',
                'description_en': 'Refrigerants, methane leaks, etc.',
                'description_tr': 'Soğutucu akışkan ve metan sızıntıları vb.',
                'icon': '💨',
                'display_order': 3,
                'created_by': admin_user
            }
        )
        
        # SCOPE 2 CATEGORIES
        cat_electricity, _ = EmissionCategory.objects.get_or_create(
            scope=scope2,
            code='electricity',
            defaults={
                'name_en': 'Purchased Electricity',
                'name_tr': 'Satın Alınan Elektrik',
                'description_en': 'Electricity purchased from grid',
                'description_tr': 'Şebekeden satın alınan elektrik',
                'icon': '⚡',
                'display_order': 1,
                'created_by': admin_user
            }
        )
        
        cat_steam, _ = EmissionCategory.objects.get_or_create(
            scope=scope2,
            code='steam-heat',
            defaults={
                'name_en': 'Steam & Heat',
                'name_tr': 'Buhar ve Isı',
                'description_en': 'Purchased steam, heat, or cooling',
                'description_tr': 'Satın alınan buhar, ısı veya soğutma',
                'icon': '♨️',
                'display_order': 2,
                'created_by': admin_user
            }
        )
        
        # SCOPE 3 CATEGORIES
        cat_travel, _ = EmissionCategory.objects.get_or_create(
            scope=scope3,
            code='travel',
            defaults={
                'name_en': 'Business Travel',
                'name_tr': 'İş Seyahati',
                'description_en': 'Employee business travel',
                'description_tr': 'Çalışanların iş seyahatleri',
                'icon': '✈️',
                'display_order': 1,
                'created_by': admin_user
            }
        )
        
        cat_commuting, _ = EmissionCategory.objects.get_or_create(
            scope=scope3,
            code='commuting',
            defaults={
                'name_en': 'Employee Commuting',
                'name_tr': 'Çalışan Ulaşımı',
                'description_en': 'Employee commuting to work',
                'description_tr': 'Çalışanların işe ulaşımı',
                'icon': '🚌',
                'display_order': 2,
                'created_by': admin_user
            }
        )
        
        cat_purchased_goods, _ = EmissionCategory.objects.get_or_create(
            scope=scope3,
            code='purchased-goods',
            defaults={
                'name_en': 'Purchased Goods & Services',
                'name_tr': 'Satın Alınan Mal ve Hizmetler',
                'description_en': 'Raw materials, products, services',
                'description_tr': 'Hammaddeler, ürünler, hizmetler',
                'icon': '📦',
                'display_order': 3,
                'created_by': admin_user
            }
        )
        
        cat_waste, _ = EmissionCategory.objects.get_or_create(
            scope=scope3,
            code='waste',
            defaults={
                'name_en': 'Waste',
                'name_tr': 'Atık',
                'description_en': 'Waste disposal and treatment',
                'description_tr': 'Atık bertarafı ve işleme',
                'icon': '🗑️',
                'display_order': 4,
                'created_by': admin_user
            }
        )
        
        cat_water, _ = EmissionCategory.objects.get_or_create(
            scope=scope3,
            code='water',
            defaults={
                'name_en': 'Water',
                'name_tr': 'Su',
                'description_en': 'Water supply and treatment',
                'description_tr': 'Su temini ve arıtma',
                'icon': '💧',
                'display_order': 5,
                'created_by': admin_user
            }
        )
        
        cat_upstream_transport, _ = EmissionCategory.objects.get_or_create(
            scope=scope3,
            code='upstream-transport',
            defaults={
                'name_en': 'Upstream Transportation',
                'name_tr': 'Yukarı Yönlü Taşımacılık',
                'description_en': 'Transportation of purchased goods',
                'description_tr': 'Satın alınan malların taşınması',
                'icon': '🚚',
                'display_order': 6,
                'created_by': admin_user
            }
        )
        
        self.stdout.write('✅ Categories created\n')
        
        # Import sources
        total_sources = 0
        
        # STATIONARY COMBUSTION
        self.stdout.write('📝 Importing Stationary Combustion sources...')
        for key, data in emission_factors.STATIONARY_COMBUSTION.items():
            source, created = EmissionSource.objects.get_or_create(
                category=cat_stationary,
                code=key,
                defaults={
                    'name_en': data['name'],
                    'name_tr': SOURCE_NAMES_TR.get(data['name'], data['name']),
                    'description_en': data.get('source', ''),
                    'default_unit': data['unit'],
                    'icon': '🔥',
                    'created_by': admin_user
                }
            )
            # Create emission factor
            EmissionFactorData.objects.get_or_create(
                source=source,
                country_code='global',
                defaults={
                    'country_name': 'Global',
                    'factor_value': data['factor'],
                    'unit': data['unit'],
                    'reference_source': data.get('source', 'IPCC/Defra'),
                    'is_active': True,
                    'is_default': True,
                    'created_by': admin_user
                }
            )
            if created:
                total_sources += 1
        
        # MOBILE COMBUSTION
        self.stdout.write('📝 Importing Mobile Combustion sources...')
        for key, data in emission_factors.MOBILE_COMBUSTION.items():
            source, created = EmissionSource.objects.get_or_create(
                category=cat_mobile,
                code=key,
                defaults={
                    'name_en': data['name'],
                    'name_tr': SOURCE_NAMES_TR.get(data['name'], data['name']),
                    'description_en': data.get('source', ''),
                    'default_unit': data['unit'],
                    'emission_factor': data['factor'],
                    'icon': '🚗',
                    'created_by': admin_user
                }
            )
            if created:
                total_sources += 1
        
        # FUGITIVE EMISSIONS
        self.stdout.write('📝 Importing Fugitive Emissions sources...')
        for key, data in emission_factors.FUGITIVE_EMISSIONS.items():
            source, created = EmissionSource.objects.get_or_create(
                category=cat_fugitive,
                code=key,
                defaults={
                    'name_en': data['name'],
                    'name_tr': SOURCE_NAMES_TR.get(data['name'], data['name']),
                    'description_en': data.get('source', ''),
                    'default_unit': data['unit'],
                    'emission_factor': data['factor'],
                    'icon': '💨',
                    'created_by': admin_user
                }
            )
            if created:
                total_sources += 1
        
        # ELECTRICITY
        self.stdout.write('📝 Importing Electricity sources...')
        for key, data in emission_factors.ELECTRICITY.items():
            source, created = EmissionSource.objects.get_or_create(
                category=cat_electricity,
                code=key,
                defaults={
                    'name_en': data['name'],
                    'name_tr': SOURCE_NAMES_TR.get(data['name'], data['name']),
                    'default_unit': data['unit'],
                    'emission_factor': data['factor'],
                    'icon': '⚡',
                    'created_by': admin_user
                }
            )
            if created:
                total_sources += 1
        
        # STEAM & HEAT
        self.stdout.write('📝 Importing Steam & Heat sources...')
        for key, data in emission_factors.STEAM_HEAT_COOLING.items():
            source, created = EmissionSource.objects.get_or_create(
                category=cat_steam,
                code=key,
                defaults={
                    'name_en': data['name'],
                    'name_tr': SOURCE_NAMES_TR.get(data['name'], data['name']),
                    'default_unit': data['unit'],
                    'emission_factor': data['factor'],
                    'icon': '♨️',
                    'created_by': admin_user
                }
            )
            if created:
                total_sources += 1
        
        # BUSINESS TRAVEL
        self.stdout.write('📝 Importing Business Travel sources...')
        for key, data in emission_factors.BUSINESS_TRAVEL.items():
            source, created = EmissionSource.objects.get_or_create(
                category=cat_travel,
                code=key,
                defaults={
                    'name_en': data['name'],
                    'name_tr': SOURCE_NAMES_TR.get(data['name'], data['name']),
                    'default_unit': data['unit'],
                    'emission_factor': data['factor'],
                    'icon': '✈️',
                    'created_by': admin_user
                }
            )
            if created:
                total_sources += 1
        
        # EMPLOYEE COMMUTING
        self.stdout.write('📝 Importing Employee Commuting sources...')
        for key, data in emission_factors.EMPLOYEE_COMMUTING.items():
            source, created = EmissionSource.objects.get_or_create(
                category=cat_commuting,
                code=key,
                defaults={
                    'name_en': data['name'],
                    'name_tr': SOURCE_NAMES_TR.get(data['name'], data['name']),
                    'default_unit': data['unit'],
                    'emission_factor': data['factor'],
                    'icon': '🚌',
                    'created_by': admin_user
                }
            )
            if created:
                total_sources += 1
        
        # PURCHASED GOODS
        self.stdout.write('📝 Importing Purchased Goods sources...')
        for key, data in emission_factors.PURCHASED_GOODS_GLOBAL.items():
            source, created = EmissionSource.objects.get_or_create(
                category=cat_purchased_goods,
                code=key,
                defaults={
                    'name_en': data['name'],
                    'name_tr': SOURCE_NAMES_TR.get(data['name'], data['name']),
                    'description_en': data.get('source', ''),
                    'default_unit': data['unit'],
                    'emission_factor': data['factor'],
                    'icon': '📦',
                    'created_by': admin_user
                }
            )
            if created:
                total_sources += 1
        
        # WASTE
        self.stdout.write('📝 Importing Waste sources...')
        for key, data in emission_factors.WASTE.items():
            source, created = EmissionSource.objects.get_or_create(
                category=cat_waste,
                code=key,
                defaults={
                    'name_en': data['name'],
                    'name_tr': SOURCE_NAMES_TR.get(data['name'], data['name']),
                    'default_unit': data['unit'],
                    'emission_factor': data['factor'],
                    'icon': '🗑️',
                    'created_by': admin_user
                }
            )
            if created:
                total_sources += 1
        
        # WATER
        self.stdout.write('📝 Importing Water sources...')
        for key, data in emission_factors.WATER.items():
            source, created = EmissionSource.objects.get_or_create(
                category=cat_water,
                code=key,
                defaults={
                    'name_en': data['name'],
                    'name_tr': SOURCE_NAMES_TR.get(data['name'], data['name']),
                    'description_en': data.get('source', ''),
                    'default_unit': data['unit'],
                    'emission_factor': data['factor'],
                    'icon': '💧',
                    'created_by': admin_user
                }
            )
            if created:
                total_sources += 1
        
        # UPSTREAM TRANSPORTATION
        self.stdout.write('📝 Importing Upstream Transportation sources...')
        for key, data in emission_factors.UPSTREAM_TRANSPORTATION.items():
            source, created = EmissionSource.objects.get_or_create(
                category=cat_upstream_transport,
                code=key,
                defaults={
                    'name_en': data['name'],
                    'name_tr': SOURCE_NAMES_TR.get(data['name'], data['name']),
                    'default_unit': data['unit'],
                    'emission_factor': data['factor'],
                    'icon': '🚚',
                    'created_by': admin_user
                }
            )
            if created:
                total_sources += 1
        
        self.stdout.write('\n' + '='*50)
        self.stdout.write(f'✅ Import completed!')
        self.stdout.write(f'📊 Total sources imported: {total_sources}')
        self.stdout.write('='*50 + '\n')
