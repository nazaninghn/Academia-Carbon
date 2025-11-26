# Release Notes - Version 2.1.0

**Release Date:** November 26, 2025

## 🎉 What's New

### DESNZ 2024 Emission Factors

We've added comprehensive support for the latest UK Government GHG Conversion Factors (DESNZ 2024):

#### 🚗 On-Road Emissions (Volume-Based)
Calculate emissions from road vehicles using fuel consumption in litres:
- **Petrol/Gasoline:** 2.30233 kg CO2e per litre
- **Diesel:** 3.17939 kg CO2e per litre
- **LPG, Natural Gas, Motor Gasoline variants** (energy-based)

**Use Cases:**
- Company car fleets
- Delivery vehicles
- Employee commuting
- Business travel

#### ❄️ Fugitive Emissions (Refrigerant Leakage)
Track greenhouse gas emissions from refrigerant leaks with complete GWP factors:

| Refrigerant | GWP | Common Use |
|-------------|-----|------------|
| **R-410A** | 2,088 | Modern HVAC systems (highest impact) |
| **R-432A** | 1,940 | Commercial refrigeration |
| **R-22 (HCFC-22)** | 1,810 | Legacy systems (being phased out) |
| **Methane (CH4)** | 27.9 | Natural gas leaks, pipelines |
| **R-600A (Isobutane)** | 3.0 | Domestic refrigerators (natural, eco-friendly) |

**Use Cases:**
- HVAC system maintenance
- Cold storage facilities
- Supermarket refrigeration
- Natural gas infrastructure

#### 🚜 Off-Road Emissions
Calculate emissions from construction equipment, agricultural machinery, and generators:
- **Diesel:** 3.17939 kg CO2e per litre
- **Gasoline:** 2.30233 kg CO2e per litre

**Use Cases:**
- Construction sites
- Agricultural operations
- Backup generators
- Industrial equipment

### 📊 Enhanced Features

#### Supplier Management
- Track emission sources by supplier/vendor
- Add supplier details (contact, location, type)
- Link emissions to specific suppliers
- Better audit trail and reporting

#### Improved User Interface
- Enhanced data entry forms
- Character counters for descriptions
- Better validation and error messages
- Consistent styling across all categories

#### Technical Improvements
- Fixed JavaScript source selection bug
- Category-specific ID-based detection
- Better form field management
- Improved code maintainability

## 📈 Impact Examples

### Example 1: Company Fleet
```
Fuel Type: Diesel
Consumption: 12,000 litres/year
Emissions: 38.15 tonnes CO2e/year
```

### Example 2: Office Building HVAC
```
Refrigerant: R-410A
Leakage: 45 kg/year
Emissions: 93.96 tonnes CO2e/year
```

### Example 3: Construction Equipment
```
Equipment: Excavators & Loaders
Fuel: Diesel
Consumption: 5,000 litres/year
Emissions: 15.90 tonnes CO2e/year
```

## 🔄 Migration Notes

### For Existing Users
- All existing data remains intact
- New emission sources are available immediately
- No database migration required
- Backward compatible with previous calculations

### For Developers
- Updated `ghg/emission_factors.py` with DESNZ 2024 factors
- Enhanced `templates/data_entry.html` with new forms
- Improved JavaScript validation logic
- Added supplier integration

## 📚 Documentation

Updated documentation includes:
- `CHANGELOG.md` - Complete version history
- `README.md` - Updated feature list
- Inline help text in forms
- Source references for all factors

## 🌍 Standards & Compliance

This release implements:
- **DESNZ 2024** - UK Government GHG Conversion Factors
- **IPCC AR6** - Latest Global Warming Potentials
- **Montreal Protocol** - Phase-out tracking for ozone-depleting substances

## 🙏 Acknowledgments

Emission factors sourced from:
- UK Department for Energy Security and Net Zero (DESNZ)
- Intergovernmental Panel on Climate Change (IPCC)
- International Energy Agency (IEA)

## 📞 Support

For questions or issues:
- Check `TROUBLESHOOTING.md`
- Review `QUICKSTART.md` for setup help
- See `CONTRIBUTING.md` for development guidelines

---

**Version:** 2.1.0  
**Previous Version:** 2.0.0  
**Release Type:** Minor (New Features)  
**Breaking Changes:** None
