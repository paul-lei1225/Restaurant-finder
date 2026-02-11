"""
Configuration settings for the Restaurant Finder application.
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Database configuration
DATABASE_CONFIG = {
    'type': 'sqlite',
    'name': 'restaurant_data.db',
    'path': BASE_DIR / 'restaurant_data.db'
}

# Database URL for SQLAlchemy
DATABASE_URL = f"sqlite:///{DATABASE_CONFIG['path']}"

# Scraping configuration
SCRAPING_CONFIG = {
    'rate_limit_delay': 2.5,  # Seconds between requests
    'timeout': 10,  # Request timeout in seconds
    'max_retries': 3,
    'retry_delay': 5,  # Seconds to wait before retry
    'user_agents': [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    ]
}

# User preferences defaults
DEFAULT_PREFERENCES = {
    'cuisine_types': ['Italian', 'Japanese', 'Mexican', 'American', 'Chinese', 'Thai', 'Indian', 'French'],
    'min_rating': 3.5,
    'max_distance_miles': 10,
    'price_range': ['$', '$$', '$$$', '$$$$']
}

# Logging configuration
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'date_format': '%Y-%m-%d %H:%M:%S'
}

# API Keys (load from environment variables)
API_KEYS = {
    'yelp_api_key': os.getenv('YELP_API_KEY', ''),
    'google_maps_api_key': os.getenv('GOOGLE_MAPS_API_KEY', ''),
}

# Application settings
APP_CONFIG = {
    'app_name': 'Restaurant Finder & Reservation Suggester',
    'version': '1.0.0',
    'default_location': 'San Francisco, CA',
    'default_party_size': 2
}

# Time slots for availability suggestions
TIME_SLOTS = [
    '11:30 AM', '12:00 PM', '12:30 PM', '1:00 PM', '1:30 PM',
    '5:30 PM', '6:00 PM', '6:30 PM', '7:00 PM', '7:30 PM',
    '8:00 PM', '8:30 PM', '9:00 PM', '9:30 PM'
]

# Sample data for demo purposes
SAMPLE_RESTAURANTS = [
    {
        'name': 'Trattoria Romana',
        'cuisine_type': 'Italian',
        'rating': 4.5,
        'price_range': '$$',
        'address': '123 North Beach, San Francisco, CA 94133',
        'phone': '(415) 555-0123',
        'latitude': 37.8003,
        'longitude': -122.4103,
        'website': 'http://trattoriaromana.com',
        'hours': 'Mon-Sun: 11:30 AM - 10:00 PM'
    },
    {
        'name': 'Pasta Milano',
        'cuisine_type': 'Italian',
        'rating': 4.3,
        'price_range': '$$',
        'address': '456 Mission St, San Francisco, CA 94105',
        'phone': '(415) 555-0456',
        'latitude': 37.7899,
        'longitude': -122.3997,
        'website': 'http://pastamilano.com',
        'hours': 'Mon-Sat: 5:00 PM - 10:30 PM'
    },
    {
        'name': 'Sushi Paradise',
        'cuisine_type': 'Japanese',
        'rating': 4.7,
        'price_range': '$$$',
        'address': '789 Geary Blvd, San Francisco, CA 94109',
        'phone': '(415) 555-0789',
        'latitude': 37.7858,
        'longitude': -122.4186,
        'website': 'http://sushiparadise.com',
        'hours': 'Tue-Sun: 5:30 PM - 10:00 PM'
    },
    {
        'name': 'El Toro Loco',
        'cuisine_type': 'Mexican',
        'rating': 4.2,
        'price_range': '$',
        'address': '321 Valencia St, San Francisco, CA 94103',
        'phone': '(415) 555-0321',
        'latitude': 37.7665,
        'longitude': -122.4216,
        'website': 'http://eltoroloco.com',
        'hours': 'Mon-Sun: 11:00 AM - 11:00 PM'
    },
    {
        'name': 'The American Grill',
        'cuisine_type': 'American',
        'rating': 4.0,
        'price_range': '$$',
        'address': '654 Market St, San Francisco, CA 94104',
        'phone': '(415) 555-0654',
        'latitude': 37.7889,
        'longitude': -122.4012,
        'website': 'http://americangrill.com',
        'hours': 'Mon-Sun: 7:00 AM - 10:00 PM'
    },
    {
        'name': 'Dragon Palace',
        'cuisine_type': 'Chinese',
        'rating': 4.4,
        'price_range': '$$',
        'address': '987 Grant Ave, San Francisco, CA 94108',
        'phone': '(415) 555-0987',
        'latitude': 37.7947,
        'longitude': -122.4065,
        'website': 'http://dragonpalace.com',
        'hours': 'Mon-Sun: 11:30 AM - 10:00 PM'
    },
    {
        'name': 'Thai Spice Kitchen',
        'cuisine_type': 'Thai',
        'rating': 4.6,
        'price_range': '$$',
        'address': '147 Polk St, San Francisco, CA 94102',
        'phone': '(415) 555-0147',
        'latitude': 37.7815,
        'longitude': -122.4186,
        'website': 'http://thaispice.com',
        'hours': 'Tue-Sun: 5:00 PM - 9:30 PM'
    },
    {
        'name': 'India Gate',
        'cuisine_type': 'Indian',
        'rating': 4.1,
        'price_range': '$$',
        'address': '258 Powell St, San Francisco, CA 94102',
        'phone': '(415) 555-0258',
        'latitude': 37.7869,
        'longitude': -122.4083,
        'website': 'http://indiagate.com',
        'hours': 'Mon-Sun: 11:30 AM - 10:30 PM'
    },
    {
        'name': 'Le Petit Bistro',
        'cuisine_type': 'French',
        'rating': 4.8,
        'price_range': '$$$$',
        'address': '369 Bush St, San Francisco, CA 94104',
        'phone': '(415) 555-0369',
        'latitude': 37.7909,
        'longitude': -122.4043,
        'website': 'http://lepetitbistro.com',
        'hours': 'Wed-Sun: 6:00 PM - 10:00 PM'
    },
    {
        'name': 'Harbor View Seafood',
        'cuisine_type': 'Seafood',
        'rating': 4.5,
        'price_range': '$$$',
        'address': '741 Embarcadero, San Francisco, CA 94111',
        'phone': '(415) 555-0741',
        'latitude': 37.8010,
        'longitude': -122.3988,
        'website': 'http://harborviewseafood.com',
        'hours': 'Mon-Sun: 11:00 AM - 10:00 PM'
    },
    {
        'name': 'Burger Barn',
        'cuisine_type': 'American',
        'rating': 3.9,
        'price_range': '$',
        'address': '852 Haight St, San Francisco, CA 94117',
        'phone': '(415) 555-0852',
        'latitude': 37.7708,
        'longitude': -122.4434,
        'website': 'http://burgerbarn.com',
        'hours': 'Mon-Sun: 10:00 AM - 11:00 PM'
    },
    {
        'name': 'Mediterranean Delight',
        'cuisine_type': 'Mediterranean',
        'rating': 4.3,
        'price_range': '$$',
        'address': '963 Irving St, San Francisco, CA 94122',
        'phone': '(415) 555-0963',
        'latitude': 37.7638,
        'longitude': -122.4698,
        'website': 'http://meddelight.com',
        'hours': 'Tue-Sun: 11:30 AM - 9:00 PM'
    },
    {
        'name': 'Steakhouse Prime',
        'cuisine_type': 'Steakhouse',
        'rating': 4.7,
        'price_range': '$$$$',
        'address': '159 Pine St, San Francisco, CA 94111',
        'phone': '(415) 555-0159',
        'latitude': 37.7920,
        'longitude': -122.3990,
        'website': 'http://steakhouseprime.com',
        'hours': 'Mon-Sat: 5:00 PM - 11:00 PM'
    },
    {
        'name': 'Veggie Garden',
        'cuisine_type': 'Vegetarian',
        'rating': 4.4,
        'price_range': '$$',
        'address': '753 Divisadero St, San Francisco, CA 94117',
        'phone': '(415) 555-0753',
        'latitude': 37.7753,
        'longitude': -122.4390,
        'website': 'http://veggiegarden.com',
        'hours': 'Mon-Sun: 11:00 AM - 9:00 PM'
    },
    {
        'name': 'Korean BBQ House',
        'cuisine_type': 'Korean',
        'rating': 4.2,
        'price_range': '$$',
        'address': '357 Clement St, San Francisco, CA 94118',
        'phone': '(415) 555-0357',
        'latitude': 37.7825,
        'longitude': -122.4652,
        'website': 'http://koreanbbq.com',
        'hours': 'Mon-Sun: 5:00 PM - 10:30 PM'
    }
]
