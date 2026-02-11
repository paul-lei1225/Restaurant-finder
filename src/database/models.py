"""
Database models for the Restaurant Finder application.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Restaurant(Base):
    """Restaurant model for storing restaurant information."""
    
    __tablename__ = 'restaurants'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False, index=True)
    cuisine_type = Column(String(100), nullable=False, index=True)
    rating = Column(Float, nullable=False)
    price_range = Column(String(10), nullable=False)
    address = Column(String(500), nullable=False)
    phone = Column(String(50))
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    website = Column(String(500))
    hours = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to available times
    available_times = relationship('AvailableTime', back_populates='restaurant', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<Restaurant(name='{self.name}', cuisine='{self.cuisine_type}', rating={self.rating})>"
    
    def to_dict(self):
        """Convert restaurant to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'cuisine_type': self.cuisine_type,
            'rating': self.rating,
            'price_range': self.price_range,
            'address': self.address,
            'phone': self.phone,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'website': self.website,
            'hours': self.hours,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class AvailableTime(Base):
    """Available time slots for restaurant reservations."""
    
    __tablename__ = 'available_times'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'), nullable=False, index=True)
    date = Column(String(20), nullable=False)  # ISO format date string
    time_slot = Column(String(20), nullable=False)
    party_size = Column(Integer, default=2)
    source = Column(String(50), default='estimated')  # e.g., "OpenTable", "Resy", "estimated"
    checked_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to restaurant
    restaurant = relationship('Restaurant', back_populates='available_times')
    
    def __repr__(self):
        return f"<AvailableTime(restaurant_id={self.restaurant_id}, date='{self.date}', time='{self.time_slot}')>"
    
    def to_dict(self):
        """Convert available time to dictionary."""
        return {
            'id': self.id,
            'restaurant_id': self.restaurant_id,
            'date': self.date,
            'time_slot': self.time_slot,
            'party_size': self.party_size,
            'source': self.source,
            'checked_at': self.checked_at.isoformat() if self.checked_at else None
        }
