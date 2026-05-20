#!/usr/bin/env python3
"""Main entry point for Ride System 2"""

from core.fare_calculator import FareCalculator
from core.midpoint_calculator import MidpointCalculator
from core.ride_comparator import RideComparator
from core.peak_hour_detector import PeakHourDetector
from services.location_service import LocationService


def print_separator(title=""):
    """Print a formatted separator"""
    if title:
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}")
    else:
        print(f"{'-'*60}")


def demo_fare_calculation():
    """Demo: Calculate ride fares"""
    print_separator("FARE CALCULATION DEMO")
    
    calc = FareCalculator()
    
    # Example 1: Bike ride during day
    print("\n📍 Example 1: Bike to Thamel (5 km) during day")
    fare = calc.calculate_fare(distance_km=5, time_period='day', vehicle_type='bike')
    print(f"   Fare: Rs. {fare['fare']}")
    print(f"   Base: Rs. {fare['base']} | Distance: Rs. {fare['distance_charge']}")
    
    # Example 2: Car ride during morning peak
    print("\n📍 Example 2: Car to Pashupatinath (12 km) during morning peak")
    fare = calc.calculate_fare(distance_km=12, time_period='morning', vehicle_type='car')
    print(f"   Fare: Rs. {fare['fare']}")
    print(f"   Surge Multiplier: {fare['surge_multiplier']}x")
    
    # Example 3: Detailed breakdown
    print("\n📍 Example 3: Detailed breakdown - Evening ride")
    breakdown = calc.get_fare_breakdown(distance_km=8, time_period='evening', vehicle_type='bike')
    print(f"   Base Fare: Rs. {breakdown['breakdown']['base_fare']}")
    print(f"   Distance Charge: Rs. {breakdown['breakdown']['distance_charge']}")
    print(f"   Surge Amount: Rs. {breakdown['breakdown']['surge_amount']}")
    print(f"   TOTAL: Rs. {breakdown['breakdown']['total']}")


def demo_midpoint_calculation():
    """Demo: Calculate midpoint for meetups"""
    print_separator("MIDPOINT CALCULATION DEMO")
    
    calc = MidpointCalculator()
    
    # Example: Three friends meeting
    locations = [
        {'lat': 27.7172, 'lng': 85.3240, 'name': 'Kathmandu Center'},
        {'lat': 27.6815, 'lng': 85.3270, 'name': 'Patan'},
        {'lat': 27.7649, 'lng': 85.3059, 'name': 'Balaju Park'}
    ]
    
    print("\n👥 Three friends meeting:")
    for loc in locations:
        print(f"   • {loc['name']}: {loc['lat']}, {loc['lng']}")
    
    midpoint = calc.calculate_midpoint(locations)
    print(f"\n🎯 Fair Midpoint: {midpoint['lat']}, {midpoint['lng']}")
    
    travel_info = calc.calculate_total_travel(locations, midpoint)
    print(f"\n📊 Travel Information:")
    for distance in travel_info['distances']:
        print(f"   • {distance['location']}: {distance['distance_km']} km")
    print(f"\n   Average Distance: {travel_info['average_distance_km']} km")
    print(f"   Fairness Score: {travel_info['fairness_score']}%")


def demo_ride_comparison():
    """Demo: Compare fares across services"""
    print_separator("RIDE COMPARISON DEMO")
    
    comparator = RideComparator()
    
    print("\n🚗 Comparing car fares during evening peak (7 km):")
    comparison = comparator.compare_fares(
        distance_km=7,
        time_period='evening',
        vehicle_type='car'
    )
    
    print(f"\n{'Service':<15} {'Fare':<10} {'Difference':<15}")
    print(f"{'-'*40}")
    for service, data in comparison['comparisons'].items():
        print(f"{service:<15} Rs. {data['fare']:<5} {data['variance_percent']:+.1f}%")
    
    print(f"\n💰 Best Deal: {comparison['best_deal']['service']} - Rs. {comparison['best_deal']['fare']}")
    print(f"💸 Save: Rs. {comparison['potential_savings']} ({comparison['savings_percent']}%)")
    
    print(f"\n📈 Ranked Services:")
    ranked = comparator.get_ranked_services(7, 'evening', 'car')
    for item in ranked:
        print(f"   {item['rank']}. {item['service'].upper()}: Rs. {item['fare']}")


def demo_peak_hour_detection():
    """Demo: Peak hour detection and surge pricing"""
    print_separator("PEAK HOUR DETECTION DEMO")
    
    detector = PeakHourDetector()
    
    test_times = ['06:30', '12:00', '18:00', '23:00']
    
    for test_time in test_times:
        print(f"\n🕐 Time: {test_time}")
        peak_info = detector.is_peak_hour(test_time)
        print(f"   Period: {peak_info['period'].upper()}")
        print(f"   Peak Hour: {'YES ⚠️' if peak_info['is_peak'] else 'No ✅'}")
        
        surge_info = detector.get_surge_info(test_time, base_fare=100, vehicle_type='bike')
        print(f"   Surge: {surge_info['surge_percentage']*100:.0f}% | Base: Rs. {surge_info['base_fare']} | Total: Rs. {surge_info['total_fare']}")


def demo_location_service():
    """Demo: Location service and offline maps"""
    print_separator("LOCATION SERVICE DEMO")
    
    service = LocationService()
    
    print("\n🔍 Searching for 'Thamel':")
    results = service.search_location('thamel')
    for result in results:
        print(f"   • {result['name']} ({result['area']})")
    
    print("\n🗺️ Nearby locations from Kathmandu Center (10 km radius):")
    nearby = service.get_nearby_locations(27.7172, 85.3240, radius_km=10)
    for loc in nearby[:5]:
        print(f"   • {loc['name']}: {loc['distance_km']} km away")


def main():
    """Run all demos"""
    print("\n")
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║     🚗 RIDE SYSTEM 2 - Kathmandu Valley 🇳🇵                ║")
    print("║     Fare Calculation & Ride Comparison Platform           ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    
    demo_fare_calculation()
    demo_midpoint_calculation()
    demo_ride_comparison()
    demo_peak_hour_detection()
    demo_location_service()
    
    print_separator()
    print("\n✅ Demo completed! Check the code for more features.")
    print("\n📚 Available modules:")
    print("   • FareCalculator: Calculate ride fares")
    print("   • MidpointCalculator: Find fair meeting points")
    print("   • RideComparator: Compare prices across services")
    print("   • PeakHourDetector: Detect surge pricing")
    print("   • LocationService: Offline location management")
    print("\n")


if __name__ == '__main__':
    main()
