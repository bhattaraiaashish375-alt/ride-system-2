"""Tests for Ride Comparator"""

import pytest
from core.ride_comparator import RideComparator


class TestRideComparator:
    """Test suite for RideComparator"""
    
    @pytest.fixture
    def comparator(self):
        """Initialize comparator for each test"""
        return RideComparator()
    
    def test_compare_fares(self, comparator):
        """Test fare comparison across services"""
        comparison = comparator.compare_fares(
            distance_km=5,
            time_period='day',
            vehicle_type='bike'
        )
        
        assert 'comparisons' in comparison
        assert 'pathao' in comparison['comparisons']
        assert 'indrive' in comparison['comparisons']
        assert 'yango' in comparison['comparisons']
    
    def test_best_deal_identification(self, comparator):
        """Test identification of best deal"""
        comparison = comparator.compare_fares(
            distance_km=5,
            time_period='day',
            vehicle_type='bike'
        )
        
        assert 'best_deal' in comparison
        assert comparison['best_deal']['service'] in ['pathao', 'indrive', 'yango']
        assert comparison['best_deal']['fare'] > 0
    
    def test_get_ranked_services(self, comparator):
        """Test service ranking by price"""
        ranked = comparator.get_ranked_services(
            distance_km=5,
            time_period='day',
            vehicle_type='bike'
        )
        
        assert len(ranked) == 3
        assert ranked[0]['rank'] == 1
        assert ranked[0]['fare'] <= ranked[1]['fare']
        assert ranked[1]['fare'] <= ranked[2]['fare']
