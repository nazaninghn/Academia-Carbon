# Scope 1 - Complete Formulas & Emission Factors

## Main Calculation Formula:
```
Emissions (kg CO2e) = Activity Data × Emission Factor
```

---

## 1️⃣ Stationary Combustion

### Global Factors:
| Fuel Type | Emission Factor | Unit | Formula |
|-----------|----------------|------|---------|
| **Coal (Industrial)** | 2.40739 | kg CO2e/kg | kg fuel × 2.40739 |
| **Gas/Diesel Oil** | 74.1 | kg CO2e/GJ | GJ energy × 74.1 |
| **LPG** | 1.51468 | kg CO2e/liter | liters × 1.51468 |
| **Motor Gasoline** | 69.55587 | kg CO2e/GJ | GJ energy × 69.55587 |
| **Natural Gas** | 56.211 | kg CO2e/GJ | GJ energy × 56.211 |
| **Diesel (Legacy)** | 2.68 | kg CO2e/liter | liters × 2.68 |
| **Coal (Legacy)** | 2.42 | kg CO2e/kg | kg fuel × 2.42 |
| **Fuel Oil** | 3.18 | kg CO2e/liter | liters × 3.18 |

### Turkey-Specific Factors:
| Fuel Type | Emission Factor | Unit | Formula |
|-----------|----------------|------|---------|
| **Natural Gas (Turkey)** | 56.211 | kg CO2e/GJ | GJ energy × 56.211 |
| **Diesel (Turkey)** | 2.68 | kg CO2e/liter | liters × 2.68 |
| **Coal/Lignite (Turkey)** | 2.45 | kg CO2e/kg | kg fuel × 2.45 |
| **LPG (Turkey)** | 1.51468 | kg CO2e/liter | liters × 1.51468 |
| **Fuel Oil (Turkey)** | 3.18 | kg CO2e/liter | liters × 3.18 |

---

## 2️⃣ Mobile Combustion

### Off-Road Equipment:
| Type | Emission Factor | Unit | Formula |
|------|----------------|------|---------|
| **Off-Road (IPCC 2019)** | 74.39892 | kg CO2e/GJ | GJ energy × 74.39892 |
| **Off-Road Diesel (DESNZ 2024)** | 3.17939 | kg CO2e/liter | liters × 3.17939 |
| **Off-Road Gasoline (DESNZ 2024)** | 2.30233 | kg CO2e/liter | liters × 2.30233 |

### On-Road Vehicles (DESNZ 2024):
| Fuel Type | Emission Factor | Unit | Formula |
|-----------|----------------|------|---------|
| **Petrol/Gasoline** | 2.30233 | kg CO2e/liter | liters × 2.30233 |
| **Diesel** | 3.17939 | kg CO2e/liter | liters × 3.17939 |
| **LPG** | 63.1 | kg CO2e/GJ | GJ energy × 63.1 |
| **Natural Gas** | 56.211 | kg CO2e/GJ | GJ energy × 56.211 |
| **Gasoline Low Mileage** | 69.55587 | kg CO2e/GJ | GJ energy × 69.55587 |
| **Gasoline Uncontrolled** | 69.55587 | kg CO2e/GJ | GJ energy × 69.55587 |
| **Gasoline Oxidation Catalyst** | 69.55587 | kg CO2e/GJ | GJ energy × 69.55587 |

### On-Road Vehicles (IPCC 2019):
| Fuel Type | Emission Factor | Unit | Formula |
|-----------|----------------|------|---------|
| **LPG** | 63.1 | kg CO2e/GJ | GJ energy × 63.1 |
| **Gasoline Low Mileage** | 69.55587 | kg CO2e/GJ | GJ energy × 69.55587 |
| **Gasoline Uncontrolled** | 69.55587 | kg CO2e/GJ | GJ energy × 69.55587 |
| **Gasoline Oxidation Catalyst** | 69.55587 | kg CO2e/GJ | GJ energy × 69.55587 |
| **Diesel** | 74.39892 | kg CO2e/GJ | GJ energy × 74.39892 |
| **Natural Gas** | 56.211 | kg CO2e/GJ | GJ energy × 56.211 |

---

## 3️⃣ Fugitive Emissions

### Refrigerants (DESNZ 2024):
| Type | GWP | Emission Factor | Formula |
|------|-----|----------------|---------|
| **R-410A** | 2,088 | 2088 kg CO2e/kg | kg leaked × 2088 |
| **R-432A** | 1,940 | 1940 kg CO2e/kg | kg leaked × 1940 |
| **R-22 (HCFC-22)** | 1,810 | 1810 kg CO2e/kg | kg leaked × 1810 |
| **Methane (CH4)** | 27.9 | 27.9 kg CO2e/kg | kg leaked × 27.9 |
| **R-600A (Isobutane)** | 3.0 | 3.0 kg CO2e/kg | kg leaked × 3.0 |

---

## Calculation Examples:

### Example 1: Stationary Combustion - Natural Gas
```
Natural Gas Consumption: 1000 GJ
Formula: 1000 GJ × 56.211 kg CO2e/GJ = 56,211 kg CO2e
Result: 56.21 tonnes CO2e
```

### Example 2: Mobile Combustion - Vehicle Diesel
```
Diesel Consumption: 500 liters
Formula: 500 liters × 3.17939 kg CO2e/liter = 1,589.70 kg CO2e
Result: 1.59 tonnes CO2e
```

### Example 3: Fugitive Emissions - R-410A
```
R-410A Leakage: 10 kg
Formula: 10 kg × 2088 kg CO2e/kg = 20,880 kg CO2e
Result: 20.88 tonnes CO2e
```

### Example 4: Fugitive Emissions - Methane
```
Methane Leakage: 100 kg
Formula: 100 kg × 27.9 kg CO2e/kg = 2,790 kg CO2e
Result: 2.79 tonnes CO2e
```

---

## Important Notes:

### Units:
- **GJ** = Gigajoule (energy)
- **liter** = Liter (volume)
- **kg** = Kilogram (mass)
- **kg CO2e** = Kilograms of Carbon Dioxide Equivalent

### Sources:
- **DESNZ 2024** = UK Government GHG Conversion Factors
- **IPCC 2019** = Intergovernmental Panel on Climate Change
- **IPCC AR6** = IPCC Sixth Assessment Report (GWP values)

### Unit Conversion:
```
1 tonne CO2e = 1,000 kg CO2e
```

---

**Date:** November 26, 2025  
**Version:** 2.1.0  
**Source:** Academia Carbon - Emission Factors Database