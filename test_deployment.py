"""
Quick deployment test script
Run this after deployment to verify everything works
"""

import sys
import os

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carbon_tracker.settings')

import django
django.setup()

from ghg.emission_factors import calculate_emissions

def test_emission_calculations():
    """Test all new emission factor calculations"""
    
    print("=" * 70)
    print("DEPLOYMENT TEST - Emission Calculations")
    print("=" * 70)
    
    tests = [
        {
            'name': 'On-Road Diesel (DESNZ 2024)',
            'category': 'mobile',
            'source': 'on-road-diesel-desnz',
            'activity': 100,
            'expected_min': 317,
            'expected_max': 318
        },
        {
            'name': 'On-Road Petrol (DESNZ 2024)',
            'category': 'mobile',
            'source': 'on-road-petrol-desnz',
            'activity': 100,
            'expected_min': 230,
            'expected_max': 231
        },
        {
            'name': 'R-410A Fugitive',
            'category': 'fugitive',
            'source': 'r410a',
            'activity': 10,
            'expected_min': 20880,
            'expected_max': 20880
        },
        {
            'name': 'R-432A Fugitive',
            'category': 'fugitive',
            'source': 'r432a',
            'activity': 10,
            'expected_min': 19400,
            'expected_max': 19400
        },
        {
            'name': 'R-22 Fugitive',
            'category': 'fugitive',
            'source': 'r22',
            'activity': 10,
            'expected_min': 18100,
            'expected_max': 18100
        },
        {
            'name': 'Methane Fugitive',
            'category': 'fugitive',
            'source': 'methane',
            'activity': 10,
            'expected_min': 279,
            'expected_max': 279
        },
        {
            'name': 'R-600A Fugitive',
            'category': 'fugitive',
            'source': 'r600a',
            'activity': 10,
            'expected_min': 30,
            'expected_max': 30
        },
        {
            'name': 'Off-Road Diesel (DESNZ 2024)',
            'category': 'mobile',
            'source': 'off-road-diesel',
            'activity': 100,
            'expected_min': 317,
            'expected_max': 318
        }
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            result = calculate_emissions(
                category=test['category'],
                source=test['source'],
                activity_data=test['activity'],
                country='global'
            )
            
            emissions = result['emissions_kg']
            
            if test['expected_min'] <= emissions <= test['expected_max']:
                print(f"✅ PASS: {test['name']}")
                print(f"   Expected: {test['expected_min']}-{test['expected_max']}, Got: {emissions}")
                passed += 1
            else:
                print(f"❌ FAIL: {test['name']}")
                print(f"   Expected: {test['expected_min']}-{test['expected_max']}, Got: {emissions}")
                failed += 1
                
        except Exception as e:
            print(f"❌ ERROR: {test['name']}")
            print(f"   {str(e)}")
            failed += 1
    
    print("\n" + "=" * 70)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 70)
    
    if failed == 0:
        print("✅ ALL TESTS PASSED - Deployment successful!")
        return True
    else:
        print("❌ SOME TESTS FAILED - Check errors above")
        return False


def test_imports():
    """Test that all modules can be imported"""
    print("\n" + "=" * 70)
    print("TESTING IMPORTS")
    print("=" * 70)
    
    try:
        from ghg import models, views, emission_factors
        print("✅ ghg modules imported successfully")
        
        from carbon_tracker import settings
        print("✅ settings imported successfully")
        
        return True
    except Exception as e:
        print(f"❌ Import error: {str(e)}")
        return False


def main():
    """Run all tests"""
    print("\n🚀 Starting Deployment Tests...\n")
    
    # Test imports
    imports_ok = test_imports()
    
    if not imports_ok:
        print("\n❌ Import tests failed. Fix imports before testing calculations.")
        sys.exit(1)
    
    # Test calculations
    calcs_ok = test_emission_calculations()
    
    if calcs_ok:
        print("\n✅ Deployment verification complete - All systems operational!")
        sys.exit(0)
    else:
        print("\n❌ Deployment verification failed - Check errors above")
        sys.exit(1)


if __name__ == '__main__':
    main()
