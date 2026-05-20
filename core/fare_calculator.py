"""Fare Calculation Engine for Kathmandu Valley"""

import math
from datetime import datetime
from config.fare_config import BIKE_FARE, CAR_FARE, TIME_PERIODS


class FareCalculator:
    """Calculate ride fares based on distance, time, and vehicle type"""
    
    def __init__(self):
        self.bike_config = BIKE_FARE
        self.car_config = CAR_FARE
        self.time_periods = TIME_PERIODS
    
    def get_time_period(self, current_time=None):
        """Determine time period from current time
        
        Args:
            current_time: str in format 'HH:MM' or None (uses current time)
            
        Returns:
            str: 'morning', 'day', 'evening', or 'night'
        """
        if current_time is None:
            current_time = datetime.now().strftime('%H:%M')
        
        hour = int(current_time.split(':')[0])
        
        if 6 <= hour < 9:
            return 'morning'
        elif 9 <= hour < 16:
            return 'day'
        elif 16 <= hour < 21:
            return 'evening'
        else:
            return 'night'
    
    def calculate_fare(self, distance_km, time_period=None, vehicle_type='bike'):
        """Calculate ride fare
        
        Args:
            distance_km: float - Distance in kilometers
            time_period: str - 'morning', 'day', 'evening', 'night' or None (uses current)
            vehicle_type: str - 'bike' or 'car'
            
        Returns:
            dict: {'fare': int, 'base': int, 'distance_charge': int, 'surge_multiplier': float}
        """
        if time_period is None:
            time_period = self.get_time_period()
        
        if vehicle_type.lower() == 'bike':
            config = self.bike_config
        elif vehicle_type.lower() == 'car':
            config = self.car_config
        else:
            raise ValueError(f"Invalid vehicle type: {vehicle_type}")
        
        # Calculate base fare + distance charge
        base_fare = config['base']
        distance_charge = distance_km * config['per_km']
        subtotal = base_fare + distance_charge
        
        # Apply surge multiplier
        surge_multiplier = config['surge_multipliers'].get(time_period, 1.0)
        final_fare = round(subtotal * surge_multiplier)
        
        return {
            'fare': final_fare,
            'base': base_fare,
            'distance_charge': round(distance_charge),
            'subtotal': round(subtotal),
            'surge_multiplier': surge_multiplier,
            'time_period': time_period,
            'vehicle_type': vehicle_type,
            'distance_km': distance_km
        }
    
    def calculate_fare_range(self, distance_km, time_period, vehicle_type='bike', variation_percent=5):
        """Calculate fare range with service variations
        
        Args:
            distance_km: float
            time_period: str
            vehicle_type: str
            variation_percent: float - Percentage variation for realistic range
            
        Returns:
            dict: {'min': int, 'max': int, 'avg': int, 'base_fare': int}
        """
        base_result = self.calculate_fare(distance_km, time_period, vehicle_type)
        base_fare = base_result['fare']
        
        variation_amount = round(base_fare * (variation_percent / 100))
        
        return {
            'min': base_fare - variation_amount,
            'max': base_fare + variation_amount,
            'avg': base_fare,
            'base_fare': base_fare,
            'variation_percent': variation_percent
        }
    
    def get_fare_breakdown(self, distance_km, time_period=None, vehicle_type='bike'):
        """Get detailed fare breakdown
        
        Returns:
            dict: Detailed breakdown of fare components
        """
        result = self.calculate_fare(distance_km, time_period, vehicle_type)
        
        surge_amount = result['subtotal'] * (result['surge_multiplier'] - 1)
        
        return {
            **result,
            'surge_amount': round(surge_amount),
            'breakdown': {
                'base_fare': result['base'],
                'distance_charge': result['distance_charge'],
                'surge_amount': round(surge_amount),
                'total': result['fare']
            }
        }
