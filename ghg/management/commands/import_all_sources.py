"""
Import all emission sources from emission_factors.py to database
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from ghg.models_emission_sources import EmissionScope, EmissionCategory, EmissionSource, EmissionFactorData
from ghg import emission_factors


# Turkish names for the sources defined in emission_factors.py (keyed by English name)
SOURCE_NAMES_TR = {
    # Stationary combustion
    'Coal (industrial)': 'Kömür (endüstriyel)',
    'Gas/Diesel Oil (energy basis)': 'Gaz/Dizel Yağı (enerji bazlı)',
    'Liquefied Petroleum Gas (LPG)': 'Sıvılaştırılmış Petrol Gazı (LPG)',
    'Propane (mass)': 'Propan (kütle)',
    'Motor Gasoline': 'Motor Benzini',
    'Natural Gas': 'Doğal Gaz',
    'Diesel (volume)': 'Dizel (hacim)',
    'Coal (generic)': 'Kömür (genel)',
    'Fuel Oil (volume)': 'Fuel Oil (hacim)',
    # Mobile combustion
    'Off-Road (IPCC 2019)': 'Arazi Araçları (IPCC 2019)',
    'On-Road Diesel': 'Karayolu Dizel',
    'On-Road Gasoline (Low Mileage)': 'Karayolu Benzin (Düşük Kilometre)',
    'On-Road Gasoline (Uncontrolled)': 'Karayolu Benzin (Kontrolsüz)',
    'On-Road Gasoline (Oxidation Catalyst)': 'Karayolu Benzin (Oksidasyon Katalizörlü)',
    'On-Road Natural Gas': 'Karayolu Doğal Gaz',
    'On-Road LPG': 'Karayolu LPG',
    'Off-Road Diesel': 'Arazi Araçları Dizel',
    'Off-Road Gasoline': 'Arazi Araçları Benzin',
    'On-Road Petrol (DESNZ 2024)': 'Karayolu Benzin (DESNZ 2024)',
    'On-Road Diesel (DESNZ 2024)': 'Karayolu Dizel (DESNZ 2024)',
    'On-Road LPG (DESNZ 2024)': 'Karayolu LPG (DESNZ 2024)',
    'Gasoline (generic)': 'Benzin (genel)',
    'Diesel (generic)': 'Dizel (genel)',
    'CNG': 'CNG (Sıkıştırılmış Doğal Gaz)',
    'Vehicle distance (avg car)': 'Araç mesafesi (ortalama otomobil)',
    # Fugitive emissions
    'R-600a (Isobutane)': 'R-600a (İzobütan)',
    'Methane (CH4)': 'Metan (CH4)',
    # Electricity
    'Grid average': 'Şebeke ortalaması',
    'US grid': 'ABD şebekesi',
    'EU grid': 'AB şebekesi',
    'China grid': 'Çin şebekesi',
    '100% renewable': '%100 yenilenebilir',
    # Steam, heat & cooling
    'District heating': 'Bölgesel ısıtma',
    'District cooling': 'Bölgesel soğutma',
    'Steam': 'Buhar',
    'Chilled water': 'Soğutulmuş su',
    # Business travel / employee commuting
    'Short-haul flight (<500 km)': 'Kısa mesafeli uçuş (<500 km)',
    'Medium-haul flight (500–3700 km)': 'Orta mesafeli uçuş (500–3700 km)',
    'Long-haul flight (>3700 km)': 'Uzun mesafeli uçuş (>3700 km)',
    'Train': 'Tren',
    'Taxi': 'Taksi',
    'Bus': 'Otobüs',
    'Car': 'Otomobil',
    'Motorcycle': 'Motosiklet',
    'Bicycle': 'Bisiklet',
    # Purchased goods
    'Electrical items – large': 'Elektrikli eşyalar – büyük',
    'Electrical items – small': 'Elektrikli eşyalar – küçük',
    'Electrical items – fridges & freezers': 'Elektrikli eşyalar – buzdolabı ve dondurucular',
    'Electrical items – IT': 'Elektrikli eşyalar – BT',
    'Glass': 'Cam',
    'Metal: aluminium cans & foil (excl. forming)': 'Metal: alüminyum kutu ve folyo (şekillendirme hariç)',
    'Metal: mixed cans': 'Metal: karışık kutular',
    'Metal: steel cans': 'Metal: çelik kutular',
    'Mineral oil': 'Mineral yağ',
    'Paper & board: mixed': 'Kâğıt ve karton: karışık',
    'Plastics: average plastics': 'Plastikler: ortalama plastik',
    'Plastics: HDPE (incl. forming)': 'Plastikler: HDPE (şekillendirme dahil)',
    'Wood': 'Ahşap',
    # Waste
    'General waste (landfill)': 'Genel atık (düzenli depolama)',
    'Recyclable waste': 'Geri dönüştürülebilir atık',
    'Organic compost': 'Organik kompost',
    'Waste incineration': 'Atık yakma',
    # Water
    'Water supply': 'Su temini',
    'Wastewater treatment': 'Atık su arıtma',
    # Upstream transportation
    'Truck freight': 'Kamyon taşımacılığı',
    'Rail freight': 'Demiryolu taşımacılığı',
    'Sea freight': 'Deniz taşımacılığı',
    'Air freight': 'Hava taşımacılığı',
}


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
