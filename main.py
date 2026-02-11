"""
Main CLI application for Restaurant Finder & Reservation Suggester.
"""

import sys
import logging
from datetime import datetime

from config.settings import APP_CONFIG, DEFAULT_PREFERENCES
from src.database.db_manager import DatabaseManager
from src.recommender.suggestion_engine import SuggestionEngine
from src.scrapers.yelp_scraper import YelpScraper
from src.scrapers.google_maps_scraper import GoogleMapsScraper
from src.utils.helpers import (
    print_header, print_separator, get_user_input,
    geocode_address, setup_logger
)

logger = setup_logger(__name__)


class RestaurantFinderApp:
    """Main application class for Restaurant Finder."""
    
    def __init__(self):
        """Initialize the application."""
        self.db_manager = DatabaseManager()
        self.suggestion_engine = SuggestionEngine(self.db_manager)
        self.yelp_scraper = YelpScraper()
        self.google_scraper = GoogleMapsScraper()
        
        # Initialize database
        self.db_manager.create_tables()
        
        # Add sample data if database is empty
        if self.db_manager.get_restaurant_count() == 0:
            print("\n🔄 Initializing database with sample data...")
            self.db_manager.seed_sample_data()
            print("✓ Sample data loaded successfully!")
        
        logger.info("RestaurantFinderApp initialized")
    
    def display_menu(self):
        """Display the main menu."""
        print_header(APP_CONFIG['app_name'])
        print("1. Scrape restaurants in a location")
        print("2. Update availability data")
        print("3. Get restaurant recommendations")
        print("4. Search by cuisine type")
        print("5. View all saved restaurants")
        print("6. Clear database")
        print("7. Exit")
        print_separator()
    
    def scrape_restaurants(self):
        """Scrape restaurants from web sources."""
        print_header("Scrape Restaurants")
        
        print("⚠️  IMPORTANT LEGAL NOTICE:")
        print("This feature is for EDUCATIONAL PURPOSES ONLY.")
        print("For production use, please use official APIs:")
        print("  - Yelp Fusion API: https://www.yelp.com/developers")
        print("  - Google Places API: https://developers.google.com/maps/documentation/places")
        print()
        
        location = get_user_input("Enter location (e.g., 'San Francisco, CA'): ")
        cuisine = get_user_input("Enter cuisine type (or 'any'): ", allow_empty=True)
        
        if not cuisine:
            cuisine = 'any'
        
        print("\n🔄 This is a MOCK scraping operation...")
        print("⚠️  No actual web scraping is performed.")
        print("⚠️  Use official APIs (Yelp Fusion, Google Places) for real data.")
        print("\nFor demo purposes, use the sample data already loaded (option 5).")
        
        input("\nPress Enter to continue...")
    
    def update_availability(self):
        """Update availability data for restaurants."""
        print_header("Update Availability Data")
        
        restaurants = self.db_manager.get_all_restaurants()
        
        if not restaurants:
            print("No restaurants in database. Please add restaurants first.")
            input("\nPress Enter to continue...")
            return
        
        print(f"Found {len(restaurants)} restaurants.")
        print("\n🔄 Updating availability data...")
        print("⚠️  This is a MOCK update using estimated times.")
        print("⚠️  Use official reservation APIs for real availability data.")
        
        # Mock update - in production, this would query real reservation systems
        from config.settings import TIME_SLOTS
        today = datetime.now().date().isoformat()
        
        updated_count = 0
        for restaurant in restaurants[:5]:  # Update first 5 for demo
            # Add mock availability
            for i, time_slot in enumerate(TIME_SLOTS):
                if i % 3 == 0:  # Add every third time slot
                    time_data = {
                        'restaurant_id': restaurant.id,
                        'date': today,
                        'time_slot': time_slot,
                        'party_size': 2,
                        'source': 'estimated',
                        'checked_at': datetime.utcnow()
                    }
                    self.db_manager.add_available_time(time_data)
            updated_count += 1
        
        print(f"\n✓ Updated availability for {updated_count} restaurants")
        input("\nPress Enter to continue...")
    
    def get_recommendations(self):
        """Get restaurant recommendations based on preferences."""
        print_header("Get Restaurant Recommendations")
        
        # Get user preferences
        location = get_user_input("Enter your location: ", allow_empty=True)
        if not location:
            location = APP_CONFIG['default_location']
        
        # Geocode location (mock)
        user_coords = geocode_address(location)
        if not user_coords:
            print("Error geocoding location. Using default San Francisco coordinates.")
            user_coords = (37.7749, -122.4194)
        
        user_lat, user_lon = user_coords
        
        # Get cuisine preference
        print("\nAvailable cuisines:")
        cuisine_stats = self.suggestion_engine.get_cuisine_statistics()
        for i, (cuisine, count) in enumerate(cuisine_stats.items(), 1):
            print(f"  {i}. {cuisine} ({count})")
        
        cuisine = get_user_input("\nEnter preferred cuisine (or 'any'): ", allow_empty=True)
        if not cuisine:
            cuisine = 'any'
        
        # Get rating preference
        min_rating_str = get_user_input("Enter minimum rating (1-5): ", allow_empty=True)
        if min_rating_str:
            try:
                min_rating = float(min_rating_str)
                if not (1.0 <= min_rating <= 5.0):
                    min_rating = DEFAULT_PREFERENCES['min_rating']
            except ValueError:
                min_rating = DEFAULT_PREFERENCES['min_rating']
        else:
            min_rating = DEFAULT_PREFERENCES['min_rating']
        
        # Get price range preference
        price_range = get_user_input("Enter price range ($ - $$$$, or leave empty): ", allow_empty=True)
        if price_range and price_range not in ['$', '$$', '$$$', '$$$$']:
            print("Invalid price range. Ignoring filter.")
            price_range = None
        
        # Get distance preference
        max_distance_str = get_user_input("Enter max distance in miles: ", allow_empty=True)
        if max_distance_str:
            try:
                max_distance = float(max_distance_str)
            except ValueError:
                max_distance = DEFAULT_PREFERENCES['max_distance_miles']
        else:
            max_distance = DEFAULT_PREFERENCES['max_distance_miles']
        
        print("\n🔍 Searching for restaurants...")
        
        # Get recommendations
        recommendations = self.suggestion_engine.get_recommendations(
            user_lat=user_lat,
            user_lon=user_lon,
            cuisine_type=cuisine if cuisine.lower() != 'any' else None,
            min_rating=min_rating,
            price_range=price_range,
            max_distance=max_distance,
            limit=10
        )
        
        if not recommendations:
            print("\n❌ No restaurants found matching your criteria.")
            print("Try adjusting your preferences (lower rating, higher distance, etc.)")
        else:
            print(f"\n✓ Found {len(recommendations)} recommendations:\n")
            print_separator(70)
            
            for i, (restaurant, distance, suggested_times) in enumerate(recommendations, 1):
                print(f"\n{i}. {self.suggestion_engine.format_recommendation(restaurant, distance, suggested_times)}")
                print_separator(70)
        
        input("\nPress Enter to continue...")
    
    def search_by_cuisine(self):
        """Search restaurants by cuisine type."""
        print_header("Search by Cuisine Type")
        
        # Show available cuisines
        cuisine_stats = self.suggestion_engine.get_cuisine_statistics()
        
        if not cuisine_stats:
            print("No restaurants in database.")
            input("\nPress Enter to continue...")
            return
        
        print("Available cuisines:")
        cuisines = list(cuisine_stats.keys())
        for i, cuisine in enumerate(cuisines, 1):
            print(f"  {i}. {cuisine} ({cuisine_stats[cuisine]} restaurants)")
        
        choice = get_user_input("\nEnter cuisine number or name: ")
        
        # Try to parse as number first
        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(cuisines):
                cuisine = cuisines[choice_num - 1]
            else:
                cuisine = choice
        except ValueError:
            cuisine = choice
        
        # Search for restaurants
        restaurants = self.db_manager.filter_restaurants(cuisine_type=cuisine)
        
        if not restaurants:
            print(f"\n❌ No restaurants found for cuisine: {cuisine}")
        else:
            print(f"\n✓ Found {len(restaurants)} {cuisine} restaurants:\n")
            print_separator(70)
            
            for i, restaurant in enumerate(restaurants, 1):
                print(f"\n{i}. ⭐ {restaurant.name} - {restaurant.rating:.1f}★ - {restaurant.price_range}")
                print(f"   📍 {restaurant.address}")
                print(f"   📞 {restaurant.phone}")
                if restaurant.hours:
                    print(f"   🕒 {restaurant.hours}")
                print_separator(70)
        
        input("\nPress Enter to continue...")
    
    def view_all_restaurants(self):
        """View all saved restaurants."""
        print_header("All Saved Restaurants")
        
        restaurants = self.db_manager.get_all_restaurants()
        
        if not restaurants:
            print("No restaurants in database.")
        else:
            print(f"Total restaurants: {len(restaurants)}\n")
            print_separator(70)
            
            for i, restaurant in enumerate(restaurants, 1):
                print(f"\n{i}. ⭐ {restaurant.name} - {restaurant.rating:.1f}★ - {restaurant.price_range}")
                print(f"   🍽️  {restaurant.cuisine_type}")
                print(f"   📍 {restaurant.address}")
                print(f"   📞 {restaurant.phone}")
                if restaurant.website:
                    print(f"   🌐 {restaurant.website}")
                if restaurant.hours:
                    print(f"   🕒 {restaurant.hours}")
                print_separator(70)
        
        input("\nPress Enter to continue...")
    
    def clear_database(self):
        """Clear all data from the database."""
        print_header("Clear Database")
        
        print("⚠️  WARNING: This will delete all restaurant and availability data!")
        confirm = get_user_input("Are you sure? (yes/no): ")
        
        if confirm.lower() in ['yes', 'y']:
            if self.db_manager.clear_database():
                print("\n✓ Database cleared successfully!")
            else:
                print("\n❌ Error clearing database.")
        else:
            print("\n✗ Operation cancelled.")
        
        input("\nPress Enter to continue...")
    
    def run(self):
        """Run the main application loop."""
        print(f"\n🍽️  Welcome to {APP_CONFIG['app_name']} v{APP_CONFIG['version']}")
        
        while True:
            try:
                self.display_menu()
                
                choice = get_user_input("Enter your choice (1-7): ", 
                                       input_type='int')
                
                if choice == 1:
                    self.scrape_restaurants()
                elif choice == 2:
                    self.update_availability()
                elif choice == 3:
                    self.get_recommendations()
                elif choice == 4:
                    self.search_by_cuisine()
                elif choice == 5:
                    self.view_all_restaurants()
                elif choice == 6:
                    self.clear_database()
                elif choice == 7:
                    print("\n👋 Thank you for using Restaurant Finder!")
                    print("For production use, remember to use official APIs:")
                    print("  - Yelp Fusion API")
                    print("  - Google Places API")
                    print("  - OpenTable/Resy APIs for reservations")
                    sys.exit(0)
                else:
                    print("\n❌ Invalid choice. Please enter a number between 1 and 7.")
                    input("\nPress Enter to continue...")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                sys.exit(0)
            except Exception as e:
                logger.error(f"Error in main loop: {e}", exc_info=True)
                print(f"\n❌ An error occurred: {e}")
                input("\nPress Enter to continue...")


def main():
    """Main entry point for the application."""
    try:
        app = RestaurantFinderApp()
        app.run()
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
