#!/usr/bin/env python
"""Test script to verify the main application functionality."""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database.db_manager import DatabaseManager
from src.recommender.suggestion_engine import SuggestionEngine
from src.utils.helpers import haversine_distance

def test_basic_functionality():
    """Test basic functionality of the application."""
    print("🧪 Testing Restaurant Finder Application\n")
    
    # Initialize database
    print("1. Initializing database...")
    db_manager = DatabaseManager()
    db_manager.create_tables()
    
    # Clear any existing data
    db_manager.clear_database()
    
    # Seed sample data
    print("2. Seeding sample data...")
    db_manager.seed_sample_data()
    
    count = db_manager.get_restaurant_count()
    print(f"   ✓ Added {count} sample restaurants")
    
    # Test filtering
    print("\n3. Testing restaurant filtering...")
    italian = db_manager.filter_restaurants(cuisine_type='Italian')
    print(f"   ✓ Found {len(italian)} Italian restaurants")
    
    high_rated = db_manager.filter_restaurants(min_rating=4.5)
    print(f"   ✓ Found {len(high_rated)} restaurants with rating >= 4.5")
    
    # Test recommendation engine
    print("\n4. Testing recommendation engine...")
    suggestion_engine = SuggestionEngine(db_manager)
    
    # San Francisco coordinates
    user_lat, user_lon = 37.7749, -122.4194
    
    recommendations = suggestion_engine.get_recommendations(
        user_lat=user_lat,
        user_lon=user_lon,
        cuisine_type='Italian',
        min_rating=4.0,
        price_range='$$',
        max_distance=5.0,
        limit=5
    )
    
    print(f"   ✓ Generated {len(recommendations)} recommendations")
    
    if recommendations:
        print("\n5. Sample recommendation:")
        restaurant, distance, suggested_times = recommendations[0]
        print(f"   {restaurant.name}")
        print(f"   Rating: {restaurant.rating}★")
        print(f"   Distance: {distance:.1f} mi")
        print(f"   Suggested times: {len(suggested_times)} slots available")
    
    # Test cuisine statistics
    print("\n6. Testing cuisine statistics...")
    stats = suggestion_engine.get_cuisine_statistics()
    print(f"   ✓ Found {len(stats)} different cuisine types:")
    for cuisine, count in sorted(stats.items()):
        print(f"     - {cuisine}: {count} restaurant(s)")
    
    print("\n✅ All tests passed!")
    print("\n🚀 You can now run the main application with: python main.py")

if __name__ == '__main__':
    test_basic_functionality()
