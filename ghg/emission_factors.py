# -*- coding: utf-8 -*-
"""
GHG Emission Factors & Calculator

- Turkey: Based on ISO 14064-1 ATOM KABLO 2023 files + National inventory
- Global/UK: Based on Defra 2024 condensed set + IPCC 2006/2019 + AR6 GWP

All factors are in kg CO2e per unit.
"""

from typing import Dict, Any


# ============================================
# 1) SCOPE 1 – STATIONARY COMBUSTION
# ============================================

# Global / default stationary combustion (IPCC + Defra)
STATIONARY_COMBUSTION: Dict[str, Dict[str, Any]] = {
    # Coal (industrial), unit = kg
    "coal-industrial": {
        "factor": 2.40739,  # kg CO2e per kg (2407.39 kg/t)
        "unit": "kg",
        "name": "Coal (industrial)",
        "source": "Defra 2024 – UK GHG Conversion Factors (2,407.39 kg CO2e/tonne)"
    },

    # Gas/Diesel oil on energy basis (boiler etc.)
    "gas-diesel-oil-energy": {
        "factor": 74.1,  # kg CO2e per GJ
        "unit": "gj",
        "name": "Gas/Diesel Oil (energy basis)",
        "source": "IPCC 2019 – default CO2 emission factor (74.1 kg CO2/GJ)"
    },

    # LPG (generic) – volume based
    "lpg": {
        "factor": 1.51468,  # kg CO2e per liter
        "unit": "liters",
        "name": "Liquefied Petroleum Gas (LPG)",
        "source": "DESNZ/Defra 2024 – UK GHG Conversion Factors"
    },

    # Propane – mass based (from Defra fuels sheet)
    "propane": {
        "factor": 2.99763233,  # kg CO2e per kg (2997.63233 kg/tonne)
        "unit": "kg",
        "name": "Propane (mass)",
        "source": "Defra 2024 – Fuels, Propane (tonnes)"
    },

    # Motor gasoline – energy basis (IPCC)
    "motor-gasoline": {
        "factor": 69.55587,  # kg CO2e per GJ
        "unit": "gj",
        "name": "Motor Gasoline",
        "source": "IPCC 2019 – Tier 1 + AR6 GWP (CO2+CH4+N2O)"
    },

    # Natural gas – energy basis (IPCC)
    "natural-gas": {
        "factor": 56.211,  # kg CO2e per GJ
        "unit": "gj",
        "name": "Natural Gas",
        "source": "IPCC 2019 – Tier 1 + AR6 GWP"
    },

    # Legacy / direct volumetric fuels
    "diesel": {
        "factor": 2.68,  # kg CO2e per liter
        "unit": "liters",
        "name": "Diesel (volume)",
        "source": "IPCC 2006"
    },
    "coal": {
        "factor": 2.42,  # kg CO2e per kg
        "unit": "kg",
        "name": "Coal (generic)",
        "source": "IPCC 2006"
    },
    "fuel-oil": {
        "factor": 3.18,  # kg CO2e per liter
        "unit": "liters",
        "name": "Fuel Oil (volume)",
        "source": "IPCC 2006"
    },
}


# Turkey-specific stationary combustion (from ATOM KABLO + IPCC)
TURKEY_STATIONARY: Dict[str, Dict[str, Any]] = {
    "natural-gas": {
        "factor": 56.211,  # kg CO2e per GJ
        "unit": "gj",
        "name": "Natural Gas (Turkey)",
        "source": "IPCC 2019 – Tier 1 + AR6 GWP"
    },
    "diesel": {
        "factor": 2.68,  # kg CO2e per liter
        "unit": "liters",
        "name": "Diesel (Turkey)",
        "source": "IPCC 2006"
    },
    "coal": {
        "factor": 2.45,  # kg CO2e per kg
        "unit": "kg",
        "name": "Coal/Lignite (Turkey)",
        "source": "Turkish lignite – higher EF"
    },
    "coal-industrial": {
        "factor": 2.40739,  # kg CO2e per kg
        "unit": "kg",
        "name": "Coal (industrial) (Turkey)",
        "source": "Defra 2024 – industrial coal factor"
    },
    "gas-diesel-oil-energy": {
        "factor": 74.1,
        "unit": "gj",
        "name": "Gas/Diesel Oil (Turkey – energy basis)",
        "source": "IPCC 2019 – default CO2 emission factor"
    },
    "lpg": {
        "factor": 1.51468,
        "unit": "liters",
        "name": "LPG (Turkey)",
        "source": "DESNZ/Defra 2024"
    },
    "motor-gasoline": {
        "factor": 69.55587,
        "unit": "gj",
        "name": "Motor Gasoline (Turkey)",
        "source": "IPCC 2019 – with AR6 GWP"
    },
    "fuel-oil": {
        "factor": 3.18,
        "unit": "liters",
        "name": "Fuel Oil (Turkey)",
        "source": "IPCC 2006"
    },
    "propane": {
        "factor": 2.99763233,
        "unit": "kg",
        "name": "Propane (Turkey)",
        "source": "Defra 2024 – Fuels, Propane (tonnes)"
    }
}


# ============================================
# 2) SCOPE 1 – MOBILE COMBUSTION
# ============================================

MOBILE_COMBUSTION: Dict[str, Dict[str, Any]] = {
    # IPCC GJ-based
    "off-road-ipcc": {
        "factor": 74.39892,  # kg CO2e per GJ
        "unit": "gj",
        "name": "Off-Road (IPCC 2019)",
        "source": "IPCC 2019 – Off-road equipment, AR6 GWP"
    },
    "on-road-diesel": {
        "factor": 74.39892,
        "unit": "gj",
        "name": "On-Road Diesel",
        "source": "IPCC 2019 – LDV/HDV diesel, AR6 GWP"
    },
    "on-road-gasoline-low-mileage": {
        "factor": 69.55587,
        "unit": "gj",
        "name": "On-Road Gasoline (Low Mileage)",
        "source": "IPCC 2019 – Light duty, AR6 GWP"
    },
    "on-road-gasoline-uncontrolled": {
        "factor": 69.55587,
        "unit": "gj",
        "name": "On-Road Gasoline (Uncontrolled)",
        "source": "IPCC 2019 – Uncontrolled vehicles"
    },
    "on-road-gasoline-oxidation": {
        "factor": 69.55587,
        "unit": "gj",
        "name": "On-Road Gasoline (Oxidation Catalyst)",
        "source": "IPCC 2019 – with oxidation catalyst"
    },
    "on-road-natural-gas": {
        "factor": 56.211,
        "unit": "gj",
        "name": "On-Road Natural Gas",
        "source": "IPCC 2019 – AR6 GWP"
    },
    "on-road-lpg": {
        "factor": 63.1,
        "unit": "gj",
        "name": "On-Road LPG",
        "source": "IPCC 2019 – LPG vehicles"
    },

    # Defra 2024 – litre-based (DESNZ)
    "off-road-diesel": {
        "factor": 3.17939,
        "unit": "liters",
        "name": "Off-Road Diesel",
        "source": "DESNZ/Defra 2024"
    },
    "off-road-gasoline": {
        "factor": 2.30233,
        "unit": "liters",
        "name": "Off-Road Gasoline",
        "source": "DESNZ/Defra 2024"
    },
    "on-road-petrol-desnz": {
        "factor": 2.30233,
        "unit": "liters",
        "name": "On-Road Petrol (DESNZ 2024)",
        "source": "DESNZ/Defra 2024"
    },
    "on-road-diesel-desnz": {
        "factor": 3.17939,
        "unit": "liters",
        "name": "On-Road Diesel (DESNZ 2024)",
        "source": "DESNZ/Defra 2024"
    },
    "on-road-lpg-desnz": {
        "factor": 63.1,
        "unit": "gj",
        "name": "On-Road LPG (DESNZ 2024)",
        "source": "IPCC 2019 – LPG EF"
    },

    # Simple generic
    "gasoline": {
        "factor": 2.31,
        "unit": "liters",
        "name": "Gasoline (generic)"
    },
    "diesel": {
        "factor": 2.68,
        "unit": "liters",
        "name": "Diesel (generic)"
    },
    "cng": {
        "factor": 1.93,
        "unit": "kg",
        "name": "CNG"
    },
    "vehicle-km": {
        "factor": 0.171,
        "unit": "km",
        "name": "Vehicle distance (avg car)"
    }
}

# Turkey Transportation – same structure but Turkey-specific where needed
TURKEY_TRANSPORTATION: Dict[str, Dict[str, Any]] = {
    # Copy of IPCC-based mobile
    **{k: v for k, v in MOBILE_COMBUSTION.items() if k.startswith("off-road") or k.startswith("on-road")},

    # Country-specific per-km factors (from your spec)
    "flight-domestic": {
        "factor": 0.232,
        "unit": "km",
        "name": "Domestic Flight (Turkey)",
        "source": "Turkish Airlines 2025 – new fleet"
    },
    "flight-international": {
        "factor": 0.148,
        "unit": "km",
        "name": "International Flight",
        "source": "ICAO 2025"
    },
    "train": {
        "factor": 0.035,
        "unit": "km",
        "name": "Train (Turkey)",
        "source": "TCDD – electrified lines"
    },
    "metro": {
        "factor": 0.028,
        "unit": "km",
        "name": "Metro (Turkey)",
        "source": "Istanbul/Ankara metro"
    },
    "bus": {
        "factor": 0.095,
        "unit": "km",
        "name": "Bus (Turkey)",
        "source": "Urban buses"
    },
    "dolmus": {
        "factor": 0.082,
        "unit": "km",
        "name": "Dolmuş (shared minibus)",
        "source": "Shared urban transport"
    },
    "car-gasoline": {
        "factor": 0.172,
        "unit": "km",
        "name": "Car – Gasoline (Turkey)",
        "source": "Turkey fleet 2025 – Euro 6d"
    },
    "car-diesel": {
        "factor": 0.156,
        "unit": "km",
        "name": "Car – Diesel (Turkey)",
        "source": "Turkey fleet 2025"
    },
    "car-lpg": {
        "factor": 0.163,
        "unit": "km",
        "name": "Car – LPG (Turkey)",
        "source": "Turkey LPG vehicles 2025"
    },
    "car-electric": {
        "factor": 0.045,
        "unit": "km",
        "name": "Car – Electric (Turkey)",
        "source": "EVs on Turkey grid 2025"
    },
    "car-hybrid": {
        "factor": 0.089,
        "unit": "km",
        "name": "Car – Hybrid (Turkey)",
        "source": "Hybrid vehicles 2025"
    }
}


# ============================================
# 3) SCOPE 1 – FUGITIVE EMISSIONS (REFRIGERANTS, CH4)
# ============================================

FUGITIVE_EMISSIONS: Dict[str, Dict[str, Any]] = {
    "r410a": {
        "factor": 2088,
        "unit": "kg",
        "name": "R-410A",
        "source": "Defra 2024 – Refrigerant & other"
    },
    "r432a": {
        "factor": 1940,
        "unit": "kg",
        "name": "R-432A",
        "source": "Defra 2024 – Refrigerant & other"
    },
    "r22": {
        "factor": 1810,
        "unit": "kg",
        "name": "HCFC-22 / R-22",
        "source": "Defra 2024 – Refrigerant & other"
    },
    "hfc-227ea": {
        "factor": 3350,
        "unit": "kg",
        "name": "HFC-227ea",
        "source": "Defra 2024 – Refrigerant & other (GWP 3350)"
    },
    "r600a": {
        "factor": 3.0,
        "unit": "kg",
        "name": "R-600a (Isobutane)",
        "source": "Defra 2024 – low-GWP"
    },
    "methane": {
        "factor": 27.9,
        "unit": "kg",
        "name": "Methane (CH4)",
        "source": "IPCC AR6 GWP100"
    }
}


# ============================================
# 4) SCOPE 2 – ELECTRICITY & HEAT/STEAM
# ============================================

# Global / generic grid factors
ELECTRICITY: Dict[str, Dict[str, Any]] = {
    "grid-average": {"factor": 0.475, "unit": "kwh", "name": "Grid average"},
    "us-grid": {"factor": 0.417, "unit": "kwh", "name": "US grid"},
    "eu-grid": {"factor": 0.295, "unit": "kwh", "name": "EU grid"},
    "china-grid": {"factor": 0.581, "unit": "kwh", "name": "China grid"},
    "renewable": {"factor": 0.0, "unit": "kwh", "name": "100% renewable"}
}

# Turkey electricity
TURKEY_ELECTRICITY: Dict[str, Dict[str, Any]] = {
    "turkey-grid": {
        "factor": 0.452,
        "unit": "kwh",
        "name": "Turkey national grid",
        "source": "Turkey Energy Strategy 2025 – projected mix"
    }
}

# Steam, heat & cooling (global/Defra-style)
STEAM_HEAT_COOLING: Dict[str, Dict[str, Any]] = {
    "district-heating": {"factor": 0.233, "unit": "kwh", "name": "District heating"},
    "district-cooling": {"factor": 0.088, "unit": "kwh", "name": "District cooling"},
    "steam": {"factor": 0.195, "unit": "kwh", "name": "Steam"},
    "chilled-water": {"factor": 0.092, "unit": "kwh", "name": "Chilled water"}
}

# Turkey district energy
TURKEY_DISTRICT_ENERGY: Dict[str, Dict[str, Any]] = {
    "district-heating": {
        "factor": 0.232,
        "unit": "kwh",
        "name": "District Heating (Turkey)",
        "source": "Turkey district heating 2025"
    },
    "district-cooling": {
        "factor": 0.089,
        "unit": "kwh",
        "name": "District Cooling (Turkey)",
        "source": "Turkey district cooling 2025"
    }
}


# ============================================
# 5) SCOPE 3 – WATER (Defra 2024)
# ============================================

# From Defra 2024 – Water supply & Water treatment sheets
WATER: Dict[str, Dict[str, Any]] = {
    "supply": {
        "factor": 0.15311,  # kg CO2e per m3
        "unit": "m3",
        "name": "Water supply",
        "source": "Defra 2024 – Water supply (cubic metres)"
    },
    "treatment": {
        "factor": 0.18574,  # kg CO2e per m3
        "unit": "m3",
        "name": "Wastewater treatment",
        "source": "Defra 2024 – Water treatment (cubic metres)"
    }
}


# ============================================
# 6) SCOPE 3 – PURCHASED GOODS & SERVICES
# ============================================

# Global/Defra 2024 – material use (per kg)
PURCHASED_GOODS_GLOBAL: Dict[str, Dict[str, Any]] = {
    "electrical-large": {
        "factor": 3.267,  # 3267 kg/t
        "unit": "kg",
        "name": "Electrical items – large",
        "source": "Defra 2024 – Material use (tonnes)"
    },
    "electrical-small": {
        "factor": 5.64794563,  # 5647.94563 kg/t
        "unit": "kg",
        "name": "Electrical items – small",
        "source": "Defra 2024 – Material use"
    },
    "electrical-fridges-freezers": {
        "factor": 4.36333333,  # 4363.33333 kg/t
        "unit": "kg",
        "name": "Electrical items – fridges & freezers",
        "source": "Defra 2024 – Material use"
    },
    "electrical-it": {
        "factor": 24.86547556,  # 24865.47556 kg/t
        "unit": "kg",
        "name": "Electrical items – IT",
        "source": "Defra 2024 – Material use"
    },
    "glass": {
        "factor": 1.40276667,  # 1402.76667 kg/t
        "unit": "kg",
        "name": "Glass",
        "source": "Defra 2024 – Material use"
    },
    "metal-aluminium-cans-foil": {
        "factor": 9.10691851,  # 9106.91851 kg/t
        "unit": "kg",
        "name": "Metal: aluminium cans & foil (excl. forming)",
        "source": "Defra 2024 – Material use"
    },
    "metal-mixed-cans": {
        "factor": 5.10563851,  # 5105.63851 kg/t
        "unit": "kg",
        "name": "Metal: mixed cans",
        "source": "Defra 2024 – Material use"
    },
    "metal-steel-cans": {
        "factor": 2.85491851,  # 2854.91851 kg/t
        "unit": "kg",
        "name": "Metal: steel cans",
        "source": "Defra 2024 – Material use"
    },
    "mineral-oil": {
        "factor": 1.401,  # 1401 kg/t
        "unit": "kg",
        "name": "Mineral oil",
        "source": "Defra 2024 – Material use"
    },
    "paper-mixed": {
        "factor": 1.28274402,  # 1282.74402 kg/t
        "unit": "kg",
        "name": "Paper & board: mixed",
        "source": "Defra 2024 – Material use"
    },
    "plastic-average": {
        "factor": 3.16478049,  # 3164.78049 kg/t
        "unit": "kg",
        "name": "Plastics: average plastics",
        "source": "Defra 2024 – Material use"
    },
    "plastic-hdpe": {
        "factor": 3.08639038,  # 3086.39038 kg/t
        "unit": "kg",
        "name": "Plastics: HDPE (incl. forming)",
        "source": "Defra 2024 – Material use"
    },
    "wood": {
        "factor": 0.26950416,  # 269.50416 kg/t
        "unit": "kg",
        "name": "Wood",
        "source": "Defra 2024 – Material use"
    },
    # You can also reuse WATER["supply"] here if you treat water as purchased good
}

# Turkey-specific purchased goods – FROM YOUR ISO SHEET "4.1 RAW MATERIALS"
PURCHASED_GOODS_TURKEY: Dict[str, Dict[str, Any]] = {
    # Chemical
    "chemical": {
        "factor": 2.04,  # kg CO2e per kg (from ISO sheet – EF column)
        "unit": "kg",
        "name": "Chemical (Turkey)",
        "source": "ATOM KABLO ISO 14064-1 – 4.1 RAW MATERIALS"
    },
    # Chemical oil
    "chemical-oil": {
        "factor": 2.04,
        "unit": "kg",
        "name": "Chemical oil (Turkey)",
        "source": "ATOM KABLO ISO 14064-1 – 4.1 RAW MATERIALS"
    },
    # Plastic
    "plastic": {
        "factor": 3.102448505,  # 3102.448505 kg/t
        "unit": "kg",
        "name": "Plastic (Turkey project-specific)",
        "source": "ATOM KABLO ISO 14064-1 – E6 = 3102.448505 kg/t"
    },
    # Carton
    "carton": {
        "factor": 0.868069945,  # 868.069945 kg/t
        "unit": "kg",
        "name": "Carton (Turkey)",
        "source": "ATOM KABLO ISO 14064-1 – EF = 868.069945 kg/t"
    },
    # Metal (primary)
    "metal-primary": {
        "factor": 4.005137775,  # 4005.137775 kg/t
        "unit": "kg",
        "name": "Metal (primary) (Turkey)",
        "source": "ATOM KABLO ISO 14064-1 – EF = 4005.137775 kg/t"
    },
    # Metal (recycled)
    "metal-recycled": {
        "factor": 1.55894894,  # 1558.94894 kg/t
        "unit": "kg",
        "name": "Metal (recycled) (Turkey)",
        "source": "ATOM KABLO ISO 14064-1 – EF = 1558.94894 kg/t"
    },
    # Wood
    "wood": {
        "factor": 0.31261178,  # 312.61178 kg/t
        "unit": "kg",
        "name": "Wood (Turkey)",
        "source": "ATOM KABLO ISO 14064-1 – EF = 312.61178 kg/t"
    },
    # Foam tape
    "foam-tape": {
        "factor": 2.586727309,  # 2586.727309 kg/t
        "unit": "kg",
        "name": "Foam tape (Turkey)",
        "source": "ATOM KABLO ISO 14064-1 – EF = 2586.727309 kg/t"
    }
}


# ============================================
# 7) OTHER SCOPE 3 CATEGORIES (simplified)
# ============================================

# Capital goods (simple generic factors)
CAPITAL_GOODS: Dict[str, Dict[str, Any]] = {
    "machinery": {"factor": 5000.0, "unit": "units", "name": "Machinery"},
    "vehicles": {"factor": 6000.0, "unit": "units", "name": "Vehicles"},
    "buildings": {"factor": 500.0, "unit": "m2", "name": "Buildings/construction"},
    "it-equipment": {"factor": 300.0, "unit": "units", "name": "IT equipment"},
}

FUEL_ENERGY_RELATED: Dict[str, Dict[str, Any]] = {
    "upstream-electricity": {"factor": 0.095, "unit": "kwh", "name": "Upstream electricity"},
    "transmission-losses": {"factor": 0.035, "unit": "kwh", "name": "T&D losses"},
    "fuel-extraction": {"factor": 0.52, "unit": "liters", "name": "Fuel extraction & processing"},
}

UPSTREAM_TRANSPORTATION: Dict[str, Dict[str, Any]] = {
    "truck-freight": {"factor": 0.112, "unit": "tonne-km", "name": "Truck freight"},
    "rail-freight": {"factor": 0.022, "unit": "tonne-km", "name": "Rail freight"},
    "sea-freight": {"factor": 0.011, "unit": "tonne-km", "name": "Sea freight"},
    "air-freight": {"factor": 0.602, "unit": "tonne-km", "name": "Air freight"},
}

# Business travel (generic, per km)
BUSINESS_TRAVEL: Dict[str, Dict[str, Any]] = {
    "flight-short": {"factor": 0.255, "unit": "km", "name": "Short-haul flight (<500 km)"},
    "flight-medium": {"factor": 0.156, "unit": "km", "name": "Medium-haul flight (500–3700 km)"},
    "flight-long": {"factor": 0.150, "unit": "km", "name": "Long-haul flight (>3700 km)"},
    "train": {"factor": 0.041, "unit": "km", "name": "Train"},
    "taxi": {"factor": 0.171, "unit": "km", "name": "Taxi"},
    "bus": {"factor": 0.089, "unit": "km", "name": "Bus"},
}

# Employee commuting (generic)
EMPLOYEE_COMMUTING: Dict[str, Dict[str, Any]] = {
    "car": {"factor": 0.171, "unit": "km", "name": "Car"},
    "bus": {"factor": 0.089, "unit": "km", "name": "Bus"},
    "train": {"factor": 0.041, "unit": "km", "name": "Train"},
    "motorcycle": {"factor": 0.113, "unit": "km", "name": "Motorcycle"},
    "bicycle": {"factor": 0.0, "unit": "km", "name": "Bicycle"},
}

# Simple waste (global generic – can be made more precise with Defra Waste disposal if needed)
WASTE: Dict[str, Dict[str, Any]] = {
    "general-landfill": {"factor": 0.57, "unit": "kg", "name": "General waste (landfill)"},
    "recyclable": {"factor": 0.021, "unit": "kg", "name": "Recyclable waste"},
    "organic-compost": {"factor": 0.015, "unit": "kg", "name": "Organic compost"},
    "incineration": {"factor": 0.91, "unit": "kg", "name": "Waste incineration"},
}

# Turkey waste (from your Turkey-specific block)
TURKEY_WASTE: Dict[str, Dict[str, Any]] = {
    "landfill": {"factor": 0.54, "unit": "kg", "name": "Landfill (Turkey)"},
    "recyclable": {"factor": 0.017, "unit": "kg", "name": "Recyclable (Turkey)"},
    "organic-compost": {"factor": 0.014, "unit": "kg", "name": "Organic compost (Turkey)"},
    "incineration": {"factor": 0.82, "unit": "kg", "name": "Incineration (Turkey)"},
}

# End of life – simple
END_OF_LIFE: Dict[str, Dict[str, Any]] = {
    "product-recycling": {"factor": 0.021, "unit": "kg", "name": "Product recycling"},
    "product-landfill": {"factor": 0.57, "unit": "kg", "name": "Product landfill"},
    "product-incineration": {"factor": 0.91, "unit": "kg", "name": "Product incineration"},
}

FRANCHISES: Dict[str, Dict[str, Any]] = {
    "franchise-operations": {
        "factor": 15000.0,
        "unit": "franchises",
        "name": "Franchise operations (per franchise/year)",
    }
}

INVESTMENTS: Dict[str, Dict[str, Any]] = {
    "equity-investments": {"factor": 0.185, "unit": "usd", "name": "Equity investments"},
    "debt-investments": {"factor": 0.095, "unit": "usd", "name": "Debt investments"},
}

UPSTREAM_LEASED: Dict[str, Dict[str, Any]] = {
    "office-space": {"factor": 45.0, "unit": "m2", "name": "Leased office space (per year)"},
    "warehouse": {"factor": 35.0, "unit": "m2", "name": "Leased warehouse (per year)"},
    "vehicles": {"factor": 2500.0, "unit": "units", "name": "Leased vehicles (per year)"},
}

DOWNSTREAM_TRANSPORTATION: Dict[str, Dict[str, Any]] = {
    "truck-delivery": {"factor": 0.112, "unit": "tonne-km", "name": "Truck delivery"},
    "courier": {"factor": 0.5, "unit": "packages", "name": "Courier service"},
    "postal": {"factor": 0.3, "unit": "packages", "name": "Postal service"},
}


# ============================================
# 8) EMISSION FACTOR REGISTRY BY COUNTRY
# ============================================

def _build_emission_factor_registry(country: str) -> Dict[str, Dict[str, Dict[str, Any]]]:
    """
    Internal helper: Returns categorized emission factors dictionary based on country.
    """
    if country.lower() == "turkey":
        return {
            "stationary": TURKEY_STATIONARY,
            "mobile": TURKEY_TRANSPORTATION,
            "fugitive": FUGITIVE_EMISSIONS,
            "electricity": TURKEY_ELECTRICITY,
            "steam-heat": TURKEY_DISTRICT_ENERGY,
            "travel": TURKEY_TRANSPORTATION,
            "waste": TURKEY_WASTE,
            "water": WATER,                 # از Defra 2024
            "purchased-goods": PURCHASED_GOODS_TURKEY,
            "capital-goods": CAPITAL_GOODS,
            "fuel-energy": FUEL_ENERGY_RELATED,
            "upstream-transport": UPSTREAM_TRANSPORTATION,
            "commuting": TURKEY_TRANSPORTATION,
            "upstream-leased": UPSTREAM_LEASED,
            "downstream-transport": DOWNSTREAM_TRANSPORTATION,
            "end-of-life": TURKEY_WASTE,   # can be separated if needed
            "franchises": FRANCHISES,
            "investments": INVESTMENTS,
        }
    else:
        # Global / default
        return {
            "stationary": STATIONARY_COMBUSTION,
            "mobile": MOBILE_COMBUSTION,
            "fugitive": FUGITIVE_EMISSIONS,
            "electricity": ELECTRICITY,
            "steam-heat": STEAM_HEAT_COOLING,
            "travel": BUSINESS_TRAVEL,
            "waste": WASTE,
            "water": WATER,
            "purchased-goods": PURCHASED_GOODS_GLOBAL,
            "capital-goods": CAPITAL_GOODS,
            "fuel-energy": FUEL_ENERGY_RELATED,
            "upstream-transport": UPSTREAM_TRANSPORTATION,
            "commuting": EMPLOYEE_COMMUTING,
            "upstream-leased": UPSTREAM_LEASED,
            "downstream-transport": DOWNSTREAM_TRANSPORTATION,
            "end-of-life": END_OF_LIFE,
            "franchises": FRANCHISES,
            "investments": INVESTMENTS,
        }


# ============================================
# 9) PUBLIC API FUNCTIONS
# ============================================

def calculate_emissions(
    category: str,
    source: str,
    activity_data: float,
    country: str = "global"
) -> Dict[str, Any]:
    """
    Calculate CO2e emissions based on category, source, activity data, and country.

    Args:
        category: One of:
            'stationary', 'mobile', 'fugitive', 'electricity', 'steam-heat',
            'travel', 'waste', 'water', 'purchased-goods', 'capital-goods',
            'fuel-energy', 'upstream-transport', 'commuting',
            'upstream-leased', 'downstream-transport', 'end-of-life',
            'franchises', 'investments'
        source: Source key, such as:
            'coal-industrial', 'natural-gas', 'lpg', 'propane',
            'plastic', 'carton', 'metal-primary', ...
        activity_data: Activity amount (in the unit defined in the factor)
        country: 'global' or 'turkey'

    Returns:
        dict containing:
            - emissions_kg
            - emissions_tons
            - factor
            - unit
            - source_name
            - activity_data
            - country
            - reference (if available)
    """
    registry = _build_emission_factor_registry(country)
    cat = category.lower()

    if cat not in registry:
        return {"error": f"Invalid category: {category}"}

    factors_for_cat = registry[cat]
    if source not in factors_for_cat:
        return {"error": f"Invalid source '{source}' for category '{category}' in country '{country}'"}

    factor_data = factors_for_cat[source]
    factor = factor_data["factor"]

    emissions_kg = activity_data * factor
    emissions_tons = emissions_kg / 1000.0

    result: Dict[str, Any] = {
        "emissions_kg": round(emissions_kg, 4),
        "emissions_tons": round(emissions_tons, 6),
        "factor": factor,
        "unit": factor_data["unit"],
        "source_name": factor_data.get("name", source),
        "activity_data": activity_data,
        "country": country.lower(),
        "category": cat,
        "source_key": source,
    }

    if "source" in factor_data:
        result["reference"] = factor_data["source"]

    return result


def get_emission_sources(category: str, country: str = "global") -> Dict[str, Dict[str, Any]]:
    """
    Returns list of all available sources for a category and country.
    """
    registry = _build_emission_factor_registry(country)
    cat = category.lower()
    return registry.get(cat, {})


def get_available_countries() -> Dict[str, str]:
    """
    Returns list of countries with specific emission factors.
    """
    return {
        "global": "Global average / Defra 2024 + IPCC",
        "turkey": "Turkey (Türkiye) – ATOM KABLO / national mix",
    }
