"""Multi-Service Ride Fare Comparator"""

import random
from core.fare_calculator import FareCalculator
from config.fare_config import RIDE_SERVICES, SERVICE_VARIATIONS


class RideComparator:
    """Compare fares across multiple ride services"""
    
    def __init__(self):
        self.fare_calculator = FareCalculator()
        self.services = RIDE_SERVICES
        self.variations = SERVICE_VARIATIONS
    
    def apply_service_variation(self, base_fare, service):
        """Apply service-specific price variation
        
        Args:
            base_fare: int - Base calculated fare
            service: str - Service name (pathao, indrive, yango)
            
        Returns:
            int: Adjusted fare with service variation
        """
        if service not in self.variations:
            return base_fare
        
        variation_range = self.variations[service]
        variance_percent = random.uniform(variation_range['min_variance'], variation_range['max_variance'])
        adjusted_fare = round(base_fare * (1 + variance_percent / 100))
        
        return max(adjusted_fare, int(base_fare * 0.8))  # Never below 80% of base
    
    def compare_fares(self, distance_km, time_period=None, vehicle_type='bike'):
        """Compare fares across all services
        
        Args:
            distance_km: float - Distance in kilometers
            time_period: str - Time period or None (uses current)
            vehicle_type: str - 'bike' or 'car'
            
        Returns:
            dict: Comparison with best deal highlighted
        """
        base_fare_result = self.fare_calculator.calculate_fare(
            distance_km, time_period, vehicle_type
        )
        base_fare = base_fare_result['fare']
        
        comparisons = {}
        for service in self.services:
            adjusted_fare = self.apply_service_variation(base_fare, service)
            comparisons[service] = {
                'fare': adjusted_fare,
                'variance_from_base': adjusted_fare - base_fare,
                'variance_percent': round((adjusted_fare - base_fare) / base_fare * 100, 2)
            }
        
        # Find cheapest and most expensive
        cheapest_service = min(comparisons, key=lambda x: comparisons[x]['fare'])
        most_expensive_service = max(comparisons, key=lambda x: comparisons[x]['fare'])
        
        cheapest_fare = comparisons[cheapest_service]['fare']
        most_expensive_fare = comparisons[most_expensive_service]['fare']
        savings = most_expensive_fare - cheapest_fare
        
        return {
            'distance_km': distance_km,
            'vehicle_type': vehicle_type,
            'time_period': time_period or self.fare_calculator.get_time_period(),
            'comparisons': comparisons,
            'best_deal': {
                'service': cheapest_service,
                'fare': cheapest_fare
            },
            'worst_deal': {
                'service': most_expensive_service,
                'fare': most_expensive_fare
            },
            'potential_savings': savings,
            'savings_percent': round(savings / most_expensive_fare * 100, 2)
        }
    
    def get_ranked_services(self, distance_km, time_period=None, vehicle_type='bike'):
        """Get services ranked by price (cheapest to most expensive)
        
        Args:
            distance_km: float
            time_period: str or None
            vehicle_type: str
            
        Returns:
            list: Services ranked by fare
        """
        comparison = self.compare_fares(distance_km, time_period, vehicle_type)
        
        ranked = sorted(
            comparison['comparisons'].items(),
            key=lambda x: x[1]['fare']
        )
        
        return [
            {
                'rank': i + 1,
                'service': service,
                'fare': data['fare'],
                'difference_from_cheapest': data['fare'] - ranked[0][1]['fare']
            }
            for i, (service, data) in enumerate(ranked)
        ]
