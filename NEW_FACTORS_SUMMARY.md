# New Emission Factors Summary

## ✅ Successfully Added Factors

### 1. Stationary Combustion
**New:**
- **Propane (mass-based):** 2.99763 kg CO2e/kg
  - Source: Defra 2024
  - Use: Industrial heating, forklifts

### 2. Fugitive Emissions
**New:**
- **HFC-227ea:** GWP 3,350 kg CO2e/kg
  - Source: Defra 2024
  - Use: Fire suppression systems, aerosols
  - Impact: Higher than R-410A!

**Existing (confirmed working):**
- R-410A: GWP 2,088
- R-432A: GWP 1,940
- R-22: GWP 1,810
- Methane: GWP 27.9
- R-600A: GWP 3.0

### 3. Water (Scope 3) - NEW CATEGORY!
- **Water Supply:** 0.15311 kg CO2e/m³
  - Source: Defra 2024
  - Use: Municipal water consumption
  
- **Wastewater Treatment:** 0.18574 kg CO2e/m³
  - Source: Defra 2024
  - Use: Sewage treatment

### 4. Purchased Goods (Scope 3) - EXPANDED!

**Global (Defra 2024):**
- Electrical items - large: 3.267 kg CO2e/kg
- Electrical items - small: 5.648 kg CO2e/kg
- Electrical items - fridges: 4.363 kg CO2e/kg
- Electrical items - IT: 24.865 kg CO2e/kg
- Glass: 1.403 kg CO2e/kg
- Metal - aluminium cans: 9.107 kg CO2e/kg
- Metal - mixed cans: 5.106 kg CO2e/kg
- Metal - steel cans: 2.855 kg CO2e/kg
- Mineral oil: 1.401 kg CO2e/kg
- Paper & board mixed: 1.283 kg CO2e/kg
- Plastics average: 3.165 kg CO2e/kg
- Plastics HDPE: 3.086 kg CO2e/kg
- Wood: 0.270 kg CO2e/kg

**Turkey-Specific (ATOM KABLO ISO 14064-1):**
- Chemical: 2.04 kg CO2e/kg
- Chemical oil: 2.04 kg CO2e/kg
- Plastic: 3.102 kg CO2e/kg
- Carton: 0.868 kg CO2e/kg
- Metal (primary): 4.005 kg CO2e/kg
- Metal (recycled): 1.559 kg CO2e/kg
- Wood: 0.313 kg CO2e/kg
- Foam tape: 2.587 kg CO2e/kg

## Test Results

### Example Calculations:
```
Propane: 100 kg → 299.76 kg CO2e
HFC-227ea: 10 kg → 33,500 kg CO2e (33.5 tonnes!)
Water Supply: 1,000 m³ → 153.11 kg CO2e
Water Treatment: 1,000 m³ → 185.74 kg CO2e
Plastic (Global): 500 kg → 1,582.39 kg CO2e
Plastic (Turkey): 500 kg → 1,551.22 kg CO2e
Metal Primary (Turkey): 1,000 kg → 4,005.14 kg CO2e
```

## Code Quality

✅ **No syntax errors**
✅ **No import errors**
✅ **All tests pass**
✅ **Type hints included**
✅ **Well documented**
✅ **Backward compatible**

## Impact

### Before (v2.0.0):
- Scope 1: Basic factors
- Scope 2: Electricity only
- Scope 3: Limited categories

### After (v2.1.0):
- Scope 1: Complete with DESNZ 2024
- Scope 2: Electricity + District Energy
- Scope 3: Water, Purchased Goods, and 10+ categories
- Turkey-specific: ATOM KABLO ISO 14064-1 factors

## Next Steps

1. ✅ Code tested and working
2. ⬜ Update UI to show new factors
3. ⬜ Deploy to server
4. ⬜ Test on production

---

**Status:** ✅ Ready for Production  
**Version:** 2.1.0  
**Date:** November 26, 2025
