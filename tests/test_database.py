"""
Tests for database operations.
"""

import unittest
import tempfile
import os
from datetime import datetime

from src.database.db_manager import DatabaseManager
from src.database.models import Restaurant, AvailableTime


class TestDatabaseManager(unittest.TestCase):
    """Test cases for DatabaseManager."""
    
    def setUp(self):
        """Set up test database."""
        # Create temporary database
        self.temp_db = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.db')
        self.temp_db.close()
        
        db_url = f"sqlite:///{self.temp_db.name}"
        self.db_manager = DatabaseManager(database_url=db_url)
        self.db_manager.create_tables()
    
    def tearDown(self):
        """Clean up test database."""
        # Remove temporary database file
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)
    
    def test_add_restaurant(self):
        """Test adding a restaurant."""
        restaurant_data = {
            'name': 'Test Restaurant',
            'cuisine_type': 'Italian',
            'rating': 4.5,
            'price_range': '$$',
            'address': '123 Test St, San Francisco, CA',
            'phone': '(415) 555-0123',
            'latitude': 37.7749,
            'longitude': -122.4194,
            'website': 'http://test.com',
            'hours': 'Mon-Sun: 11:00 AM - 10:00 PM'
        }
        
        restaurant = self.db_manager.add_restaurant(restaurant_data)
        
        self.assertIsNotNone(restaurant)
        self.assertEqual(restaurant.name, 'Test Restaurant')
        self.assertEqual(restaurant.cuisine_type, 'Italian')
        self.assertEqual(restaurant.rating, 4.5)
    
    def test_get_restaurant_by_id(self):
        """Test retrieving a restaurant by ID."""
        # Add a restaurant first
        restaurant_data = {
            'name': 'Test Restaurant',
            'cuisine_type': 'Italian',
            'rating': 4.5,
            'price_range': '$$',
            'address': '123 Test St',
            'latitude': 37.7749,
            'longitude': -122.4194
        }
        
        added = self.db_manager.add_restaurant(restaurant_data)
        
        # Retrieve it
        retrieved = self.db_manager.get_restaurant_by_id(added.id)
        
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.name, 'Test Restaurant')
    
    def test_filter_restaurants_by_cuisine(self):
        """Test filtering restaurants by cuisine."""
        # Add multiple restaurants
        restaurants = [
            {
                'name': 'Italian Place',
                'cuisine_type': 'Italian',
                'rating': 4.5,
                'price_range': '$$',
                'address': '123 Test St',
                'latitude': 37.7749,
                'longitude': -122.4194
            },
            {
                'name': 'Japanese Place',
                'cuisine_type': 'Japanese',
                'rating': 4.3,
                'price_range': '$$$',
                'address': '456 Test St',
                'latitude': 37.7849,
                'longitude': -122.4094
            }
        ]
        
        for r in restaurants:
            self.db_manager.add_restaurant(r)
        
        # Filter by cuisine
        italian = self.db_manager.filter_restaurants(cuisine_type='Italian')
        
        self.assertEqual(len(italian), 1)
        self.assertEqual(italian[0].cuisine_type, 'Italian')
    
    def test_filter_restaurants_by_rating(self):
        """Test filtering restaurants by minimum rating."""
        # Add restaurants with different ratings
        restaurants = [
            {
                'name': 'High Rated',
                'cuisine_type': 'Italian',
                'rating': 4.8,
                'price_range': '$$',
                'address': '123 Test St',
                'latitude': 37.7749,
                'longitude': -122.4194
            },
            {
                'name': 'Low Rated',
                'cuisine_type': 'Italian',
                'rating': 3.2,
                'price_range': '$$',
                'address': '456 Test St',
                'latitude': 37.7849,
                'longitude': -122.4094
            }
        ]
        
        for r in restaurants:
            self.db_manager.add_restaurant(r)
        
        # Filter by rating
        high_rated = self.db_manager.filter_restaurants(min_rating=4.0)
        
        self.assertEqual(len(high_rated), 1)
        self.assertEqual(high_rated[0].name, 'High Rated')
    
    def test_add_available_time(self):
        """Test adding an available time slot."""
        # Add a restaurant first
        restaurant_data = {
            'name': 'Test Restaurant',
            'cuisine_type': 'Italian',
            'rating': 4.5,
            'price_range': '$$',
            'address': '123 Test St',
            'latitude': 37.7749,
            'longitude': -122.4194
        }
        
        restaurant = self.db_manager.add_restaurant(restaurant_data)
        
        # Add available time
        time_data = {
            'restaurant_id': restaurant.id,
            'date': '2024-03-15',
            'time_slot': '7:00 PM',
            'party_size': 2,
            'source': 'test'
        }
        
        available_time = self.db_manager.add_available_time(time_data)
        
        self.assertIsNotNone(available_time)
        self.assertEqual(available_time.restaurant_id, restaurant.id)
        self.assertEqual(available_time.time_slot, '7:00 PM')
    
    def test_clear_database(self):
        """Test clearing the database."""
        # Add some data
        restaurant_data = {
            'name': 'Test Restaurant',
            'cuisine_type': 'Italian',
            'rating': 4.5,
            'price_range': '$$',
            'address': '123 Test St',
            'latitude': 37.7749,
            'longitude': -122.4194
        }
        
        self.db_manager.add_restaurant(restaurant_data)
        
        # Clear database
        self.assertTrue(self.db_manager.clear_database())
        
        # Verify it's empty
        count = self.db_manager.get_restaurant_count()
        self.assertEqual(count, 0)


if __name__ == '__main__':
    unittest.main()
