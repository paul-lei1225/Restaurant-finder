"""
Recommendation engine for suggesting restaurants and reservation times.
"""

import logging
import random
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple

from src.database.models import Restaurant, AvailableTime
from src.utils.helpers import haversine_distance, format_rating, format_distance, setup_logger

logger = setup_logger(__name__)


class SuggestionEngine:
    """Engine for generating restaurant and reservation suggestions."""
    
    def __init__(self, db_manager):
        """
        Initialize the suggestion engine.
        
        Args:
            db_manager: DatabaseManager instance
        """
        self.db_manager = db_manager
        logger.info("SuggestionEngine initialized")
    
    def get_recommendations(
        self,
        user_lat: float,
        user_lon: float,
        cuisine_type: Optional[str] = None,
        min_rating: float = 3.5,
        price_range: Optional[str] = None,
        max_distance: float = 10.0,
        limit: int = 10
    ) -> List[Tuple[Restaurant, float, List[Dict]]]:
        """
        Get restaurant recommendations based on user preferences.
        
        Args:
            user_lat: User's latitude
            user_lon: User's longitude
            cuisine_type: Preferred cuisine type (or 'any')
            min_rating: Minimum rating filter
            price_range: Price range filter
            max_distance: Maximum distance in miles
            limit: Maximum number of recommendations
        
        Returns:
            List of tuples: (restaurant, distance, suggested_times)
        """
        logger.info(f"Getting recommendations for cuisine={cuisine_type}, rating>={min_rating}, "
                   f"price={price_range}, max_distance={max_distance}")
        
        # Get filtered restaurants
        restaurants = self.db_manager.filter_restaurants(
            cuisine_type=cuisine_type,
            min_rating=min_rating,
            price_range=price_range
        )
        
        if not restaurants:
            logger.warning("No restaurants found matching criteria")
            return []
        
        # Calculate distances and filter by max distance
        recommendations = []
        for restaurant in restaurants:
            distance = haversine_distance(
                user_lat, user_lon,
                restaurant.latitude, restaurant.longitude
            )
            
            if distance <= max_distance:
                # Get suggested times
                suggested_times = self._get_suggested_times(restaurant.id)
                recommendations.append((restaurant, distance, suggested_times))
        
        # Sort by rating (descending) then distance (ascending)
        recommendations.sort(key=lambda x: (-x[0].rating, x[1]))
        
        # Limit results
        recommendations = recommendations[:limit]
        
        logger.info(f"Generated {len(recommendations)} recommendations")
        return recommendations
    
    def _get_suggested_times(self, restaurant_id: int, date: Optional[str] = None) -> List[Dict]:
        """
        Get suggested reservation times for a restaurant.
        
        Args:
            restaurant_id: Restaurant ID
            date: Optional date (defaults to today)
        
        Returns:
            List of suggested time dictionaries
        """
        if not date:
            date = datetime.now().date().isoformat()
        
        # Get available times from database
        available_times = self.db_manager.get_available_times(restaurant_id, date)
        
        if not available_times:
            # Generate mock available times if none exist
            return self._generate_mock_available_times()
        
        # Convert to suggestion format
        suggestions = []
        for time_slot in available_times:
            # Determine if time is "less busy" (mock logic)
            is_less_busy = self._is_less_busy_time(time_slot.time_slot)
            
            suggestions.append({
                'time': time_slot.time_slot,
                'date': time_slot.date,
                'party_size': time_slot.party_size,
                'available': True,
                'less_busy': is_less_busy,
                'source': time_slot.source
            })
        
        return suggestions
    
    def _generate_mock_available_times(self) -> List[Dict]:
        """
        Generate mock available times for demonstration.
        
        Returns:
            List of mock time slot dictionaries
        """
        today = datetime.now().date().isoformat()
        
        mock_times = [
            {'time': '6:00 PM', 'date': today, 'party_size': 2, 'available': True, 
             'less_busy': True, 'source': 'estimated'},
            {'time': '6:30 PM', 'date': today, 'party_size': 2, 'available': True, 
             'less_busy': True, 'source': 'estimated'},
            {'time': '7:00 PM', 'date': today, 'party_size': 2, 'available': True, 
             'less_busy': False, 'source': 'estimated'},
            {'time': '8:00 PM', 'date': today, 'party_size': 2, 'available': True, 
             'less_busy': False, 'source': 'estimated'},
        ]
        
        # Randomly select 2-3 times
        return random.sample(mock_times, min(3, len(mock_times)))
    
    def _is_less_busy_time(self, time_str: str) -> bool:
        """
        Determine if a time slot is typically less busy.
        
        Args:
            time_str: Time string (e.g., "6:30 PM")
        
        Returns:
            True if less busy, False otherwise
        """
        # Mock logic: Earlier times (before 7 PM) and later times (after 9 PM) are less busy
        try:
            # Parse time
            time_obj = datetime.strptime(time_str, '%I:%M %p')
            hour = time_obj.hour
            
            # 5:30-6:30 PM or after 9 PM are less busy
            if (17 <= hour < 19) or hour >= 21:
                return True
            return False
        except Exception:
            return False
    
    def rank_by_availability(
        self,
        restaurants: List[Restaurant],
        preferred_time: Optional[str] = None
    ) -> List[Tuple[Restaurant, int]]:
        """
        Rank restaurants by availability.
        
        Args:
            restaurants: List of Restaurant objects
            preferred_time: Preferred time slot
        
        Returns:
            List of tuples: (restaurant, availability_score)
        """
        ranked = []
        
        for restaurant in restaurants:
            available_times = self.db_manager.get_available_times(restaurant.id)
            
            # Calculate availability score
            score = len(available_times)
            
            # Bonus if preferred time is available
            if preferred_time:
                for time_slot in available_times:
                    if time_slot.time_slot == preferred_time:
                        score += 10
                        break
            
            ranked.append((restaurant, score))
        
        # Sort by score (descending)
        ranked.sort(key=lambda x: -x[1])
        
        return ranked
    
    def find_best_time_for_group(
        self,
        restaurant_id: int,
        party_size: int,
        date: Optional[str] = None
    ) -> Optional[Dict]:
        """
        Find the best available time for a group size.
        
        Args:
            restaurant_id: Restaurant ID
            party_size: Number of people
            date: Date for reservation
        
        Returns:
            Best time slot dictionary or None
        """
        if not date:
            date = datetime.now().date().isoformat()
        
        available_times = self.db_manager.get_available_times(restaurant_id, date)
        
        # Filter by party size
        suitable_times = [t for t in available_times if t.party_size >= party_size]
        
        if not suitable_times:
            logger.warning(f"No suitable times found for party size {party_size}")
            return None
        
        # Pick the first less busy time, or any available time
        for time_slot in suitable_times:
            if self._is_less_busy_time(time_slot.time_slot):
                return {
                    'time': time_slot.time_slot,
                    'date': time_slot.date,
                    'party_size': time_slot.party_size,
                    'less_busy': True
                }
        
        # Return first available
        first = suitable_times[0]
        return {
            'time': first.time_slot,
            'date': first.date,
            'party_size': first.party_size,
            'less_busy': False
        }
    
    def get_cuisine_statistics(self) -> Dict[str, int]:
        """
        Get statistics about available cuisines.
        
        Returns:
            Dictionary mapping cuisine types to counts
        """
        restaurants = self.db_manager.get_all_restaurants()
        
        stats = {}
        for restaurant in restaurants:
            cuisine = restaurant.cuisine_type
            stats[cuisine] = stats.get(cuisine, 0) + 1
        
        logger.info(f"Cuisine statistics: {stats}")
        return stats
    
    def format_recommendation(
        self,
        restaurant: Restaurant,
        distance: float,
        suggested_times: List[Dict]
    ) -> str:
        """
        Format a recommendation for display.
        
        Args:
            restaurant: Restaurant object
            distance: Distance from user
            suggested_times: List of suggested time slots
        
        Returns:
            Formatted string
        """
        lines = []
        lines.append(f"⭐ {restaurant.name} - {format_rating(restaurant.rating)} - {restaurant.price_range}")
        lines.append(f"   📍 {restaurant.address}")
        lines.append(f"   📏 {format_distance(distance)} away")
        lines.append(f"   🍽️  {restaurant.cuisine_type}")
        
        if restaurant.phone:
            lines.append(f"   📞 {restaurant.phone}")
        
        if suggested_times:
            lines.append(f"\n   Suggested Times (Today):")
            for time_info in suggested_times[:3]:  # Show max 3 times
                status = "✓ Available"
                if time_info.get('less_busy'):
                    status += " (Less busy)"
                lines.append(f"   • {time_info['time']} {status}")
        
        return '\n'.join(lines)
