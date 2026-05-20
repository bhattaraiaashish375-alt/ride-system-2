"""Kathmandu Valley Ride Fare Configuration

Based on real-world data from Pathao, InDrive, and Yango
Data: May 2026
"""

# Bike Fare Structure
BIKE_FARE = {
    'base': 30,  # Base fare in NPR
    'per_km': 18,  # Cost per kilometer
    'surge_multipliers': {
        'morning': 1.35,    # 6 AM - 9 AM: +35%
        'day': 1.0,         # 9 AM - 4 PM: No surge
        'evening': 1.40,    # 4 PM - 9 PM: +40%
        'night': 1.15       # 9 PM - 6 AM: +15%
    }
}

# Car Fare Structure
CAR_FARE = {
    'base': 100,  # Base fare in NPR
    'per_km': 42,  # Cost per kilometer
    'surge_multipliers': {
        'morning': 1.30,    # 6 AM - 9 AM: +30%
        'day': 1.0,         # 9 AM - 4 PM: No surge
        'evening': 1.35,    # 4 PM - 9 PM: +35%
        'night': 1.20       # 9 PM - 6 AM: +20%
    }
}

# Time Period Definitions (24-hour format)
TIME_PERIODS = {
    'morning': {'start': 6, 'end': 9},
    'day': {'start': 9, 'end': 16},
    'evening': {'start': 16, 'end': 21},
    'night': {'start': 21, 'end': 6}  # Wraps around midnight
}

# Ride Services
RIDE_SERVICES = ['pathao', 'indrive', 'yango']

# Service-specific variations (realistic ranges)
SERVICE_VARIATIONS = {
    'pathao': {'min_variance': -2, 'max_variance': 2},  # ±2% variance
    'indrive': {'min_variance': -3, 'max_variance': 3},  # ±3% variance
    'yango': {'min_variance': -1, 'max_variance': 4}     # -1% to +4% variance
}

# Peak hour fare drop thresholds (for notifications)
FARE_DROP_THRESHOLDS = {
    'notification_drop_percentage': 10,  # Alert if fare drops 10%+
    'check_interval_minutes': 5
}

# Multi-stop route optimization
ROUTE_OPTIMIZATION = {
    'max_stops': 10,
    'wait_time_per_stop_minutes': 2,
    'optimization_algorithms': ['shortest_distance', 'fastest_time']
}
