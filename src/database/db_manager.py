"""
Database manager for the Restaurant Finder application.
"""

import logging
from datetime import datetime
from typing import List, Optional, Dict
from sqlalchemy import create_engine, and_, or_
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError

from config.settings import DATABASE_URL, SAMPLE_RESTAURANTS, TIME_SLOTS
from src.database.models import Base, Restaurant, AvailableTime
from src.utils.helpers import setup_logger

logger = setup_logger(__name__)


class DatabaseManager:
    """Manages database connections and operations."""
    
    def __init__(self, database_url: str = DATABASE_URL):
        """
        Initialize database manager.
        
        Args:
            database_url: SQLAlchemy database URL
        """
        self.engine = create_engine(database_url, echo=False)
        self.SessionLocal = sessionmaker(bind=self.engine)
        logger.info(f"Database manager initialized with URL: {database_url}")
    
    def create_tables(self):
        """Create all database tables."""
        try:
            Base.metadata.create_all(self.engine)
            logger.info("Database tables created successfully")
        except SQLAlchemyError as e:
            logger.error(f"Error creating database tables: {e}")
            raise
    
    def drop_tables(self):
        """Drop all database tables."""
        try:
            Base.metadata.drop_all(self.engine)
            logger.info("Database tables dropped successfully")
        except SQLAlchemyError as e:
            logger.error(f"Error dropping database tables: {e}")
            raise
    
    def get_session(self) -> Session:
        """Get a new database session."""
        return self.SessionLocal()
    
    # Restaurant CRUD operations
    
    def add_restaurant(self, restaurant_data: Dict) -> Optional[Restaurant]:
        """
        Add a new restaurant to the database.
        
        Args:
            restaurant_data: Dictionary with restaurant information
        
        Returns:
            Created Restaurant object or None if error
        """
        session = self.get_session()
        try:
            restaurant = Restaurant(**restaurant_data)
            session.add(restaurant)
            session.commit()
            session.refresh(restaurant)
            logger.info(f"Added restaurant: {restaurant.name}")
            return restaurant
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Error adding restaurant: {e}")
            return None
        finally:
            session.close()
    
    def get_restaurant_by_id(self, restaurant_id: int) -> Optional[Restaurant]:
        """
        Get a restaurant by ID.
        
        Args:
            restaurant_id: Restaurant ID
        
        Returns:
            Restaurant object or None if not found
        """
        session = self.get_session()
        try:
            restaurant = session.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
            return restaurant
        except SQLAlchemyError as e:
            logger.error(f"Error getting restaurant by ID: {e}")
            return None
        finally:
            session.close()
    
    def get_all_restaurants(self) -> List[Restaurant]:
        """
        Get all restaurants from the database.
        
        Returns:
            List of Restaurant objects
        """
        session = self.get_session()
        try:
            restaurants = session.query(Restaurant).all()
            return restaurants
        except SQLAlchemyError as e:
            logger.error(f"Error getting all restaurants: {e}")
            return []
        finally:
            session.close()
    
    def filter_restaurants(
        self,
        cuisine_type: Optional[str] = None,
        min_rating: Optional[float] = None,
        price_range: Optional[str] = None,
        max_distance: Optional[float] = None,
        user_lat: Optional[float] = None,
        user_lon: Optional[float] = None
    ) -> List[Restaurant]:
        """
        Filter restaurants by various criteria.
        
        Args:
            cuisine_type: Filter by cuisine type
            min_rating: Minimum rating
            price_range: Price range filter
            max_distance: Maximum distance in miles (requires user coordinates)
            user_lat: User latitude
            user_lon: User longitude
        
        Returns:
            List of filtered Restaurant objects
        """
        session = self.get_session()
        try:
            query = session.query(Restaurant)
            
            if cuisine_type and cuisine_type.lower() != 'any':
                query = query.filter(Restaurant.cuisine_type.ilike(f'%{cuisine_type}%'))
            
            if min_rating is not None:
                query = query.filter(Restaurant.rating >= min_rating)
            
            if price_range:
                query = query.filter(Restaurant.price_range == price_range)
            
            restaurants = query.all()
            
            # Filter by distance if user location provided
            if max_distance and user_lat and user_lon:
                from src.utils.helpers import haversine_distance
                filtered = []
                for restaurant in restaurants:
                    distance = haversine_distance(
                        user_lat, user_lon,
                        restaurant.latitude, restaurant.longitude
                    )
                    if distance <= max_distance:
                        filtered.append(restaurant)
                restaurants = filtered
            
            return restaurants
        except SQLAlchemyError as e:
            logger.error(f"Error filtering restaurants: {e}")
            return []
        finally:
            session.close()
    
    def update_restaurant(self, restaurant_id: int, update_data: Dict) -> bool:
        """
        Update a restaurant's information.
        
        Args:
            restaurant_id: Restaurant ID
            update_data: Dictionary with fields to update
        
        Returns:
            True if successful, False otherwise
        """
        session = self.get_session()
        try:
            restaurant = session.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
            if not restaurant:
                logger.warning(f"Restaurant with ID {restaurant_id} not found")
                return False
            
            for key, value in update_data.items():
                if hasattr(restaurant, key):
                    setattr(restaurant, key, value)
            
            restaurant.updated_at = datetime.utcnow()
            session.commit()
            logger.info(f"Updated restaurant: {restaurant.name}")
            return True
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Error updating restaurant: {e}")
            return False
        finally:
            session.close()
    
    def delete_restaurant(self, restaurant_id: int) -> bool:
        """
        Delete a restaurant from the database.
        
        Args:
            restaurant_id: Restaurant ID
        
        Returns:
            True if successful, False otherwise
        """
        session = self.get_session()
        try:
            restaurant = session.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
            if not restaurant:
                logger.warning(f"Restaurant with ID {restaurant_id} not found")
                return False
            
            session.delete(restaurant)
            session.commit()
            logger.info(f"Deleted restaurant: {restaurant.name}")
            return True
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Error deleting restaurant: {e}")
            return False
        finally:
            session.close()
    
    # AvailableTime CRUD operations
    
    def add_available_time(self, time_data: Dict) -> Optional[AvailableTime]:
        """
        Add an available time slot.
        
        Args:
            time_data: Dictionary with time slot information
        
        Returns:
            Created AvailableTime object or None if error
        """
        session = self.get_session()
        try:
            available_time = AvailableTime(**time_data)
            session.add(available_time)
            session.commit()
            session.refresh(available_time)
            logger.info(f"Added available time for restaurant ID {available_time.restaurant_id}")
            return available_time
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Error adding available time: {e}")
            return None
        finally:
            session.close()
    
    def get_available_times(self, restaurant_id: int, date: Optional[str] = None) -> List[AvailableTime]:
        """
        Get available times for a restaurant.
        
        Args:
            restaurant_id: Restaurant ID
            date: Optional date filter (ISO format)
        
        Returns:
            List of AvailableTime objects
        """
        session = self.get_session()
        try:
            query = session.query(AvailableTime).filter(AvailableTime.restaurant_id == restaurant_id)
            
            if date:
                query = query.filter(AvailableTime.date == date)
            
            times = query.all()
            return times
        except SQLAlchemyError as e:
            logger.error(f"Error getting available times: {e}")
            return []
        finally:
            session.close()
    
    def clear_database(self) -> bool:
        """
        Clear all data from the database.
        
        Returns:
            True if successful, False otherwise
        """
        session = self.get_session()
        try:
            session.query(AvailableTime).delete()
            session.query(Restaurant).delete()
            session.commit()
            logger.info("Database cleared successfully")
            return True
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Error clearing database: {e}")
            return False
        finally:
            session.close()
    
    def seed_sample_data(self) -> bool:
        """
        Seed the database with sample restaurant data.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Add sample restaurants
            for restaurant_data in SAMPLE_RESTAURANTS:
                restaurant = self.add_restaurant(restaurant_data)
                
                if restaurant:
                    # Add some mock available times for today
                    today = datetime.now().date().isoformat()
                    for i, time_slot in enumerate(TIME_SLOTS):
                        if i % 2 == 0:  # Add every other time slot
                            time_data = {
                                'restaurant_id': restaurant.id,
                                'date': today,
                                'time_slot': time_slot,
                                'party_size': 2,
                                'source': 'estimated',
                                'checked_at': datetime.utcnow()
                            }
                            self.add_available_time(time_data)
            
            logger.info(f"Seeded database with {len(SAMPLE_RESTAURANTS)} sample restaurants")
            return True
        except Exception as e:
            logger.error(f"Error seeding sample data: {e}")
            return False
    
    def get_restaurant_count(self) -> int:
        """
        Get the total count of restaurants in the database.
        
        Returns:
            Number of restaurants
        """
        session = self.get_session()
        try:
            count = session.query(Restaurant).count()
            return count
        except SQLAlchemyError as e:
            logger.error(f"Error getting restaurant count: {e}")
            return 0
        finally:
            session.close()
