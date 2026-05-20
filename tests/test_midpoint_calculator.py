"""Tests for Midpoint Calculator"""

import pytest
import math
from core.midpoint_calculator import MidpointCalculator


class TestMidpointCalculator:
    """Test suite for MidpointCalculator"""
    
    @pytest.fixture
    def calculator(self):
        """Initialize calculator for each test"""
        return MidpointCalculator()
    
    def test_haversine_distance(self, calculator):
        """Test Haversine distance calculation"""
        # Kathmandu to Patan (~3-4 km)
        distance = calculator.haversine_distance(
            27.7172, 85.3240,  # Kathmandu
            27.6815, 85.3270   # Patan
        )
        
        # Should be approximately 3-4 km
        assert 3 < distance < 5
    
    def test_single_location_midpoint(self, calculator):
        """Test midpoint with single location"""
        locations = [{'lat': 27.7172, 'lng': 85.3240}]
        midpoint = calculator.calculate_midpoint(locations)
        
        assert midpoint['lat'] == 27.7172
        assert midpoint['lng'] == 85.3240
        assert midpoint['location_count'] == 1
    
    def test_two_location_midpoint(self, calculator):
        """Test midpoint between two locations"""
        locations = [
            {'lat': 27.7172, 'lng': 85.3240},  # Kathmandu
            {'lat': 27.6815, 'lng': 85.3270}   # Patan
        ]
        midpoint = calculator.calculate_midpoint(locations)
        
        # Midpoint should be between both locations
        assert 27.6815 < midpoint['lat'] < 27.7172
        assert midpoint['location_count'] == 2
    
    def test_travel_distances(self, calculator):
        """Test travel distances calculation"""
        locations = [
            {'lat': 27.7172, 'lng': 85.3240, 'name': 'Kathmandu'},
            {'lat': 27.6815, 'lng': 85.3270, 'name': 'Patan'}
        ]
        midpoint = {'lat': 27.6993, 'lng': 85.3255}
        
        distances = calculator.calculate_travel_distances(locations, midpoint)
        
        assert len(distances) == 2
        assert all('distance_km' in d for d in distances)
    
    def test_total_travel_calculation(self, calculator):
        """Test total travel calculation"""
        locations = [
            {'lat': 27.7172, 'lng': 85.3240},
            {'lat': 27.6815, 'lng': 85.3270},
            {'lat': 27.7649, 'lng': 85.3059}
        ]
        midpoint = calculator.calculate_midpoint(locations)
        travel_info = calculator.calculate_total_travel(locations, midpoint)
        
        assert 'total_distance_km' in travel_info
        assert 'average_distance_km' in travel_info
        assert travel_info['average_distance_km'] > 0
