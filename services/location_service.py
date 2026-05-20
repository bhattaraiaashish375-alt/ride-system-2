"""Location Service for Offline Map Support"""

from config.locations import LOCATIONS_DB, get_location, search_locations
from core.midpoint_calculator import MidpointCalculator


class LocationService:
    """Handle location operations with offline map support"""
    
    def __init__(self):
        self.midpoint_calc = MidpointCalculator()
        self.locations_db = LOCATIONS_DB
    
    def get_nearby_locations(self, lat, lng, radius_km=5):
        """Find locations near a point
        
        Args:
            lat: float - Latitude
            lng: float - Longitude
            radius_km: float - Search radius in kilometers
            
        Returns:
            list: Nearby locations within radius
        """
        nearby = []
        
        for key, location in self.locations_db.items():
            distance = self.midpoint_calc.haversine_distance(
                lat, lng,
                location['lat'], location['lng']
            )
            
            if distance <= radius_km:
                nearby.append({
                    'key': key,
                    'name': location['name'],
                    'area': location['area'],
                    'lat': location['lat'],
                    'lng': location['lng'],
                    'distance_km': round(distance, 2)
                })
        
        # Sort by distance
        nearby.sort(key=lambda x: x['distance_km'])
        return nearby
    
    def search_location(self, search_term):
        """Search for locations by name or area
        
        Args:
            search_term: str - Search query
            
        Returns:
            list: Matching locations
        """
        return search_locations(search_term)
    
    def get_location_details(self, location_key):
        """Get detailed information about a location
        
        Args:
            location_key: str - Location identifier
            
        Returns:
            dict: Location details or None
        """
        location = get_location(location_key)
        if location:
            return {**location, 'key': location_key}
        return None
    
    def calculate_distances_between_locations(self, location_keys):
        """Calculate pairwise distances between locations
        
        Args:
            location_keys: list - Location identifiers
            
        Returns:
            dict: Distance matrix
        """
        locations = []
        valid_keys = []
        
        for key in location_keys:
            loc = get_location(key)
            if loc:
                locations.append(loc)
                valid_keys.append(key)
        
        if len(locations) < 2:
            return {'error': 'At least 2 valid locations required'}
        
        distances = {}
        for i, key1 in enumerate(valid_keys):
            distances[key1] = {}
            for j, key2 in enumerate(valid_keys):
                if i != j:
                    distance = self.midpoint_calc.haversine_distance(
                        locations[i]['lat'], locations[i]['lng'],
                        locations[j]['lat'], locations[j]['lng']
                    )
                    distances[key1][key2] = round(distance, 2)
        
        return distances
