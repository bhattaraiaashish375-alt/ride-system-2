"""Midpoint Calculator for Fair Meeting Locations"""

import math
from typing import List, Dict, Tuple


class MidpointCalculator:
    """Calculate geographic midpoint between multiple locations"""
    
    # Earth's radius in kilometers
    EARTH_RADIUS_KM = 6371.0
    
    def __init__(self):
        pass
    
    def haversine_distance(self, lat1, lng1, lat2, lng2):
        """Calculate distance between two points using Haversine formula
        
        Args:
            lat1, lng1: First point coordinates
            lat2, lng2: Second point coordinates
            
        Returns:
            float: Distance in kilometers
        """
        # Convert to radians
        lat1_rad = math.radians(lat1)
        lng1_rad = math.radians(lng1)
        lat2_rad = math.radians(lat2)
        lng2_rad = math.radians(lng2)
        
        # Differences
        dlat = lat2_rad - lat1_rad
        dlng = lng2_rad - lng1_rad
        
        # Haversine formula
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlng / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = self.EARTH_RADIUS_KM * c
        
        return distance
    
    def calculate_midpoint(self, locations: List[Dict]):
        """Calculate geographic midpoint for multiple locations
        
        Args:
            locations: List of dicts with 'lat' and 'lng' keys
                      Example: [{'lat': 27.7172, 'lng': 85.3240}, ...]
        
        Returns:
            dict: {'lat': float, 'lng': float, 'location_count': int}
        """
        if not locations or len(locations) == 0:
            raise ValueError("At least one location is required")
        
        if len(locations) == 1:
            return {
                'lat': locations[0]['lat'],
                'lng': locations[0]['lng'],
                'location_count': 1,
                'midpoint_type': 'single_location'
            }
        
        # Convert to Cartesian coordinates
        x_sum = 0.0
        y_sum = 0.0
        z_sum = 0.0
        
        for loc in locations:
            lat_rad = math.radians(loc['lat'])
            lng_rad = math.radians(loc['lng'])
            
            x_sum += math.cos(lat_rad) * math.cos(lng_rad)
            y_sum += math.cos(lat_rad) * math.sin(lng_rad)
            z_sum += math.sin(lat_rad)
        
        n = len(locations)
        x_avg = x_sum / n
        y_avg = y_sum / n
        z_avg = z_sum / n
        
        # Convert back to lat/lng
        midpoint_lat = math.degrees(math.atan2(z_avg, math.sqrt(x_avg**2 + y_avg**2)))
        midpoint_lng = math.degrees(math.atan2(y_avg, x_avg))
        
        return {
            'lat': round(midpoint_lat, 6),
            'lng': round(midpoint_lng, 6),
            'location_count': len(locations),
            'midpoint_type': 'geographic_center'
        }
    
    def calculate_travel_distances(self, locations: List[Dict], midpoint: Dict):
        """Calculate travel distances from each location to midpoint
        
        Args:
            locations: List of starting locations
            midpoint: Midpoint coordinates
            
        Returns:
            list: Distances from each location to midpoint
        """
        distances = []
        
        for loc in locations:
            distance = self.haversine_distance(
                loc['lat'], loc['lng'],
                midpoint['lat'], midpoint['lng']
            )
            distances.append({
                'location': loc.get('name', f"Lat: {loc['lat']}, Lng: {loc['lng']}"),
                'distance_km': round(distance, 2)
            })
        
        return distances
    
    def calculate_total_travel(self, locations: List[Dict], midpoint: Dict):
        """Calculate total travel distance for all users to reach midpoint
        
        Args:
            locations: List of starting locations
            midpoint: Midpoint coordinates
            
        Returns:
            dict: Total and average travel distances
        """
        distances = self.calculate_travel_distances(locations, midpoint)
        distance_values = [d['distance_km'] for d in distances]
        
        total_distance = sum(distance_values)
        avg_distance = total_distance / len(distance_values) if distance_values else 0
        max_distance = max(distance_values) if distance_values else 0
        min_distance = min(distance_values) if distance_values else 0
        
        return {
            'distances': distances,
            'total_distance_km': round(total_distance, 2),
            'average_distance_km': round(avg_distance, 2),
            'max_distance_km': round(max_distance, 2),
            'min_distance_km': round(min_distance, 2),
            'fairness_score': round((max_distance - min_distance) / avg_distance * 100, 2) if avg_distance > 0 else 0
        }
