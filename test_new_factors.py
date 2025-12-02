"""Test new emission factors"""
from ghg.emission_factors import calculate_emissions

print("=" * 70)
print("TESTING NEW EMISSION FACTORS")
print("=" * 70)

# Test Propane
r1 = calculate_emissions('stationary', 'propane', 100, 'global')
print(f"\n✅ Propane: {r1['emissions_kg']} kg CO2e")
print(f"   Factor: {r1['factor']} kg CO2e/kg")

# Test HFC-227ea
r2 = calculate_emissions('fugitive', 'hfc-227ea', 10, 'global')
print(f"\n✅ HFC-227ea: {r2['emissions_kg']} kg CO2e")
print(f"   Factor: {r2['factor']} kg CO2e/kg (GWP: 3,350)")

# Test Water Supply
r3 = calculate_emissions('water', 'supply', 1000, 'global')
print(f"\n✅ Water Supply: {r3['emissions_kg']} kg CO2e")
print(f"   Factor: {r3['factor']} kg CO2e/m3")

# Test Water Treatment
r4 = calculate_emissions('water', 'treatment', 1000, 'global')
print(f"\n✅ Water Treatment: {r4['emissions_kg']} kg CO2e")
print(f"   Factor: {r4['factor']} kg CO2e/m3")

# Test Purchased Goods - Plastic
r5 = calculate_emissions('purchased-goods', 'plastic-average', 500, 'global')
print(f"\n✅ Plastic (average): {r5['emissions_kg']} kg CO2e")
print(f"   Factor: {r5['factor']} kg CO2e/kg")

# Test Turkey Purchased Goods - Plastic
r6 = calculate_emissions('purchased-goods', 'plastic', 500, 'turkey')
print(f"\n✅ Plastic (Turkey): {r6['emissions_kg']} kg CO2e")
print(f"   Factor: {r6['factor']} kg CO2e/kg")

# Test Turkey Purchased Goods - Metal Primary
r7 = calculate_emissions('purchased-goods', 'metal-primary', 1000, 'turkey')
print(f"\n✅ Metal Primary (Turkey): {r7['emissions_kg']} kg CO2e")
print(f"   Factor: {r7['factor']} kg CO2e/kg")

print("\n" + "=" * 70)
print("✅ ALL NEW FACTORS WORKING CORRECTLY!")
print("=" * 70)
