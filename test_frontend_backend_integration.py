#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Integration test for frontend-backend emission calculations
Tests all emission factor categories with both Turkey and Global data
"""

from ghg.emission_factors import calculate_emissions, get_emission_sources

def test_category(category, country='global'):
    """Test all sources in a category"""
    print(f"\n{'='*60}")
    print(f"Testing Category: {category.upper()} ({country.upper()})")
    print('='*60)
    
    sources = get_emission_sources(category, country)
    
    if not sources:
        print(f"❌ No sources found for {category} in {country}")
        return False
    
    print(f"✓ Found {len(sources)} sources")
    
    success_count = 0
    for source_key, source_data in sources.items():
        # Test with sample activity data
        test_value = 100
        result = calculate_emissions(category, source_key, test_value, country)
        
        if 'error' in result:
            print(f"  ❌ {source_key}: {result['error']}")
        else:
            success_count += 1
            print(f"  ✓ {source_key}: {test_value} {result['unit']} = {result['emissions_kg']} kg CO2e")
    
    print(f"\nResult: {success_count}/{len(sources)} sources working")
    return success_count == len(sources)

def main():
    print("="*60)
    print("EMISSION FACTOR INTEGRATION TEST")
    print("="*60)
    
    # Test categories for both Turkey and Global
    test_cases = [
        # Scope 1
        ('stationary', 'turkey'),
        ('stationary', 'global'),
        ('mobile', 'turkey'),
        ('mobile', 'global'),
        ('fugitive', 'global'),
        
        # Scope 2
        ('electricity', 'turkey'),
        ('electricity', 'global'),
        ('steam-heat', 'turkey'),
        ('steam-heat', 'global'),
        
        # Scope 3
        ('water', 'global'),
        ('purchased-goods', 'turkey'),
        ('purchased-goods', 'global'),
        ('travel', 'turkey'),
        ('travel', 'global'),
        ('waste', 'turkey'),
        ('waste', 'global'),
        ('capital-goods', 'global'),
        ('fuel-energy', 'global'),
        ('upstream-transport', 'global'),
        ('commuting', 'turkey'),
        ('commuting', 'global'),
        ('upstream-leased', 'global'),
        ('downstream-transport', 'global'),
        ('end-of-life', 'turkey'),
        ('franchises', 'global'),
        ('investments', 'global'),
    ]
    
    results = []
    for category, country in test_cases:
        success = test_category(category, country)
        results.append((category, country, success))
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, _, success in results if success)
    total = len(results)
    
    print(f"\nTotal: {passed}/{total} categories passed")
    
    if passed == total:
        print("\n✅ ALL TESTS PASSED!")
    else:
        print("\n⚠️ Some tests failed:")
        for category, country, success in results:
            if not success:
                print(f"  ❌ {category} ({country})")
    
    # Test specific calculations
    print("\n" + "="*60)
    print("SAMPLE CALCULATIONS")
    print("="*60)
    
    samples = [
        ('stationary', 'natural-gas', 10, 'turkey', 'Natural gas 10 GJ in Turkey'),
        ('electricity', 'turkey-grid', 1000, 'turkey', 'Turkey grid 1000 kWh'),
        ('purchased-goods', 'plastic', 500, 'turkey', 'Plastic 500 kg (Turkey)'),
        ('travel', 'car-gasoline', 100, 'turkey', 'Car gasoline 100 km (Turkey)'),
        ('water', 'supply', 50, 'global', 'Water supply 50 m³'),
        ('waste', 'landfill', 1000, 'turkey', 'Landfill 1000 kg (Turkey)'),
        ('fugitive', 'r410a', 1, 'global', 'R-410A refrigerant 1 kg'),
    ]
    
    for category, source, activity, country, description in samples:
        result = calculate_emissions(category, source, activity, country)
        if 'error' not in result:
            print(f"\n{description}:")
            print(f"  Activity: {result['activity_data']} {result['unit']}")
            print(f"  Factor: {result['factor']} kg CO2e/{result['unit']}")
            print(f"  Emissions: {result['emissions_kg']} kg CO2e ({result['emissions_tons']} tons)")
            if 'reference' in result:
                print(f"  Source: {result['reference']}")

if __name__ == '__main__':
    main()
