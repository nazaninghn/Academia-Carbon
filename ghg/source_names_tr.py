"""
Turkish display names for emission sources.

Display labels only: keys are the English names from emission_factors.py and
nothing here affects factors or calculations.
"""

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
