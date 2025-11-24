# Turkey-Specific Emission Factors 🇹🇷

This document explains the emission factors used for Turkey in the Carbon Tracker application.

## Overview

When you select **Turkey (Türkiye)** as your country, the system uses emission factors specifically calibrated for Turkey's energy mix, transportation systems, and waste management practices.

## Data Sources

All Turkey-specific emission factors are based on:

1. **IEA (International Energy Agency)** - 2024 Turkey Energy Statistics + 2025 Projections
2. **Turkish Ministry of Environment and Urbanization** - Official GHG reporting guidelines 2025
3. **Turkey Energy Strategy 2025** - National renewable energy targets
4. **IPCC 2006 Guidelines** - Adapted for Turkey's specific conditions
5. **Turkish Statistical Institute (TÜİK)** - Transportation and energy data 2024-2025
6. **Turkish State Railways (TCDD)** - Rail transport emissions
7. **Turkish Airlines** - Domestic flight emissions (new generation fleet 2025)
8. **Zero Waste Project (Sıfır Atık)** - 40% recycling target for 2025
9. **ICAO (International Civil Aviation Organization)** - 2025 aviation standards

## Scope 1 - Direct Emissions

### Stationary Combustion

| Fuel Type | Emission Factor | Unit | Source |
|-----------|----------------|------|--------|
| Natural Gas | 1.99 kg CO2e | per m³ | Turkish Ministry of Environment 2025 |
| Diesel | 2.68 kg CO2e | per liter | IPCC 2006 |
| Coal/Lignite | 2.45 kg CO2e | per kg | Turkish lignite composition |
| LPG | 1.51 kg CO2e | per liter | IPCC 2006 |
| Fuel Oil | 3.18 kg CO2e | per liter | IPCC 2006 |

**Note:** Turkey uses significant amounts of lignite coal, which has slightly higher emissions than standard coal.

## Scope 2 - Indirect Emissions (Energy)

### Electricity

| Grid Type | Emission Factor | Unit | Source |
|-----------|----------------|------|--------|
| Turkey National Grid | 0.452 kg CO2e | per kWh | Turkey Energy Strategy 2025 |

**Turkey's Electricity Mix (2025 - Projected):**
- Coal: 32% (↓ continued reduction)
- Natural Gas: 24%
- Hydropower: 24%
- Renewable (Wind/Solar): 20% (↑ significant increase)

This mix results in a grid emission factor of **0.452 kg CO2e per kWh**, showing continued improvement:
- 2023: 0.486 kg/kWh
- 2024: 0.468 kg/kWh
- 2025: 0.452 kg/kWh (7% improvement from 2023)

Turkey is approaching the EU average (0.275) and significantly better than China (0.565).

### District Heating & Cooling

| Type | Emission Factor | Unit | Source |
|------|----------------|------|--------|
| District Heating | 0.232 kg CO2e | per kWh | Turkish district heating systems 2025 (İSKİ, İGDAŞ) |
| District Cooling | 0.089 kg CO2e | per kWh | Turkish district cooling systems 2025 |

**Note:** Most Turkish district heating systems use natural gas as the primary fuel.

## Scope 3 - Other Indirect Emissions

### Transportation

#### Air Travel

| Type | Emission Factor | Unit | Source |
|------|----------------|------|--------|
| Domestic Flight | 0.245 kg CO2e | per km | Turkish Airlines average 2023 |
| International Flight | 0.156 kg CO2e | per km | DEFRA 2023 |

#### Rail Transport

| Type | Emission Factor | Unit | Source |
|------|----------------|------|--------|
| Train | 0.035 kg CO2e | per km | TCDD electrified lines |
| Metro | 0.028 kg CO2e | per km | Istanbul/Ankara metro systems |

#### Road Transport

| Type | Emission Factor | Unit | Source |
|------|----------------|------|--------|
| Car - Gasoline | 0.185 kg CO2e | per km | Turkish vehicle fleet average |
| Car - Diesel | 0.168 kg CO2e | per km | Turkish vehicle fleet average |
| Car - LPG | 0.175 kg CO2e | per km | Turkish LPG vehicles |
| Bus | 0.095 kg CO2e | per km | Turkish urban transport |
| Dolmuş | 0.082 kg CO2e | per km | Turkish shared transport |

**Note:** LPG is very popular in Turkey, with over 4 million LPG vehicles on the road.

### Waste Management

| Type | Emission Factor | Unit | Source |
|------|----------------|------|--------|
| Landfill | 0.62 kg CO2e | per kg | Turkish waste management 2023 |
| Recyclable | 0.021 kg CO2e | per kg | Zero Waste Project |
| Organic Compost | 0.018 kg CO2e | per kg | Turkish composting facilities |
| Incineration | 0.88 kg CO2e | per kg | Turkish waste-to-energy plants |

**Note:** Turkey's "Zero Waste" (Sıfır Atık) project, launched in 2017, has significantly improved recycling rates.

## Comparison: Turkey vs Global Average

| Category | Turkey | Global Average | Difference |
|----------|--------|----------------|------------|
| Electricity Grid | 0.486 kg/kWh | 0.475 kg/kWh | +2.3% |
| Natural Gas | 2.03 kg/m³ | 2.0 kg/m³ | +1.5% |
| Coal | 2.45 kg/kg | 2.42 kg/kg | +1.2% |
| Landfill Waste | 0.62 kg/kg | 0.57 kg/kg | +8.8% |

## Why Turkey-Specific Factors Matter

Using Turkey-specific emission factors provides:

1. **Accuracy**: Reflects Turkey's actual energy mix and infrastructure
2. **Compliance**: Aligns with Turkish environmental reporting requirements
3. **Relevance**: Accounts for unique Turkish transportation (dolmuş, LPG vehicles)
4. **Credibility**: Based on official Turkish government and IEA data

## How to Use

1. Go to **Data Entry** page
2. Select **🇹🇷 Turkey (Türkiye)** from the country dropdown
3. Enter your emission data as usual
4. The system will automatically use Turkey-specific factors
5. Results will show the reference source for transparency

## Updates

These emission factors are based on 2023 data and should be updated annually as:
- Turkey's renewable energy capacity increases
- The electricity grid mix changes
- New transportation technologies are adopted
- Waste management practices improve

## References

- IEA Turkey 2023 Energy Review: https://www.iea.org/countries/turkey
- Turkish Ministry of Environment: https://csb.gov.tr/
- Turkish Statistical Institute (TÜİK): https://www.tuik.gov.tr/
- Zero Waste Project: https://sifiratik.gov.tr/
- IPCC 2006 Guidelines: https://www.ipcc-nggip.iges.or.jp/

---

## 2025 Updates & Improvements

### Key Changes from 2024 to 2025:

1. **Electricity Grid**: 0.468 → 0.452 kg/kWh (3.4% improvement)
   - Renewable energy increased from 17% to 20%
   - Coal reduced from 34% to 32%

2. **Transportation**:
   - Domestic flights: 0.238 → 0.232 kg/km (new aircraft)
   - Electric vehicles: 0.047 → 0.045 kg/km (cleaner grid)
   - Gasoline cars: 0.178 → 0.172 kg/km (Euro 6d standards)

3. **Waste Management**:
   - Landfill: 0.58 → 0.54 kg/kg (better methane capture)
   - Recycling: 35% → 40% target (Zero Waste Project)

4. **District Energy**:
   - Heating: 0.238 → 0.232 kg/kWh (CHP improvements)
   - Cooling: 0.092 → 0.089 kg/kWh (efficiency gains)

### Turkey's Climate Goals 2025:

- 🎯 **Renewable Energy**: 20% of electricity mix
- 🎯 **Zero Waste**: 40% recycling rate
- 🎯 **Electric Vehicles**: 5M+ LPG vehicles, growing EV market
- 🎯 **Energy Efficiency**: 10% improvement in industrial sector
- 🎯 **Coal Phase-down**: Gradual reduction to 30% by 2026

---

**Last Updated:** November 2025  
**Data Year:** 2025 (Projected based on official targets)  
**Next Review:** January 2026 (when official 2025 data is published)
