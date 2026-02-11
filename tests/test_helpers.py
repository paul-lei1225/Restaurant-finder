"""
Tests for utility functions.
"""

import unittest
from src.utils.helpers import (
    haversine_distance,
    validate_rating,
    validate_price_range,
    format_distance,
    format_rating
)


class TestHelpers(unittest.TestCase):
    """Test cases for helper functions."""
    
    def test_haversine_distance(self):
        """Test haversine distance calculation."""
        # San Francisco to Los Angeles (approx 347 miles)
        sf_lat, sf_lon = 37.7749, -122.4194
        la_lat, la_lon = 34.0522, -118.2437
        
        distance = haversine_distance(sf_lat, sf_lon, la_lat, la_lon)
        
        # Should be approximately 347 miles
        self.assertGreater(distance, 340)
        self.assertLess(distance, 360)
    
    def test_haversine_distance_same_point(self):
        """Test distance between same point is zero."""
        lat, lon = 37.7749, -122.4194
        
        distance = haversine_distance(lat, lon, lat, lon)
        
        self.assertAlmostEqual(distance, 0.0, places=5)
    
    def test_validate_rating_valid(self):
        """Test rating validation with valid values."""
        self.assertTrue(validate_rating(0.0))
        self.assertTrue(validate_rating(3.5))
        self.assertTrue(validate_rating(5.0))
    
    def test_validate_rating_invalid(self):
        """Test rating validation with invalid values."""
        self.assertFalse(validate_rating(-1.0))
        self.assertFalse(validate_rating(5.5))
        self.assertFalse(validate_rating(10.0))
    
    def test_validate_price_range_valid(self):
        """Test price range validation with valid values."""
        self.assertTrue(validate_price_range('$'))
        self.assertTrue(validate_price_range('$$'))
        self.assertTrue(validate_price_range('$$$'))
        self.assertTrue(validate_price_range('$$$$'))
    
    def test_validate_price_range_invalid(self):
        """Test price range validation with invalid values."""
        self.assertFalse(validate_price_range(''))
        self.assertFalse(validate_price_range('$$$$$'))
        self.assertFalse(validate_price_range('cheap'))
    
    def test_format_distance(self):
        """Test distance formatting."""
        self.assertEqual(format_distance(1.234), "1.2 mi")
        self.assertEqual(format_distance(10.0), "10.0 mi")
        self.assertEqual(format_distance(0.5), "0.5 mi")
    
    def test_format_rating(self):
        """Test rating formatting."""
        self.assertEqual(format_rating(4.5), "4.5★")
        self.assertEqual(format_rating(3.0), "3.0★")
        self.assertEqual(format_rating(5.0), "5.0★")


if __name__ == '__main__':
    unittest.main()
