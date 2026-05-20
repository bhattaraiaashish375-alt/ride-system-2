"""Pre-defined Locations Database for Kathmandu Valley"""

LOCATIONS_DB = {
    # Kathmandu City Center
    'kathmandu_center': {'lat': 27.7172, 'lng': 85.3240, 'name': 'Kathmandu City Center', 'area': 'Kathmandu'},
    'thamel': {'lat': 27.7220, 'lng': 85.4267, 'name': 'Thamel', 'area': 'Kathmandu'},
    'garden_of_dreams': {'lat': 27.7174, 'lng': 85.3145, 'name': 'Garden of Dreams', 'area': 'Kathmandu'},
    'durbar_square': {'lat': 27.7172, 'lng': 85.3240, 'name': 'Basantapur Durbar Square', 'area': 'Kathmandu'},
    'pashupatinath': {'lat': 27.7303, 'lng': 85.3382, 'name': 'Pashupatinath Temple Area', 'area': 'Kathmandu'},
    'boudhanath': {'lat': 27.7209, 'lng': 85.3645, 'name': 'Boudhanath Stupa', 'area': 'Kathmandu'},
    'swayambhunath': {'lat': 27.7107, 'lng': 85.2885, 'name': 'Swayambhunath Area', 'area': 'Kathmandu'},
    'budhanilkantha': {'lat': 27.8033, 'lng': 85.3226, 'name': 'Budhanilkantha Temple Area', 'area': 'Kathmandu'},
    'chobhar_hills': {'lat': 27.6872, 'lng': 85.2657, 'name': 'Chobhar Hills', 'area': 'Kathmandu'},
    'balaju_park': {'lat': 27.7649, 'lng': 85.3059, 'name': 'Balaju Park', 'area': 'Kathmandu'},
    
    # Patan (Lalitpur)
    'patan_center': {'lat': 27.6815, 'lng': 85.3270, 'name': 'Patan City Center', 'area': 'Lalitpur'},
    'patan_durbar_square': {'lat': 27.6789, 'lng': 85.3289, 'name': 'Patan Durbar Square', 'area': 'Lalitpur'},
    'central_zoo': {'lat': 27.6733, 'lng': 85.3384, 'name': 'Central Zoo Jawalakhel', 'area': 'Lalitpur'},
    'jhamsikhel': {'lat': 27.6747, 'lng': 85.3250, 'name': 'Jhamsikhel', 'area': 'Lalitpur'},
    'satdobato': {'lat': 27.6520, 'lng': 85.3456, 'name': 'Satdobato', 'area': 'Lalitpur'},
    'godawari': {'lat': 27.6088, 'lng': 85.4031, 'name': 'Godawari Botanical Garden', 'area': 'Lalitpur'},
    
    # Bhaktapur
    'bhaktapur_center': {'lat': 27.6733, 'lng': 85.8289, 'name': 'Bhaktapur City Center', 'area': 'Bhaktapur'},
    'bhaktapur_durbar': {'lat': 27.6731, 'lng': 85.8292, 'name': 'Bhaktapur Durbar Square', 'area': 'Bhaktapur'},
    'nagarkot': {'lat': 27.6156, 'lng': 85.5250, 'name': 'Nagarkot', 'area': 'Bhaktapur'},
    'changu_narayan': {'lat': 27.6844, 'lng': 85.4819, 'name': 'Changu Narayan', 'area': 'Bhaktapur'},
    'thimi': {'lat': 27.6589, 'lng': 85.5289, 'name': 'Thimi', 'area': 'Bhaktapur'},
}

def get_location(location_key):
    """Get location by key"""
    return LOCATIONS_DB.get(location_key, None)

def get_all_locations():
    """Get all available locations"""
    return LOCATIONS_DB

def search_locations(search_term):
    """Search locations by name or area"""
    results = []
    search_lower = search_term.lower()
    
    for key, loc in LOCATIONS_DB.items():
        if (search_lower in loc['name'].lower() or 
            search_lower in loc['area'].lower()):
            results.append({**loc, 'key': key})
    
    return results
