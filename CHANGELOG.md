# Changelog

All notable changes to Academia Carbon will be documented in this file.

## [2.1.0] - 2025-11-26

### Added - DESNZ 2024 Emission Factors
- 🚗 **On-Road (DESNZ 2024)** - Volume-based emission factors for road vehicles
  - Petrol: 2.30233 kg CO2e/litre
  - Diesel: 3.17939 kg CO2e/litre
  - LPG, Motor Gasoline variants, Natural Gas (GJ-based)
- ❄️ **Fugitive Emissions (DESNZ 2024)** - Complete refrigerant leakage tracking
  - R-410A: GWP 2,088 (highest impact)
  - R-432A: GWP 1,940
  - R-22 (HCFC-22): GWP 1,810 (being phased out)
  - Methane (CH4): GWP 27.9 (IPCC AR6)
  - R-600A (Isobutane): GWP 3.0 (natural refrigerant)
- 🚜 **Off-Road (DESNZ 2024)** - Equipment and machinery emissions
  - Diesel: 3.17939 kg CO2e/litre
  - Gasoline: 2.30233 kg CO2e/litre

### Improved
- 📝 Enhanced data entry forms with supplier tracking
- 🔧 Fixed JavaScript source selection for fugitive emissions
- 📊 Better form validation and user feedback
- 🎨 Consistent UI across all emission categories
- 📱 **Complete Mobile Optimization** - Fully responsive design for all devices
  - Touch-optimized buttons (min 44px)
  - Mobile-first navigation with hamburger menu
  - Responsive tables with card view on mobile
  - Optimized forms to prevent iOS zoom
  - Better spacing and typography for small screens

### Technical
- Updated emission_factors.py with DESNZ 2024 standards
- Improved category-specific source detection in JavaScript
- Added character counter for description fields
- Enhanced supplier management integration

## [2.0.0] - 2025-11-24

### Added
- 🎓 Rebranded to "Academia Carbon" with academic focus
- 🔐 Email-based authentication system
- 📊 Emission calculation for Scope 1, 2, and 3
- 🌍 Turkey-specific emission factors (2025 updated)
- 📈 Emission history tracking
- 🎨 Modern, responsive UI design
- 🇹🇷 Turkey 2025 emission factors with 20% renewable energy
- 🚗 Electric and hybrid vehicle emission factors
- ♻️ Updated waste management factors (40% recycling target)
- 📱 Mobile-responsive design
- 🔍 User-specific emission records
- 📝 Comprehensive user guide

### Changed
- Updated electricity grid factor: 0.486 → 0.452 kg CO2e/kWh (Turkey)
- Improved natural gas factor: 2.03 → 1.99 kg CO2e/m³
- Enhanced aviation factors with new fleet data
- Better waste management factors with Zero Waste improvements
- Modernized login/signup pages with nature-inspired design

### Removed
- Username-based authentication (replaced with email)
- Persian/Farsi language files (English-only interface)
- Temporary documentation files
- GitHub social login button (kept Google only)

### Fixed
- Form validation for email authentication
- Responsive design on mobile devices
- Emission calculation accuracy
- User session management

## [1.0.0] - 2024-11-01

### Added
- Initial release
- Basic emission tracking
- Country comparison
- Admin panel
- Turkish translations

---

## Version History

- **2.0.0** (2025-11-24) - Academia Carbon rebrand, email auth, Turkey 2025 factors
- **1.0.0** (2024-11-01) - Initial release

---

**Note**: This project follows [Semantic Versioning](https://semver.org/).
