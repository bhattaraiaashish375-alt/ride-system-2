"""Tests for Fare Calculator"""

import pytest
from core.fare_calculator import FareCalculator


class TestFareCalculator:
    """Test suite for FareCalculator"""
    
    @pytest.fixture
    def calculator(self):
        """Initialize calculator for each test"""
        return FareCalculator()
    
    def test_bike_fare_calculation(self, calculator):
        """Test bike fare calculation"""
        fare = calculator.calculate_fare(
            distance_km=5,
            time_period='day',
            vehicle_type='bike'
        )
        
        # Base 30 + (5 * 18) = 120
        assert fare['fare'] == 120
        assert fare['vehicle_type'] == 'bike'
    
    def test_car_fare_calculation(self, calculator):
        """Test car fare calculation"""
        fare = calculator.calculate_fare(
            distance_km=5,
            time_period='day',
            vehicle_type='car'
        )
        
        # Base 100 + (5 * 42) = 310
        assert fare['fare'] == 310
        assert fare['vehicle_type'] == 'car'
    
    def test_surge_pricing_morning(self, calculator):
        """Test surge pricing during morning peak"""
        fare = calculator.calculate_fare(
            distance_km=5,
            time_period='morning',
            vehicle_type='bike'
        )
        
        # Base (30 + 90) * 1.35 = 162
        assert fare['surge_multiplier'] == 1.35
        assert fare['fare'] > 120
    
    def test_surge_pricing_evening(self, calculator):
        """Test surge pricing during evening peak"""
        fare = calculator.calculate_fare(
            distance_km=5,
            time_period='evening',
            vehicle_type='bike'
        )
        
        # (30 + 90) * 1.40 = 168
        assert fare['surge_multiplier'] == 1.40
    
    def test_get_time_period(self, calculator):
        """Test time period detection"""
        assert calculator.get_time_period('06:30') == 'morning'
        assert calculator.get_time_period('12:00') == 'day'
        assert calculator.get_time_period('18:00') == 'evening'
        assert calculator.get_time_period('23:00') == 'night'
    
    def test_fare_breakdown(self, calculator):
        """Test detailed fare breakdown"""
        breakdown = calculator.get_fare_breakdown(
            distance_km=10,
            time_period='day',
            vehicle_type='bike'
        )
        
        assert 'breakdown' in breakdown
        assert breakdown['breakdown']['base_fare'] == 30
        assert breakdown['breakdown']['distance_charge'] == 180
