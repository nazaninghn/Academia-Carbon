# Carbon Tracker - User Guide 📚

Welcome to Carbon Tracker! This comprehensive guide will help you track, calculate, and manage your organization's greenhouse gas (GHG) emissions.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Dashboard Overview](#dashboard-overview)
3. [Data Entry](#data-entry)
4. [Country Selection](#country-selection)
5. [Scope 1 - Direct Emissions](#scope-1---direct-emissions)
6. [Scope 2 - Indirect Emissions (Energy)](#scope-2---indirect-emissions-energy)
7. [Scope 3 - Other Indirect Emissions](#scope-3---other-indirect-emissions)
8. [Emission History](#emission-history)
9. [Understanding Results](#understanding-results)
10. [Best Practices](#best-practices)
11. [Troubleshooting](#troubleshooting)

---

## Getting Started

### First Steps

1. **Access the Application**
   - Open your browser and go to: `http://127.0.0.1:8000`
   - You'll be redirected to the login page

2. **Login**
   - Username: `admin`
   - Password: `admin123`
   - Click "Sign In"

3. **Navigate to Data Entry**
   - Click on "Emission Management" in the sidebar
   - Or click the green "Data entry" button

### System Requirements

- Modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection (for initial setup)
- Screen resolution: 1280x720 or higher recommended

---

## Dashboard Overview

The dashboard provides a quick overview of your emissions data:

### Key Metrics

- **Total Emissions**: Sum of all recorded emissions
- **Latest Year**: Most recent data year
- **Data Points**: Number of emission records

### Features

- 📊 **Global Emissions Chart**: View worldwide emission trends
- 🌍 **Country Comparison**: Compare emissions across countries
- 📈 **Interactive Charts**: Hover for detailed information

---

## Data Entry

### Accessing Data Entry

1. Click "Emission Management" in the sidebar
2. Select your country/region from the dropdown
3. Choose the appropriate Scope tab (1, 2, or 3)

### Country Selection

At the top of the Data Entry page, you'll see:

```
Country/Region: [Dropdown Menu]
🌍 Global Average
🇹🇷 Turkey (Türkiye)
```

**Important**: Select your country BEFORE entering data to ensure accurate emission factors.

#### Why Country Matters?

Different countries have different:
- Electricity grid mixes
- Fuel compositions
- Transportation systems
- Waste management practices

**Example**: 
- Turkey electricity: 0.486 kg CO2e/kWh
- EU electricity: 0.295 kg CO2e/kWh
- Difference: +64%

---

## Scope 1 - Direct Emissions

Direct emissions from sources owned or controlled by your organization.

### 1. Stationary Combustion

**What it includes**: Fuel burned in boilers, furnaces, heaters

**How to calculate**:

1. Click on "Stationary combustion"
2. Select your fuel type:
   - Natural Gas
   - Diesel
   - Coal
   - LPG
   - Fuel Oil

3. Select unit (liters, kg, m³)
4. Enter activity data (amount consumed)
5. Optional: Add supplier and description
6. Click "Calculate"

**Example**:
```
Fuel: Natural Gas
Amount: 1000 m³
Result: 2,030 kg CO2e (Turkey)
```

### 2. Mobile Combustion

**What it includes**: Fuel burned in company vehicles

**How to calculate**:

1. Click on "Mobile combustion"
2. Select fuel type:
   - Gasoline
   - Diesel
   - CNG
   - LPG (Turkey)

3. Enter fuel consumed (liters) OR distance traveled (km)
4. Click "Calculate"

**Example**:
```
Fuel: Diesel
Amount: 100 liters
Result: 268 kg CO2e
```

### 3. Fugitive Emissions

**What it includes**: Refrigerant leaks, AC systems

**How to calculate**:

1. Click on "Fugitive emissions"
2. Select refrigerant type:
   - R-134a (common in cars)
   - R-410A (common in AC)
   - R-22 (older systems)
   - SF6 (electrical equipment)

3. Enter amount leaked (kg)
4. Click "Calculate"

**Warning**: Refrigerants have VERY high global warming potential!

**Example**:
```
Refrigerant: R-134a
Amount: 1 kg
Result: 1,430 kg CO2e (equivalent to driving 8,400 km!)
```

---

## Scope 2 - Indirect Emissions (Energy)

Emissions from purchased energy.

### 1. Electricity

**What it includes**: All electricity purchased from the grid

**How to calculate**:

1. Click on "Electricity"
2. Select grid type (or it auto-selects based on country)
3. Enter consumption in kWh
4. Optional: Add supplier (e.g., "TEDAŞ")
5. Click "Calculate"

**Where to find data**:
- Monthly electricity bills
- Meter readings
- Building management system

**Example**:
```
Country: Turkey
Consumption: 10,000 kWh
Result: 4,860 kg CO2e
```

### 2. Steam, Heat and Cooling

**What it includes**: District heating/cooling, purchased steam

**How to calculate**:

1. Click on "Steam, Heat and Cooling"
2. Select type:
   - District Heating
   - District Cooling
   - Steam
   - Chilled Water

3. Enter consumption (kWh, MJ, MMBtu, or tons)
4. Click "Calculate"

**Example**:
```
Type: District Heating
Amount: 5,000 kWh
Result: 1,225 kg CO2e (Turkey)
```

---

## Scope 3 - Other Indirect Emissions

Emissions from your value chain.

### 1. Purchased Goods and Services

**What it includes**: Paper, electronics, furniture, office supplies

**Categories**:
- Paper Products: 1.32 kg CO2e per kg
- Electronics: 85 kg CO2e per unit
- Furniture: 120 kg CO2e per unit
- Office Supplies: 2.5 kg CO2e per kg

**Example**:
```
Item: Paper
Amount: 100 kg
Result: 132 kg CO2e
```

### 2. Capital Goods

**What it includes**: Machinery, vehicles, buildings, IT equipment

**Example**:
```
Item: New Vehicle
Amount: 1 unit
Result: 6,000 kg CO2e
```

### 3. Business Travel

**What it includes**: Employee travel in vehicles not owned by company

**Turkey-specific options**:
- ✈️ Domestic Flight: 0.245 kg CO2e/km
- 🚂 Train (TCDD): 0.035 kg CO2e/km
- 🚇 Metro: 0.028 kg CO2e/km
- 🚌 Bus: 0.095 kg CO2e/km
- 🚐 Dolmuş: 0.082 kg CO2e/km

**Example**:
```
Travel: Istanbul to Ankara (450 km)
Mode: Domestic Flight
Result: 110.25 kg CO2e
```

### 4. Employee Commuting

**What it includes**: Daily commute between home and work

**How to calculate**:

1. Survey employees about:
   - Transportation mode
   - Distance (one way)
   - Days per week

2. Calculate monthly:
   ```
   Distance × 2 (round trip) × Days per month × Emission factor
   ```

**Example**:
```
Mode: Car
Distance: 20 km/day
Days: 20 days/month
Total: 800 km/month
Result: 136.8 kg CO2e/month (Turkey car average)
```

### 5. Waste Generated

**What it includes**: Waste disposal and treatment

**Turkey waste factors**:
- Landfill: 0.62 kg CO2e/kg
- Recyclable: 0.021 kg CO2e/kg
- Organic Compost: 0.018 kg CO2e/kg
- Incineration: 0.88 kg CO2e/kg

**Example**:
```
Waste: General waste to landfill
Amount: 500 kg
Result: 310 kg CO2e (Turkey)
```

### 6. Upstream Transportation

**What it includes**: Transportation of purchased goods to your facility

**How to calculate**:

1. Get shipping data from suppliers
2. Calculate tonne-km: Weight (tonnes) × Distance (km)
3. Select transport mode

**Example**:
```
Mode: Truck Freight
Weight: 5 tonnes
Distance: 200 km
Tonne-km: 1,000
Result: 112 kg CO2e
```

---

## Emission History

### Viewing Your History

1. Click "History" in the sidebar
2. View all your calculated emissions

### What You'll See

**Summary Cards**:
- Total Emissions (all scopes)
- Scope 1 Total (red)
- Scope 2 Total (orange)
- Scope 3 Total (blue)

**History Table**:
- Date and time of calculation
- Scope badge (color-coded)
- Source name and description
- Activity data
- Country used
- Emissions (kg and tons)

### Filtering and Analysis

- Records are sorted by date (newest first)
- Shows last 50 records
- Color-coded by scope for easy identification

---

## Understanding Results

### Reading the Calculation Result

When you click "Calculate", you'll see:

```
✓ Calculation Result (Saved to History)

Activity Data          Emission Factor
1000 kwh              0.486 kg CO2e/kwh

Total Emissions (kg)   Total Emissions (tons)
486.0 kg CO2e         0.486 t CO2e

ℹ️ Source: Turkey National Grid | Country: 🇹🇷 Turkey
📖 Reference: IEA 2023 - Turkey electricity mix
```

### Key Components

1. **Activity Data**: What you entered
2. **Emission Factor**: The conversion factor used
3. **Total Emissions**: Your carbon footprint
4. **Source**: Where the factor comes from
5. **Reference**: Scientific basis

### What is CO2e?

**CO2e** = Carbon Dioxide Equivalent

It's a standard unit that converts all greenhouse gases to the equivalent amount of CO2:
- CO2 = 1
- Methane (CH4) = 25
- Nitrous Oxide (N2O) = 298
- R-134a = 1,430

---

## Best Practices

### 1. Data Collection

✅ **DO**:
- Collect data monthly for accuracy
- Keep copies of bills and invoices
- Use actual meter readings
- Document data sources
- Add descriptions to records

❌ **DON'T**:
- Use estimates when actual data is available
- Mix different time periods
- Forget to include all facilities

### 2. Country Selection

✅ **Always select your country BEFORE calculating**
- More accurate results
- Compliant with local regulations
- Better for reporting

### 3. Scope Coverage

**Minimum Requirements**:
- Scope 1: All direct emissions
- Scope 2: All purchased electricity

**Recommended**:
- Scope 3: At least business travel and waste

**Best Practice**:
- Track all 15 Scope 3 categories

### 4. Regular Tracking

**Monthly**: 
- Electricity consumption
- Fuel consumption
- Waste generation

**Quarterly**:
- Business travel
- Employee commuting

**Annually**:
- Capital goods
- Purchased goods and services

### 5. Documentation

For each entry, include:
- Date of activity
- Source of data (bill number, invoice)
- Supplier name
- Any relevant notes

---

## Troubleshooting

### Common Issues

#### 1. "Invalid source" error

**Problem**: Selected source not available for chosen country

**Solution**: 
- Check country selection
- Some sources are country-specific (e.g., "Dolmuş" only in Turkey)
- Switch to global if needed

#### 2. Results seem too high/low

**Problem**: Unexpected emission values

**Solution**:
- Verify activity data (check decimal point)
- Confirm correct unit selected
- Check country selection
- Review emission factor in result

#### 3. Can't see history

**Problem**: History page is empty

**Solution**:
- Ensure you clicked "Calculate" (not just filled the form)
- Check that you're logged in
- Verify data was saved (look for "Saved to History" message)

#### 4. Country-specific source not showing

**Problem**: Expected source not in dropdown

**Solution**:
- Confirm country is selected correctly
- Some sources only appear for specific countries
- Example: "Dolmuş" only shows when Turkey is selected

### Getting Help

If you encounter issues:

1. Check this guide first
2. Review the QUICKSTART.md for basic setup
3. Check TURKEY_EMISSION_FACTORS.md for Turkey-specific info
4. Contact your system administrator

---

## Emission Factor References

### Global Standards

- **IPCC**: Intergovernmental Panel on Climate Change
- **EPA**: US Environmental Protection Agency
- **DEFRA**: UK Department for Environment
- **GHG Protocol**: World Resources Institute

### Turkey-Specific

- **IEA**: International Energy Agency (Turkey 2023)
- **Turkish Ministry of Environment**: Official GHG guidelines
- **TÜİK**: Turkish Statistical Institute
- **TCDD**: Turkish State Railways

---

## Reporting Tips

### Monthly Report Checklist

- [ ] All electricity bills entered
- [ ] All fuel purchases recorded
- [ ] Business travel logged
- [ ] Waste disposal tracked
- [ ] Review history for completeness
- [ ] Check totals by scope

### Annual Report

1. **Export Data**: Use history page
2. **Calculate Totals**: Sum by scope
3. **Identify Hotspots**: What contributes most?
4. **Set Targets**: Reduction goals for next year
5. **Document Changes**: New equipment, processes

---

## Glossary

**Activity Data**: The amount of activity (kWh, liters, km, etc.)

**CO2e**: Carbon Dioxide Equivalent - standard unit for GHG

**Emission Factor**: Conversion factor (kg CO2e per unit)

**GHG**: Greenhouse Gas (CO2, CH4, N2O, etc.)

**Scope 1**: Direct emissions you control

**Scope 2**: Indirect emissions from purchased energy

**Scope 3**: All other indirect emissions in value chain

**Tonne-km**: Weight (tonnes) × Distance (km) - used for freight

---

## Quick Reference Card

### Most Common Calculations

| Activity | Typical Amount | Turkey Factor | Result |
|----------|---------------|---------------|---------|
| Electricity | 1,000 kWh | 0.486 | 486 kg CO2e |
| Natural Gas | 100 m³ | 2.03 | 203 kg CO2e |
| Diesel (car) | 50 liters | 2.68 | 134 kg CO2e |
| Domestic Flight | 500 km | 0.245 | 122.5 kg CO2e |
| Waste (landfill) | 100 kg | 0.62 | 62 kg CO2e |

### Conversion Factors

- 1 ton = 1,000 kg
- 1 MWh = 1,000 kWh
- 1 gallon ≈ 3.785 liters
- 1 mile ≈ 1.609 km

---

## Support & Resources

### Documentation

- `README.md` - Project overview
- `QUICKSTART.md` - Quick setup guide
- `TURKEY_EMISSION_FACTORS.md` - Turkey-specific factors
- `MULTILINGUAL.md` - Language support

### External Resources

- [GHG Protocol](https://ghgprotocol.org/)
- [IPCC Guidelines](https://www.ipcc-nggip.iges.or.jp/)
- [IEA Turkey](https://www.iea.org/countries/turkey)
- [Turkish Ministry of Environment](https://csb.gov.tr/)

---

## Version History

- **v1.0** (November 2025)
  - Initial release
  - Turkey-specific emission factors
  - All 3 scopes supported
  - Emission history tracking

---

**Last Updated**: November 24, 2025  
**Application Version**: 1.0  
**For Support**: Contact your system administrator

---

*Happy tracking! Together we can reduce emissions and fight climate change.* 🌍💚
