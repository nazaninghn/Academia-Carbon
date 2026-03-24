# Emission Sources Summary

## Before vs After

### BEFORE (Database Only)
- Total Sources: **5 sources** ❌
- Limited to what was manually entered in database
- Missing most emission factors from `emission_factors.py`

### AFTER (Reading from emission_factors.py)
- Total Sources: **80 sources** ✅
- All sources from `emission_factors.py` are now accessible
- Complete coverage of all emission categories

---

## Detailed Breakdown by Scope

### Scope 1: Direct Emissions (31 sources)

#### Stationary Combustion (9 sources)
- Coal (industrial)
- Gas/Diesel Oil (energy basis)
- Liquefied Petroleum Gas (LPG)
- Propane (mass)
- Motor Gasoline
- Natural Gas
- Diesel (volume)
- Coal (generic)
- Fuel Oil (volume)

#### Mobile Combustion (16 sources)
- Off-Road (IPCC 2019)
- On-Road Diesel
- On-Road Gasoline (Low Mileage)
- On-Road Gasoline (Uncontrolled)
- On-Road Gasoline (Oxidation Catalyst)
- On-Road Natural Gas
- On-Road LPG
- Off-Road Diesel
- Off-Road Gasoline
- On-Road Petrol (DESNZ 2024)
- On-Road Diesel (DESNZ 2024)
- On-Road LPG (DESNZ 2024)
- Gasoline (generic)
- Diesel (generic)
- CNG
- Vehicle distance (avg car)

#### Fugitive Emissions (6 sources)
- R-410A
- R-432A
- HCFC-22 / R-22
- HFC-227ea
- R-600a (Isobutane)
- Methane (CH4)

---

### Scope 2: Indirect Emissions from Energy (9 sources)

#### Purchased Electricity (5 sources)
- Grid average
- US grid
- EU grid
- China grid
- 100% renewable

#### Steam & Heat (4 sources)
- District heating
- District cooling
- Steam
- Chilled water

---

### Scope 3: Other Indirect Emissions (40 sources)

#### Business Travel (6 sources)
- Short-haul flight (<500 km)
- Medium-haul flight (500–3700 km)
- Long-haul flight (>3700 km)
- Train
- Taxi
- Bus

#### Employee Commuting (5 sources)
- Car
- Bus
- Train
- Motorcycle
- Bicycle

#### Purchased Goods & Services (13 sources)
- Electrical items – large
- Electrical items – small
- Electrical items – fridges & freezers
- Electrical items – IT
- Glass
- Metal: aluminium cans & foil
- Metal: mixed cans
- Metal: steel cans
- Mineral oil
- Paper & board: mixed
- Plastics: average plastics
- Plastics: HDPE
- Wood

#### Waste (4 sources)
- General waste (landfill)
- Recyclable waste
- Organic compost
- Waste incineration

#### Water (2 sources)
- Water supply
- Wastewater treatment

#### Upstream Transportation (4 sources)
- Truck freight
- Rail freight
- Sea freight
- Air freight

#### Other Categories (6 sources)
- Various other Scope 3 categories

---

## Technical Implementation

### API Endpoints
- `GET /en/api/scopes/` - Returns 3 scopes
- `GET /en/api/categories/?scope={id}` - Returns categories for a scope (now includes `code` field)
- `GET /en/api/sources/?category={id}` - Returns sources for a category (now reads from emission_factors.py)
- `POST /en/api/calculate/` - Calculates emissions (now accepts `category` and `country` parameters)

### Data Flow
```
User selects Scope
    ↓
Frontend fetches Categories (with code)
    ↓
User selects Category
    ↓
Frontend fetches Sources (from emission_factors.py via API)
    ↓
User enters Activity Data
    ↓
Frontend sends: {category: code, source: key, activity_data: number}
    ↓
Backend calculates using emission_factors.calculate_emissions()
    ↓
Result returned with emissions_kg, emissions_tons, factor, unit, reference
```

### Key Changes
1. **views.py**: `api_get_sources()` now reads from `emission_factors.py` dictionaries
2. **views.py**: `api_get_categories()` now includes `code` field
3. **views.py**: `calculate_emission()` now has `@csrf_exempt` for API access
4. **data-entry/page.tsx**: Now sends `category` code and `country` in calculation requests

---

## References

All emission factors are sourced from:
- **IPCC 2019** (AR6 GWP100)
- **Defra 2024** (UK GHG Conversion Factors)
- **DESNZ 2024** (Department for Energy Security and Net Zero)
- **Turkey-specific factors** (ATOM KABLO ISO 14064-1)

---

## Testing

Run the complete flow test:
```bash
python test_complete_flow.py
```

Expected output:
- ✓ 3 Scopes loaded
- ✓ 12 Categories loaded
- ✓ 80 Emission sources loaded
- ✓ Calculation successful
- ✓ Results accurate

---

## Next Steps

The system now has complete emission source coverage. Users can:
1. Select from 80 different emission sources
2. Calculate emissions for any activity
3. Save records to database
4. View results in dashboard
5. Generate reports

All sources are properly categorized by Scope (1, 2, 3) and Category, making it easy to comply with GHG Protocol standards.
