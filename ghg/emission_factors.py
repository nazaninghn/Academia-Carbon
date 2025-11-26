"""
Emission Factors based on IPCC, EPA, and DEFRA guidelines
All values in kg CO2e per unit

Turkey-specific factors based on:
- IEA (International Energy Agency) 2023 data
- Turkish Ministry of Environment and Urbanization
- IPCC 2006 Guidelines adapted for Turkey
"""

# ============================================
# TURKEY-SPECIFIC EMISSION FACTORS
# ============================================

# Turkey Scope 2 - Electricity (kg CO2e per kWh)
# Source: IEA 2024 + Turkey Energy Strategy 2025 projections
TURKEY_ELECTRICITY = {
    'turkey-grid': {
        'factor': 0.452,  # kg CO2e per kWh (Turkey national grid 2025 - projected with renewable expansion)
        'unit': 'kwh',
        'name': 'Turkey National Grid',
        'source': 'Turkey Energy Strategy 2025 - Projected mix (coal 32%, natural gas 24%, hydro 24%, renewable 20%)'
    }
}

# Turkey Scope 1 - Stationary Combustion
# Source: Turkish Ministry of Environment, IPCC 2006
TURKEY_STATIONARY = {
    'natural-gas': {
        'factor': 56.211,  # kg CO2e per GJ (CO2: 56.1 + CH4: 0.0837 + N2O: 0.0273)
        'unit': 'gj',
        'name': 'Natural Gas (Turkey)',
        'source': 'IPCC 2019 - Tier 1 factors with AR6 GWP values (CO2: 56.1, CH4: 3.0g×27.9, N2O: 0.1g×273)'
    },
    'diesel': {
        'factor': 2.68,  # kg CO2e per liter (standard)
        'unit': 'liters',
        'name': 'Diesel (Turkey)',
        'source': 'IPCC 2006'
    },
    'coal': {
        'factor': 2.45,  # kg CO2e per kg (Turkish lignite coal)
        'unit': 'kg',
        'name': 'Coal/Lignite (Turkey)',
        'source': 'Turkish lignite has slightly higher emissions'
    },
    'coal-industrial': {
        'factor': 2.40739,  # kg CO2e per kg (2,407.39 kg CO2e per tonne)
        'unit': 'kg',
        'name': 'Coal (industrial) (Turkey)',
        'source': 'Defra 2024 - UK Government GHG Conversion Factors (2,407.39 kg CO2e/tonne or 94.759 kg CO2e/GJ)'
    },
    'gas-diesel-oil-energy': {
        'factor': 74.1,  # kg CO2 per GJ (IPCC Tier 1)
        'unit': 'gj',
        'name': 'Gas/Diesel Oil (Turkey)',
        'source': 'IPCC 2019 - Default CO2 Emission Factor (74.1 kg CO2/GJ)'
    },
    'lpg': {
        'factor': 1.51468,  # kg CO2e per liter
        'unit': 'liters',
        'name': 'LPG (Turkey)',
        'source': 'DESNZ/Defra 2024 - UK Government GHG Conversion Factors'
    },
    'motor-gasoline': {
        'factor': 69.55587,  # kg CO2e per GJ (CO2: 69.3 + CH4: 0.09207 + N2O: 0.1638)
        'unit': 'gj',
        'name': 'Motor Gasoline (Turkey)',
        'source': 'IPCC 2019 - Tier 1 factors with AR6 GWP values (CO2: 69.3, CH4: 3.3g×27.9, N2O: 0.6g×273)'
    },
    'fuel-oil': {
        'factor': 3.18,  # kg CO2e per liter
        'unit': 'liters',
        'name': 'Fuel Oil (Turkey)',
        'source': 'IPCC 2006'
    }
}

# Turkey Scope 3 - Transportation
# Source: Turkish Statistical Institute (TÜİK), DEFRA adapted
TURKEY_TRANSPORTATION = {
    'off-road-ipcc': {
        'factor': 74.39892,  # kg CO2e per GJ (CO2: 74.1 + CH4: 0.18972 + N2O: 0.1092)
        'unit': 'gj',
        'name': 'Off-Road (IPCC 2019) (Turkey)',
        'source': 'IPCC 2019 - Off-road equipment with AR6 GWP (CO2: 74.1, CH4: 6.8g×27.9, N2O: 0.4g×273)'
    },
    'off-road-diesel': {
        'factor': 3.17939,  # kg CO2e per litre
        'unit': 'liters',
        'name': 'Off-Road Diesel (Turkey)',
        'source': 'DESNZ 2024 - UK Government GHG Conversion Factors'
    },
    'off-road-gasoline': {
        'factor': 2.30233,  # kg CO2e per litre
        'unit': 'liters',
        'name': 'Off-Road Gasoline (Turkey)',
        'source': 'DESNZ 2024 - UK Government GHG Conversion Factors'
    },
    'on-road-petrol-desnz': {
        'factor': 2.30233,  # kg CO2e per litre
        'unit': 'liters',
        'name': 'On-Road Petrol (DESNZ 2024) (Turkey)',
        'source': 'DESNZ 2024 - UK Government GHG Conversion Factors'
    },
    'on-road-diesel-desnz': {
        'factor': 3.17939,  # kg CO2e per litre
        'unit': 'liters',
        'name': 'On-Road Diesel (DESNZ 2024) (Turkey)',
        'source': 'DESNZ 2024 - UK Government GHG Conversion Factors'
    },
    'on-road-lpg-desnz': {
        'factor': 63.1,  # kg CO2e per GJ (using IPCC factor)
        'unit': 'gj',
        'name': 'On-Road LPG (DESNZ 2024) (Turkey)',
        'source': 'IPCC 2019 - On-road vehicles (LPG)'
    },
    'on-road-gasoline-low-mileage-desnz': {
        'factor': 69.55587,  # kg CO2e per GJ
        'unit': 'gj',
        'name': 'On-Road Gasoline Low Mileage (DESNZ 2024) (Turkey)',
        'source': 'IPCC 2019 - Light Duty Vehicle Vintage 1995+ with AR6 GWP'
    },
    'on-road-gasoline-uncontrolled-desnz': {
        'factor': 69.55587,  # kg CO2e per GJ
        'unit': 'gj',
        'name': 'On-Road Gasoline Uncontrolled (DESNZ 2024) (Turkey)',
        'source': 'IPCC 2019 - Uncontrolled vehicles with AR6 GWP'
    },
    'on-road-gasoline-oxidation-desnz': {
        'factor': 69.55587,  # kg CO2e per GJ
        'unit': 'gj',
        'name': 'On-Road Gasoline Oxidation Catalyst (DESNZ 2024) (Turkey)',
        'source': 'IPCC 2019 - Vehicles with oxidation catalyst and AR6 GWP'
    },
    'on-road-natural-gas-desnz': {
        'factor': 56.211,  # kg CO2e per GJ
        'unit': 'gj',
        'name': 'On-Road Natural Gas (DESNZ 2024) (Turkey)',
        'source': 'IPCC 2019 - On-road vehicles with AR6 GWP'
    },
    'on-road-lpg': {
        'factor': 63.1,  # kg CO2e per GJ (IPCC default for LPG on-road)
        'unit': 'gj',
        'name': 'On-Road LPG (Turkey)',
        'source': 'IPCC 2019 - On-road vehicles (LPG)'
    },
    'on-road-gasoline-low-mileage': {
        'factor': 69.55587,  # kg CO2e per GJ (CO2: 69.3 + CH4: 0.09207 + N2O: 0.1638)
        'unit': 'gj',
        'name': 'On-Road Gasoline (Low Mileage) (Turkey)',
        'source': 'IPCC 2019 - Light Duty Vehicle Vintage 1995+ with AR6 GWP'
    },
    'on-road-gasoline-uncontrolled': {
        'factor': 69.55587,  # kg CO2e per GJ (same base factor)
        'unit': 'gj',
        'name': 'On-Road Gasoline (Uncontrolled) (Turkey)',
        'source': 'IPCC 2019 - Uncontrolled vehicles with AR6 GWP'
    },
    'on-road-gasoline-oxidation': {
        'factor': 69.55587,  # kg CO2e per GJ (same base factor)
        'unit': 'gj',
        'name': 'On-Road Gasoline (Oxidation Catalyst) (Turkey)',
        'source': 'IPCC 2019 - Vehicles with oxidation catalyst and AR6 GWP'
    },
    'on-road-diesel': {
        'factor': 74.39892,  # kg CO2e per GJ (CO2: 74.1 + CH4: 0.18972 + N2O: 0.1092)
        'unit': 'gj',
        'name': 'On-Road Diesel (Turkey)',
        'source': 'IPCC 2019 - On-road vehicles with AR6 GWP (CO2: 74.1, CH4: 6.8g×27.9, N2O: 0.4g×273)'
    },
    'on-road-natural-gas': {
        'factor': 56.211,  # kg CO2e per GJ (CO2: 56.1 + CH4: 0.0837 + N2O: 0.0273)
        'unit': 'gj',
        'name': 'On-Road Natural Gas (Turkey)',
        'source': 'IPCC 2019 - On-road vehicles with AR6 GWP (CO2: 56.1, CH4: 3.0g×27.9, N2O: 0.1g×273)'
    },
    'flight-domestic': {
        'factor': 0.232,  # kg CO2e per km (Turkish domestic flights - 2025 with Boeing 737 MAX & A320neo)
        'unit': 'km',
        'name': 'Domestic Flight (Turkey)',
        'source': 'Turkish Airlines 2025 - New generation aircraft fleet'
    },
    'flight-international': {
        'factor': 0.148,  # kg CO2e per km (improved efficiency with new aircraft)
        'unit': 'km',
        'name': 'International Flight',
        'source': 'ICAO 2025 standards'
    },
    'train': {
        'factor': 0.035,  # kg CO2e per km (TCDD - Turkish State Railways)
        'unit': 'km',
        'name': 'Train (Turkey)',
        'source': 'TCDD electrified lines'
    },
    'metro': {
        'factor': 0.028,  # kg CO2e per km (Istanbul/Ankara metro)
        'unit': 'km',
        'name': 'Metro (Turkey)',
        'source': 'Turkish metro systems'
    },
    'bus': {
        'factor': 0.095,  # kg CO2e per km (Turkish city buses)
        'unit': 'km',
        'name': 'Bus (Turkey)',
        'source': 'Turkish urban transport'
    },
    'dolmus': {
        'factor': 0.082,  # kg CO2e per km (shared minibus)
        'unit': 'km',
        'name': 'Dolmuş (Turkey)',
        'source': 'Turkish shared transport'
    },
    'car-gasoline': {
        'factor': 0.172,  # kg CO2e per km (Turkish average car - Euro 6d standards 2025)
        'unit': 'km',
        'name': 'Car - Gasoline (Turkey)',
        'source': 'Turkish vehicle fleet average 2025 - Euro 6d compliance'
    },
    'car-diesel': {
        'factor': 0.156,  # kg CO2e per km (improved efficiency with Euro 6d)
        'unit': 'km',
        'name': 'Car - Diesel (Turkey)',
        'source': 'Turkish vehicle fleet average 2025'
    },
    'car-lpg': {
        'factor': 0.163,  # kg CO2e per km (LPG popular in Turkey - 5M+ vehicles in 2025)
        'unit': 'km',
        'name': 'Car - LPG (Turkey)',
        'source': 'Turkish LPG vehicles 2025 - Growing market'
    },
    'car-electric': {
        'factor': 0.045,  # kg CO2e per km (based on Turkey grid 2025 - cleaner grid)
        'unit': 'km',
        'name': 'Car - Electric (Turkey)',
        'source': 'Electric vehicles using Turkey grid 2025 - 20% renewable'
    },
    'car-hybrid': {
        'factor': 0.089,  # kg CO2e per km (hybrid vehicles - improved technology)
        'unit': 'km',
        'name': 'Car - Hybrid (Turkey)',
        'source': 'Hybrid vehicles average 2025'
    }
}

# Turkey Scope 3 - Waste
# Source: Turkish Ministry of Environment, Zero Waste Project
TURKEY_WASTE = {
    'landfill': {
        'factor': 0.54,  # kg CO2e per kg (Turkish landfills - advanced methane capture 2025)
        'unit': 'kg',
        'name': 'Landfill (Turkey)',
        'source': 'Turkish waste management 2025 - Zero Waste target: 40% recycling'
    },
    'recyclable': {
        'factor': 0.017,  # kg CO2e per kg (improved recycling efficiency)
        'unit': 'kg',
        'name': 'Recyclable (Turkey)',
        'source': 'Zero Waste Project 2025 - 40% recycling rate target'
    },
    'organic-compost': {
        'factor': 0.014,  # kg CO2e per kg (improved composting technology)
        'unit': 'kg',
        'name': 'Organic Compost (Turkey)',
        'source': 'Turkish composting facilities 2025 - Expanded capacity'
    },
    'incineration': {
        'factor': 0.82,  # kg CO2e per kg (improved energy recovery efficiency)
        'unit': 'kg',
        'name': 'Incineration (Turkey)',
        'source': 'Turkish waste-to-energy plants 2025 - New facilities'
    }
}

# Turkey Scope 2 - District Heating/Cooling
# Source: Turkish district heating systems (İSKİ, İGDAŞ)
TURKEY_DISTRICT_ENERGY = {
    'district-heating': {
        'factor': 0.232,  # kg CO2e per kWh (natural gas based - 2025 efficiency standards)
        'unit': 'kwh',
        'name': 'District Heating (Turkey)',
        'source': 'Turkish district heating 2025 (natural gas with CHP and efficiency improvements)'
    },
    'district-cooling': {
        'factor': 0.089,  # kg CO2e per kWh (improved efficiency and renewable integration)
        'unit': 'kwh',
        'name': 'District Cooling (Turkey)',
        'source': 'Turkish district cooling systems 2025'
    }
}

# ============================================
# GLOBAL/DEFAULT EMISSION FACTORS
# ============================================

# Scope 1 - Stationary Combustion (kg CO2e per unit)
# Based on IPCC 2006 Guidelines and Defra 2024
STATIONARY_COMBUSTION = {
    'coal-industrial': {
        'factor': 2.40739,  # kg CO2e per kg (2,407.39 kg CO2e per tonne)
        'unit': 'kg',
        'name': 'Coal (industrial)',
        'source': 'Defra 2024 - UK Government GHG Conversion Factors (2,407.39 kg CO2e/tonne or 94.759 kg CO2e/GJ)'
    },
    'gas-diesel-oil-energy': {
        'factor': 74.1,  # kg CO2 per GJ (IPCC Tier 1)
        'unit': 'gj',
        'name': 'Gas/Diesel Oil',
        'source': 'IPCC 2019 - Default CO2 Emission Factor (74.1 kg CO2/GJ)'
    },
    'lpg': {
        'factor': 1.51468,  # kg CO2e per liter
        'unit': 'liters',
        'name': 'Liquefied Petroleum Gases',
        'source': 'DESNZ/Defra 2024 - UK Government GHG Conversion Factors'
    },
    'motor-gasoline': {
        'factor': 69.55587,  # kg CO2e per GJ (CO2: 69.3 + CH4: 0.09207 + N2O: 0.1638)
        'unit': 'gj',
        'name': 'Motor Gasoline',
        'source': 'IPCC 2019 - Tier 1 factors with AR6 GWP values (CO2: 69.3, CH4: 3.3g×27.9, N2O: 0.6g×273)'
    },
    'natural-gas': {
        'factor': 56.211,  # kg CO2e per GJ (CO2: 56.1 + CH4: 0.0837 + N2O: 0.0273)
        'unit': 'gj',
        'name': 'Natural Gas',
        'source': 'IPCC 2019 - Tier 1 factors with AR6 GWP values (CO2: 56.1, CH4: 3.0g×27.9, N2O: 0.1g×273)'
    },
    # Legacy options (kept for backward compatibility)
    'diesel': {
        'factor': 2.68,  # kg CO2e per liter
        'unit': 'liters',
        'name': 'Diesel',
        'source': 'IPCC 2006'
    },
    'coal': {
        'factor': 2.42,  # kg CO2e per kg
        'unit': 'kg',
        'name': 'Coal',
        'source': 'IPCC 2006'
    },
    'fuel-oil': {
        'factor': 3.18,  # kg CO2e per liter
        'unit': 'liters',
        'name': 'Fuel Oil',
        'source': 'IPCC 2006'
    }
}

# Scope 1 - Mobile Combustion (kg CO2e per liter or km)
MOBILE_COMBUSTION = {
    'off-road-ipcc': {
        'factor': 74.39892,  # kg CO2e per GJ (CO2: 74.1 + CH4: 0.18972 + N2O: 0.1092)
        'unit': 'gj',
        'name': 'Off-Road (IPCC 2019)',
        'source': 'IPCC 2019 - Off-road equipment with AR6 GWP (CO2: 74.1, CH4: 6.8g×27.9, N2O: 0.4g×273)'
    },
    'off-road-diesel': {
        'factor': 3.17939,  # kg CO2e per litre
        'unit': 'liters',
        'name': 'Off-Road Diesel',
        'source': 'DESNZ 2024 - UK Government GHG Conversion Factors'
    },
    'off-road-gasoline': {
        'factor': 2.30233,  # kg CO2e per litre
        'unit': 'liters',
        'name': 'Off-Road Gasoline',
        'source': 'DESNZ 2024 - UK Government GHG Conversion Factors'
    },
    'on-road-petrol-desnz': {
        'factor': 2.30233,  # kg CO2e per litre
        'unit': 'liters',
        'name': 'On-Road Petrol (DESNZ 2024)',
        'source': 'DESNZ 2024 - UK Government GHG Conversion Factors'
    },
    'on-road-diesel-desnz': {
        'factor': 3.17939,  # kg CO2e per litre
        'unit': 'liters',
        'name': 'On-Road Diesel (DESNZ 2024)',
        'source': 'DESNZ 2024 - UK Government GHG Conversion Factors'
    },
    'on-road-lpg-desnz': {
        'factor': 63.1,  # kg CO2e per GJ (using IPCC factor)
        'unit': 'gj',
        'name': 'On-Road LPG (DESNZ 2024)',
        'source': 'IPCC 2019 - On-road vehicles (LPG)'
    },
    'on-road-gasoline-low-mileage-desnz': {
        'factor': 69.55587,  # kg CO2e per GJ
        'unit': 'gj',
        'name': 'On-Road Gasoline Low Mileage (DESNZ 2024)',
        'source': 'IPCC 2019 - Light Duty Vehicle Vintage 1995+ with AR6 GWP'
    },
    'on-road-gasoline-uncontrolled-desnz': {
        'factor': 69.55587,  # kg CO2e per GJ
        'unit': 'gj',
        'name': 'On-Road Gasoline Uncontrolled (DESNZ 2024)',
        'source': 'IPCC 2019 - Uncontrolled vehicles with AR6 GWP'
    },
    'on-road-gasoline-oxidation-desnz': {
        'factor': 69.55587,  # kg CO2e per GJ
        'unit': 'gj',
        'name': 'On-Road Gasoline Oxidation Catalyst (DESNZ 2024)',
        'source': 'IPCC 2019 - Vehicles with oxidation catalyst and AR6 GWP'
    },
    'on-road-natural-gas-desnz': {
        'factor': 56.211,  # kg CO2e per GJ
        'unit': 'gj',
        'name': 'On-Road Natural Gas (DESNZ 2024)',
        'source': 'IPCC 2019 - On-road vehicles with AR6 GWP'
    },
    'on-road-lpg': {
        'factor': 63.1,  # kg CO2e per GJ (IPCC default for LPG on-road)
        'unit': 'gj',
        'name': 'On-Road LPG',
        'source': 'IPCC 2019 - On-road vehicles (LPG)'
    },
    'on-road-gasoline-low-mileage': {
        'factor': 69.55587,  # kg CO2e per GJ (CO2: 69.3 + CH4: 0.09207 + N2O: 0.1638)
        'unit': 'gj',
        'name': 'On-Road Gasoline (Low Mileage)',
        'source': 'IPCC 2019 - Light Duty Vehicle Vintage 1995+ with AR6 GWP'
    },
    'on-road-gasoline-uncontrolled': {
        'factor': 69.55587,  # kg CO2e per GJ (same base factor)
        'unit': 'gj',
        'name': 'On-Road Gasoline (Uncontrolled)',
        'source': 'IPCC 2019 - Uncontrolled vehicles with AR6 GWP'
    },
    'on-road-gasoline-oxidation': {
        'factor': 69.55587,  # kg CO2e per GJ (same base factor)
        'unit': 'gj',
        'name': 'On-Road Gasoline (Oxidation Catalyst)',
        'source': 'IPCC 2019 - Vehicles with oxidation catalyst and AR6 GWP'
    },
    'on-road-diesel': {
        'factor': 74.39892,  # kg CO2e per GJ (CO2: 74.1 + CH4: 0.18972 + N2O: 0.1092)
        'unit': 'gj',
        'name': 'On-Road Diesel',
        'source': 'IPCC 2019 - On-road vehicles with AR6 GWP (CO2: 74.1, CH4: 6.8g×27.9, N2O: 0.4g×273)'
    },
    'on-road-natural-gas': {
        'factor': 56.211,  # kg CO2e per GJ (CO2: 56.1 + CH4: 0.0837 + N2O: 0.0273)
        'unit': 'gj',
        'name': 'On-Road Natural Gas',
        'source': 'IPCC 2019 - On-road vehicles with AR6 GWP (CO2: 56.1, CH4: 3.0g×27.9, N2O: 0.1g×273)'
    },
    'gasoline': {
        'factor': 2.31,  # kg CO2e per liter
        'unit': 'liters',
        'name': 'Gasoline'
    },
    'diesel': {
        'factor': 2.68,  # kg CO2e per liter
        'unit': 'liters',
        'name': 'Diesel'
    },
    'cng': {
        'factor': 1.93,  # kg CO2e per kg
        'unit': 'kg',
        'name': 'CNG'
    },
    'vehicle-km': {
        'factor': 0.171,  # kg CO2e per km (average car)
        'unit': 'km',
        'name': 'Vehicle Distance'
    }
}

# Scope 1 - Fugitive Emissions (kg CO2e per kg)
FUGITIVE_EMISSIONS = {
    'r410a': {
        'factor': 2088,  # GWP of R-410A (highest among common refrigerants)
        'unit': 'kg',
        'name': 'R-410A (Refrigerant)',
        'source': 'DESNZ 2024 - UK Government GHG Conversion Factors'
    },
    'r432a': {
        'factor': 1940,  # GWP of R-432A
        'unit': 'kg',
        'name': 'R-432A (Refrigerant)',
        'source': 'DESNZ 2024 - UK Government GHG Conversion Factors'
    },
    'r22': {
        'factor': 1810,  # GWP of R-22 (HCFC-22 / Chlorodifluoromethane)
        'unit': 'kg',
        'name': 'R-22 (HCFC-22 / Chlorodifluoromethane)',
        'source': 'DESNZ 2024 - UK Government GHG Conversion Factors'
    },
    'r600a': {
        'factor': 3.0,  # GWP of R-600A (Isobutane)
        'unit': 'kg',
        'name': 'R-600A (Isobutane)',
        'source': 'DESNZ 2024 - UK Government GHG Conversion Factors'
    },
    'methane': {
        'factor': 27.9,  # GWP of Methane (CH4) - IPCC AR6
        'unit': 'kg',
        'name': 'Methane (CH4)',
        'source': 'DESNZ 2024 / IPCC AR6 GWP'
    }
}

# Scope 2 - Electricity (kg CO2e per kWh) - varies by country/grid
ELECTRICITY = {
    'grid-average': {
        'factor': 0.475,  # kg CO2e per kWh (global average)
        'unit': 'kwh',
        'name': 'Grid Average'
    },
    'us-grid': {
        'factor': 0.417,  # kg CO2e per kWh (US average)
        'unit': 'kwh',
        'name': 'US Grid'
    },
    'eu-grid': {
        'factor': 0.295,  # kg CO2e per kWh (EU average)
        'unit': 'kwh',
        'name': 'EU Grid'
    },
    'china-grid': {
        'factor': 0.581,  # kg CO2e per kWh (China average)
        'unit': 'kwh',
        'name': 'China Grid'
    },
    'renewable': {
        'factor': 0.0,  # kg CO2e per kWh (renewable energy)
        'unit': 'kwh',
        'name': 'Renewable Energy'
    }
}

# Scope 2 - Steam, Heat and Cooling (kg CO2e per unit)
STEAM_HEAT_COOLING = {
    'district-heating': {
        'factor': 0.233,  # kg CO2e per kWh
        'unit': 'kwh',
        'name': 'District Heating'
    },
    'district-cooling': {
        'factor': 0.088,  # kg CO2e per kWh
        'unit': 'kwh',
        'name': 'District Cooling'
    },
    'steam': {
        'factor': 0.195,  # kg CO2e per kWh
        'unit': 'kwh',
        'name': 'Steam'
    },
    'chilled-water': {
        'factor': 0.092,  # kg CO2e per kWh
        'unit': 'kwh',
        'name': 'Chilled Water'
    }
}

# Scope 3 - Business Travel (kg CO2e per km or per trip)
BUSINESS_TRAVEL = {
    'flight-short': {
        'factor': 0.255,  # kg CO2e per km (< 500 km)
        'unit': 'km',
        'name': 'Short-haul Flight'
    },
    'flight-medium': {
        'factor': 0.156,  # kg CO2e per km (500-3700 km)
        'unit': 'km',
        'name': 'Medium-haul Flight'
    },
    'flight-long': {
        'factor': 0.150,  # kg CO2e per km (> 3700 km)
        'unit': 'km',
        'name': 'Long-haul Flight'
    },
    'train': {
        'factor': 0.041,  # kg CO2e per km
        'unit': 'km',
        'name': 'Train'
    },
    'taxi': {
        'factor': 0.171,  # kg CO2e per km
        'unit': 'km',
        'name': 'Taxi'
    },
    'bus': {
        'factor': 0.089,  # kg CO2e per km
        'unit': 'km',
        'name': 'Bus'
    }
}

# Scope 3 - Waste (kg CO2e per kg)
WASTE = {
    'general-landfill': {
        'factor': 0.57,  # kg CO2e per kg
        'unit': 'kg',
        'name': 'General Waste (Landfill)'
    },
    'recyclable': {
        'factor': 0.021,  # kg CO2e per kg
        'unit': 'kg',
        'name': 'Recyclable Waste'
    },
    'organic-compost': {
        'factor': 0.015,  # kg CO2e per kg
        'unit': 'kg',
        'name': 'Organic Waste (Compost)'
    },
    'incineration': {
        'factor': 0.91,  # kg CO2e per kg
        'unit': 'kg',
        'name': 'Waste Incineration'
    }
}

# Scope 3 - Water (kg CO2e per m3)
WATER = {
    'supply': {
        'factor': 0.344,  # kg CO2e per m3
        'unit': 'm3',
        'name': 'Water Supply'
    },
    'treatment': {
        'factor': 0.708,  # kg CO2e per m3
        'unit': 'm3',
        'name': 'Wastewater Treatment'
    }
}

# Scope 3 - Purchased Goods and Services (kg CO2e per unit)
PURCHASED_GOODS = {
    'paper': {
        'factor': 1.32,  # kg CO2e per kg
        'unit': 'kg',
        'name': 'Paper Products'
    },
    'electronics': {
        'factor': 85.0,  # kg CO2e per unit
        'unit': 'units',
        'name': 'Electronics'
    },
    'furniture': {
        'factor': 120.0,  # kg CO2e per unit
        'unit': 'units',
        'name': 'Furniture'
    },
    'office-supplies': {
        'factor': 2.5,  # kg CO2e per kg
        'unit': 'kg',
        'name': 'Office Supplies'
    }
}

# Scope 3 - Capital Goods (kg CO2e per unit)
CAPITAL_GOODS = {
    'machinery': {
        'factor': 5000.0,  # kg CO2e per unit
        'unit': 'units',
        'name': 'Machinery'
    },
    'vehicles': {
        'factor': 6000.0,  # kg CO2e per vehicle
        'unit': 'units',
        'name': 'Vehicles'
    },
    'buildings': {
        'factor': 500.0,  # kg CO2e per m2
        'unit': 'm2',
        'name': 'Buildings/Construction'
    },
    'it-equipment': {
        'factor': 300.0,  # kg CO2e per unit
        'unit': 'units',
        'name': 'IT Equipment'
    }
}

# Scope 3 - Fuel and Energy Related Activities (kg CO2e per unit)
FUEL_ENERGY_RELATED = {
    'upstream-electricity': {
        'factor': 0.095,  # kg CO2e per kWh
        'unit': 'kwh',
        'name': 'Upstream Electricity'
    },
    'transmission-losses': {
        'factor': 0.035,  # kg CO2e per kWh
        'unit': 'kwh',
        'name': 'Transmission & Distribution Losses'
    },
    'fuel-extraction': {
        'factor': 0.52,  # kg CO2e per liter
        'unit': 'liters',
        'name': 'Fuel Extraction & Processing'
    }
}

# Scope 3 - Upstream Transportation (kg CO2e per unit)
UPSTREAM_TRANSPORTATION = {
    'truck-freight': {
        'factor': 0.112,  # kg CO2e per tonne-km
        'unit': 'tonne-km',
        'name': 'Truck Freight'
    },
    'rail-freight': {
        'factor': 0.022,  # kg CO2e per tonne-km
        'unit': 'tonne-km',
        'name': 'Rail Freight'
    },
    'sea-freight': {
        'factor': 0.011,  # kg CO2e per tonne-km
        'unit': 'tonne-km',
        'name': 'Sea Freight'
    },
    'air-freight': {
        'factor': 0.602,  # kg CO2e per tonne-km
        'unit': 'tonne-km',
        'name': 'Air Freight'
    }
}

# Scope 3 - Employee Commuting (kg CO2e per km)
EMPLOYEE_COMMUTING = {
    'car': {
        'factor': 0.171,  # kg CO2e per km
        'unit': 'km',
        'name': 'Car'
    },
    'bus': {
        'factor': 0.089,  # kg CO2e per km
        'unit': 'km',
        'name': 'Bus'
    },
    'train': {
        'factor': 0.041,  # kg CO2e per km
        'unit': 'km',
        'name': 'Train'
    },
    'motorcycle': {
        'factor': 0.113,  # kg CO2e per km
        'unit': 'km',
        'name': 'Motorcycle'
    },
    'bicycle': {
        'factor': 0.0,  # kg CO2e per km
        'unit': 'km',
        'name': 'Bicycle'
    }
}

# Scope 3 - Upstream Leased Assets (kg CO2e per unit)
UPSTREAM_LEASED = {
    'office-space': {
        'factor': 45.0,  # kg CO2e per m2 per year
        'unit': 'm2',
        'name': 'Leased Office Space'
    },
    'warehouse': {
        'factor': 35.0,  # kg CO2e per m2 per year
        'unit': 'm2',
        'name': 'Leased Warehouse'
    },
    'vehicles': {
        'factor': 2500.0,  # kg CO2e per vehicle per year
        'unit': 'units',
        'name': 'Leased Vehicles'
    }
}

# Scope 3 - Downstream Transportation (kg CO2e per unit)
DOWNSTREAM_TRANSPORTATION = {
    'truck-delivery': {
        'factor': 0.112,  # kg CO2e per tonne-km
        'unit': 'tonne-km',
        'name': 'Truck Delivery'
    },
    'courier': {
        'factor': 0.5,  # kg CO2e per package
        'unit': 'packages',
        'name': 'Courier Service'
    },
    'postal': {
        'factor': 0.3,  # kg CO2e per package
        'unit': 'packages',
        'name': 'Postal Service'
    }
}

# Scope 3 - End of Life Treatment (kg CO2e per kg)
END_OF_LIFE = {
    'product-recycling': {
        'factor': 0.021,  # kg CO2e per kg
        'unit': 'kg',
        'name': 'Product Recycling'
    },
    'product-landfill': {
        'factor': 0.57,  # kg CO2e per kg
        'unit': 'kg',
        'name': 'Product to Landfill'
    },
    'product-incineration': {
        'factor': 0.91,  # kg CO2e per kg
        'unit': 'kg',
        'name': 'Product Incineration'
    }
}

# Scope 3 - Franchises (kg CO2e per unit)
FRANCHISES = {
    'franchise-operations': {
        'factor': 15000.0,  # kg CO2e per franchise per year
        'unit': 'franchises',
        'name': 'Franchise Operations'
    }
}

# Scope 3 - Investments (kg CO2e per unit)
INVESTMENTS = {
    'equity-investments': {
        'factor': 0.185,  # kg CO2e per $ invested
        'unit': 'usd',
        'name': 'Equity Investments'
    },
    'debt-investments': {
        'factor': 0.095,  # kg CO2e per $ invested
        'unit': 'usd',
        'name': 'Debt Investments'
    }
}


def calculate_emissions(category, source, activity_data, country='global'):
    """
    Calculate CO2e emissions based on category, source, activity data, and country
    
    Args:
        category: 'stationary', 'mobile', 'fugitive', 'electricity', 'steam-heat', 'travel', 'waste', 'water'
        source: specific emission source (e.g., 'diesel', 'natural-gas')
        activity_data: amount of activity (float)
        country: 'turkey' or 'global' (default: 'global')
    
    Returns:
        dict with emissions in kg CO2e and tons CO2e
    """
    
    # Turkey-specific emission factors
    if country == 'turkey':
        emission_factors = {
            'stationary': TURKEY_STATIONARY,
            'mobile': TURKEY_TRANSPORTATION,
            'fugitive': FUGITIVE_EMISSIONS,  # Same globally
            'electricity': TURKEY_ELECTRICITY,
            'steam-heat': TURKEY_DISTRICT_ENERGY,
            'travel': TURKEY_TRANSPORTATION,
            'waste': TURKEY_WASTE,
            'water': WATER,  # Use global for now
            'purchased-goods': PURCHASED_GOODS,  # Use global
            'capital-goods': CAPITAL_GOODS,  # Use global
            'fuel-energy': FUEL_ENERGY_RELATED,  # Use global
            'upstream-transport': UPSTREAM_TRANSPORTATION,  # Use global
            'commuting': TURKEY_TRANSPORTATION,
            'upstream-leased': UPSTREAM_LEASED,  # Use global
            'downstream-transport': DOWNSTREAM_TRANSPORTATION,  # Use global
            'end-of-life': TURKEY_WASTE,
            'franchises': FRANCHISES,  # Use global
            'investments': INVESTMENTS  # Use global
        }
    else:
        # Global/default emission factors
        emission_factors = {
            'stationary': STATIONARY_COMBUSTION,
            'mobile': MOBILE_COMBUSTION,
            'fugitive': FUGITIVE_EMISSIONS,
            'electricity': ELECTRICITY,
            'steam-heat': STEAM_HEAT_COOLING,
            'travel': BUSINESS_TRAVEL,
            'waste': WASTE,
            'water': WATER,
            'purchased-goods': PURCHASED_GOODS,
            'capital-goods': CAPITAL_GOODS,
            'fuel-energy': FUEL_ENERGY_RELATED,
            'upstream-transport': UPSTREAM_TRANSPORTATION,
            'commuting': EMPLOYEE_COMMUTING,
            'upstream-leased': UPSTREAM_LEASED,
            'downstream-transport': DOWNSTREAM_TRANSPORTATION,
            'end-of-life': END_OF_LIFE,
            'franchises': FRANCHISES,
            'investments': INVESTMENTS
        }
    
    if category not in emission_factors:
        return {'error': 'Invalid category'}
    
    if source not in emission_factors[category]:
        return {'error': f'Invalid source: {source} for category: {category}'}
    
    factor_data = emission_factors[category][source]
    factor = factor_data['factor']
    
    # Calculate emissions in kg CO2e
    emissions_kg = activity_data * factor
    
    # Convert to tons CO2e
    emissions_tons = emissions_kg / 1000
    
    result = {
        'emissions_kg': round(emissions_kg, 2),
        'emissions_tons': round(emissions_tons, 4),
        'factor': factor,
        'unit': factor_data['unit'],
        'source_name': factor_data['name'],
        'activity_data': activity_data,
        'country': country
    }
    
    # Add source reference if available
    if 'source' in factor_data:
        result['reference'] = factor_data['source']
    
    return result


def get_emission_sources(category, country='global'):
    """Get all available emission sources for a category and country"""
    
    if country == 'turkey':
        sources = {
            'stationary': TURKEY_STATIONARY,
            'mobile': TURKEY_TRANSPORTATION,
            'fugitive': FUGITIVE_EMISSIONS,
            'electricity': TURKEY_ELECTRICITY,
            'steam-heat': TURKEY_DISTRICT_ENERGY,
            'travel': TURKEY_TRANSPORTATION,
            'waste': TURKEY_WASTE,
            'water': WATER,
            'purchased-goods': PURCHASED_GOODS,
            'capital-goods': CAPITAL_GOODS,
            'fuel-energy': FUEL_ENERGY_RELATED,
            'upstream-transport': UPSTREAM_TRANSPORTATION,
            'commuting': TURKEY_TRANSPORTATION,
            'upstream-leased': UPSTREAM_LEASED,
            'downstream-transport': DOWNSTREAM_TRANSPORTATION,
            'end-of-life': TURKEY_WASTE,
            'franchises': FRANCHISES,
            'investments': INVESTMENTS
        }
    else:
        sources = {
            'stationary': STATIONARY_COMBUSTION,
            'mobile': MOBILE_COMBUSTION,
            'fugitive': FUGITIVE_EMISSIONS,
            'electricity': ELECTRICITY,
            'steam-heat': STEAM_HEAT_COOLING,
            'travel': BUSINESS_TRAVEL,
            'waste': WASTE,
            'water': WATER,
            'purchased-goods': PURCHASED_GOODS,
            'capital-goods': CAPITAL_GOODS,
            'fuel-energy': FUEL_ENERGY_RELATED,
            'upstream-transport': UPSTREAM_TRANSPORTATION,
            'commuting': EMPLOYEE_COMMUTING,
            'upstream-leased': UPSTREAM_LEASED,
            'downstream-transport': DOWNSTREAM_TRANSPORTATION,
            'end-of-life': END_OF_LIFE,
            'franchises': FRANCHISES,
            'investments': INVESTMENTS
        }
    
    if category in sources:
        return sources[category]
    return {}


def get_available_countries():
    """Get list of available countries with specific emission factors"""
    return {
        'global': 'Global Average',
        'turkey': 'Turkey (Türkiye)'
    }
