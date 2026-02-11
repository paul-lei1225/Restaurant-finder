"""
Utility functions for the Restaurant Finder application.
"""

import math
import logging
import re
from datetime import datetime, timedelta
from typing import Tuple, Optional

# Configure logging
from config.settings import LOGGING_CONFIG

logging.basicConfig(
    level=getattr(logging, LOGGING_CONFIG['level']),
    format=LOGGING_CONFIG['format'],
    datefmt=LOGGING_CONFIG['date_format']
)

logger = logging.getLogger(__name__)


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points on Earth.
    
    Args:
        lat1: Latitude of first point
        lon1: Longitude of first point
        lat2: Latitude of second point
        lon2: Longitude of second point
    
    Returns:
        Distance in miles
    """
    # Convert degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    # Haversine formula
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    
    # Radius of Earth in miles
    radius_miles = 3959.0
    
    return c * radius_miles


def geocode_address(address: str) -> Optional[Tuple[float, float]]:
    """
    Convert an address to latitude and longitude coordinates.
    
    Note: This is a mock implementation. In production, use Google Maps API
    or another geocoding service.
    
    Args:
        address: Street address
    
    Returns:
        Tuple of (latitude, longitude) or None if not found
    """
    # Mock implementation - returns San Francisco coordinates
    # In production, use a real geocoding API
    logger.warning("Using mock geocoding - returning San Francisco coordinates")
    return (37.7749, -122.4194)


def validate_rating(rating: float) -> bool:
    """
    Validate that a rating is within acceptable range.
    
    Args:
        rating: Rating value
    
    Returns:
        True if valid, False otherwise
    """
    return 0.0 <= rating <= 5.0


def validate_price_range(price_range: str) -> bool:
    """
    Validate that a price range is in correct format.
    
    Args:
        price_range: Price range string (e.g., "$", "$$", "$$$", "$$$$")
    
    Returns:
        True if valid, False otherwise
    """
    return price_range in ['$', '$$', '$$$', '$$$$']


def validate_phone_number(phone: str) -> bool:
    """
    Validate phone number format.
    
    Args:
        phone: Phone number string
    
    Returns:
        True if valid, False otherwise
    """
    # Simple validation - accepts various formats
    pattern = r'^[\d\s\-\(\)\.+]+$'
    return bool(re.match(pattern, phone)) and len(re.sub(r'\D', '', phone)) >= 10


def format_distance(distance: float) -> str:
    """
    Format distance for display.
    
    Args:
        distance: Distance in miles
    
    Returns:
        Formatted string
    """
    return f"{distance:.1f} mi"


def format_rating(rating: float) -> str:
    """
    Format rating for display with star symbol.
    
    Args:
        rating: Rating value
    
    Returns:
        Formatted string
    """
    return f"{rating:.1f}★"


def parse_time_string(time_str: str) -> Optional[datetime]:
    """
    Parse a time string into a datetime object.
    
    Args:
        time_str: Time string (e.g., "6:30 PM")
    
    Returns:
        datetime object or None if parsing fails
    """
    try:
        # Try common time formats
        for fmt in ['%I:%M %p', '%H:%M', '%I %p']:
            try:
                time_obj = datetime.strptime(time_str, fmt)
                # Combine with today's date
                today = datetime.now().date()
                return datetime.combine(today, time_obj.time())
            except ValueError:
                continue
        return None
    except Exception as e:
        logger.error(f"Error parsing time string '{time_str}': {e}")
        return None


def get_time_slots_for_date(date: datetime, available_times: list) -> list:
    """
    Get available time slots for a specific date.
    
    Args:
        date: Date to check
        available_times: List of available time strings
    
    Returns:
        List of time slot strings
    """
    # Simple implementation - returns all available times
    return available_times


def format_restaurant_display(restaurant: dict, distance: Optional[float] = None) -> str:
    """
    Format restaurant information for display.
    
    Args:
        restaurant: Restaurant dictionary
        distance: Optional distance from user
    
    Returns:
        Formatted string
    """
    lines = []
    lines.append(f"⭐ {restaurant['name']} - {format_rating(restaurant['rating'])} - {restaurant['price_range']}")
    lines.append(f"   📍 {restaurant['address']}")
    
    if distance:
        lines.append(f"   📏 {format_distance(distance)} away")
    
    lines.append(f"   🍽️  {restaurant['cuisine_type']}")
    
    if restaurant.get('phone'):
        lines.append(f"   📞 {restaurant['phone']}")
    
    if restaurant.get('hours'):
        lines.append(f"   🕒 {restaurant['hours']}")
    
    return '\n'.join(lines)


def get_user_input(prompt: str, input_type: str = 'string', 
                   valid_options: Optional[list] = None,
                   allow_empty: bool = False) -> any:
    """
    Get and validate user input.
    
    Args:
        prompt: Prompt to display
        input_type: Type of input expected ('string', 'int', 'float')
        valid_options: List of valid options (for choice validation)
        allow_empty: Whether to allow empty input
    
    Returns:
        Validated input value
    """
    while True:
        user_input = input(prompt).strip()
        
        if not user_input and allow_empty:
            return None
        
        if not user_input and not allow_empty:
            print("Input cannot be empty. Please try again.")
            continue
        
        if valid_options and user_input not in valid_options:
            print(f"Invalid option. Please choose from: {', '.join(valid_options)}")
            continue
        
        if input_type == 'int':
            try:
                return int(user_input)
            except ValueError:
                print("Please enter a valid integer.")
                continue
        
        if input_type == 'float':
            try:
                return float(user_input)
            except ValueError:
                print("Please enter a valid number.")
                continue
        
        return user_input


def print_header(text: str, width: int = 60):
    """
    Print a formatted header.
    
    Args:
        text: Header text
        width: Width of header
    """
    print("\n" + "=" * width)
    print(text.center(width))
    print("=" * width)


def print_separator(width: int = 60):
    """
    Print a separator line.
    
    Args:
        width: Width of separator
    """
    print("-" * width)


def setup_logger(name: str) -> logging.Logger:
    """
    Set up a logger with the application's configuration.
    
    Args:
        name: Logger name
    
    Returns:
        Configured logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, LOGGING_CONFIG['level']))
    
    # Add console handler if not already present
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(
            LOGGING_CONFIG['format'],
            LOGGING_CONFIG['date_format']
        ))
        logger.addHandler(handler)
    
    return logger
