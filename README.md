# Ride System 2 - Kathmandu Valley Ride Sharing Platform

A Python-based ride sharing application for Kathmandu Valley that calculates fares, finds midpoints between friends, compares prices across multiple ride services, and integrates offline map support.

## Features

### Core Functionality
- **Fare Calculation**: Dynamic pricing based on distance, time of day, and surge pricing
- **Midpoint Calculator**: Find fair meeting points between multiple users
- **Ride Comparison**: Compare fares across Pathao, InDrive, and Yango
- **Peak Hour Detection**: Identify and warn about surge pricing
- **Offline Map Support**: Location services without internet dependency
- **Multi-Stop Route Planning**: Optimize routes for group pickups
- **Smart Notifications**: Alerts for fare drops and peak hours

## Project Structure

```
ride-system-2/
├── README.md
├── requirements.txt
├── config/
│   ├── __init__.py
│   ├── fare_config.py          # Kathmandu Valley fare data
│   └── locations.py             # Pre-defined locations database
├── core/
│   ├── __init__.py
│   ├── fare_calculator.py       # Fare calculation engine
│   ├── midpoint_calculator.py   # Midpoint calculation logic
│   ├── ride_comparator.py       # Multi-service fare comparison
│   └── peak_hour_detector.py    # Surge pricing detection
├── services/
│   ├── __init__.py
│   ├── location_service.py      # Offline map & location handling
│   ├── route_planner.py         # Multi-stop route optimization
│   └── notification_service.py  # Alert system
├── models/
│   ├── __init__.py
│   ├── user.py                  # User model
│   ├── ride.py                  # Ride model
│   └── location.py              # Location model
├── api/
│   ├── __init__.py
│   └── routes.py                # API endpoints (Flask/FastAPI)
├── tests/
│   ├── __init__.py
│   ├── test_fare_calculator.py
│   ├── test_midpoint_calculator.py
│   └── test_ride_comparator.py
├── main.py                       # Entry point
└── .gitignore
```

## Installation

```bash
# Clone the repository
git clone https://github.com/bhattaraiaashish375-alt/ride-system-2.git
cd ride-system-2

# Install dependencies
pip install -r requirements.txt
```

## Usage

### 1. Calculate Fare
```python
from core.fare_calculator import FareCalculator

calc = FareCalculator()
fare = calc.calculate_fare(
    distance_km=5.5,
    time_period='morning',  # morning, day, evening, night
    vehicle_type='bike'      # bike, car
)
print(f"Fare: Rs. {fare}")
```

### 2. Find Midpoint
```python
from core.midpoint_calculator import MidpointCalculator

calc = MidpointCalculator()
midpoint = calc.calculate_midpoint(
    locations=[
        {'lat': 27.7172, 'lng': 85.3240},  # Kathmandu Center
        {'lat': 27.6815, 'lng': 85.3270}   # Patan
    ]
)
print(f"Midpoint: {midpoint}")
```

### 3. Compare Rides
```python
from core.ride_comparator import RideComparator

comparator = RideComparator()
comparison = comparator.compare_fares(
    distance_km=7.0,
    time_period='evening',
    vehicle_type='car'
)
print(comparison)
```

### 4. Check Peak Hours & Surge
```python
from core.peak_hour_detector import PeakHourDetector

detector = PeakHourDetector()
surge_info = detector.get_surge_info(
    current_time='06:30',  # HH:MM format
    base_fare=100
)
print(f"Surge: {surge_info['surge_percentage']}%")
```

## User Stories Implemented

- **S.N. 3**: Ride Cost Estimation
- **S.N. 10**: Fare Drop Alert
- **S.N. 20**: Peak Hour Fare Warning
- **S.N. 25**: Multi-Stop Route Planning
- **S.N. 26**: Friend Availability Scheduler

## Fare Structure (Kathmandu Valley)

### Bike
- Base: Rs. 30
- Per km: Rs. 18
- Morning (6-9 AM): +35% surge
- Day (9 AM-4 PM): No surge
- Evening (4-9 PM): +40% surge
- Night (9 PM-6 AM): +15% surge

### Car
- Base: Rs. 100
- Per km: Rs. 42
- Morning (6-9 AM): +30% surge
- Day (9 AM-4 PM): No surge
- Evening (4-9 PM): +35% surge
- Night (9 PM-6 AM): +20% surge

## API Endpoints

- `POST /api/calculate-fare` - Calculate ride fare
- `POST /api/find-midpoint` - Calculate midpoint between locations
- `POST /api/compare-rides` - Compare fares across services
- `GET /api/peak-hours` - Get current peak hour info
- `POST /api/plan-route` - Plan multi-stop route
- `GET /api/notifications` - Get fare drop alerts

## Technologies

- **Python 3.8+**
- **Flask/FastAPI** - Web framework
- **Geopy** - Geolocation services
- **Math** - Distance calculations
- **DateTime** - Time-based pricing
- **SQLAlchemy** - Database ORM
- **Pytest** - Testing framework

## Contributing

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Commit changes: `git commit -m 'Add feature'`
3. Push to branch: `git push origin feature/your-feature`
4. Open a pull request

## License

MIT License - See LICENSE file for details

## Author

**Aashish Bhattarai** (bhattaraiaashish375-alt)

---

**Last Updated**: May 2026
