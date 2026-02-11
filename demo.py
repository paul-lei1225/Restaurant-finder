#!/usr/bin/env python
"""
Demo script to showcase the Restaurant Finder application.
This simulates running the app and viewing restaurants.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database.db_manager import DatabaseManager
from src.recommender.suggestion_engine import SuggestionEngine

def demo_restaurant_finder():
    """Demonstrate the Restaurant Finder application."""
    
    print("\n" + "="*60)
    print("🍽️  Restaurant Finder & Reservation Suggester - DEMO".center(60))
    print("="*60)
    
    # Initialize
    print("\n[Initializing application...]")
    db_manager = DatabaseManager()
    db_manager.create_tables()
    
    # Check if database is empty and seed if needed
    if db_manager.get_restaurant_count() == 0:
        print("Loading sample restaurant data...")
        db_manager.seed_sample_data()
    
    suggestion_engine = SuggestionEngine(db_manager)
    
    # Demo 1: View all restaurants
    print("\n" + "="*60)
    print("📋 All Available Restaurants".center(60))
    print("="*60 + "\n")
    
    restaurants = db_manager.get_all_restaurants()
    for i, restaurant in enumerate(restaurants[:5], 1):  # Show first 5
        print(f"{i}. ⭐ {restaurant.name} - {restaurant.rating:.1f}★ - {restaurant.price_range}")
        print(f"   🍽️  {restaurant.cuisine_type}")
        print(f"   📍 {restaurant.address}")
        print(f"   📞 {restaurant.phone}")
        print()
    
    print(f"... and {len(restaurants) - 5} more restaurants\n")
    
    # Demo 2: Get Italian restaurant recommendations
    print("="*60)
    print("🎯 Getting Italian Restaurant Recommendations".center(60))
    print("="*60)
    print("\nFilters:")
    print("  • Location: San Francisco, CA")
    print("  • Cuisine: Italian")
    print("  • Minimum Rating: 4.0")
    print("  • Price Range: $$")
    print("  • Max Distance: 5 miles")
    print("\n🔍 Searching...")
    
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
    
    if recommendations:
        print(f"\n✓ Found {len(recommendations)} recommendations:\n")
        print("-"*60)
        
        for i, (restaurant, distance, suggested_times) in enumerate(recommendations, 1):
            print(f"\n{i}. {suggestion_engine.format_recommendation(restaurant, distance, suggested_times)}")
            print("-"*60)
    else:
        print("\n❌ No restaurants found matching criteria.")
    
    # Demo 3: Show cuisine statistics
    print("\n" + "="*60)
    print("📊 Available Cuisine Types".center(60))
    print("="*60 + "\n")
    
    stats = suggestion_engine.get_cuisine_statistics()
    cuisine_list = sorted(stats.items(), key=lambda x: x[1], reverse=True)
    
    for cuisine, count in cuisine_list:
        bar = "█" * count
        print(f"  {cuisine:15s} {bar} ({count})")
    
    print("\n" + "="*60)
    print("✅ Demo Complete!".center(60))
    print("="*60)
    print("\n💡 To run the interactive application, use: python main.py")
    print("\n📚 Features:")
    print("  • Search and filter restaurants by preferences")
    print("  • Get personalized recommendations")
    print("  • View suggested reservation times")
    print("  • Manage restaurant database")
    print("\n⚠️  Note: This uses sample data for demonstration.")
    print("   For production, integrate with Yelp Fusion API or Google Places API.\n")

if __name__ == '__main__':
    demo_restaurant_finder()
