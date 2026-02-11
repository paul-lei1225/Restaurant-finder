"""
Base scraper class for all web scrapers.
"""

import time
import random
import logging
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup

from config.settings import SCRAPING_CONFIG
from src.utils.helpers import setup_logger

logger = setup_logger(__name__)


class BaseScraper(ABC):
    """Abstract base class for all scrapers."""
    
    def __init__(self):
        """Initialize the base scraper."""
        self.session = requests.Session()
        self.rate_limit_delay = SCRAPING_CONFIG['rate_limit_delay']
        self.timeout = SCRAPING_CONFIG['timeout']
        self.max_retries = SCRAPING_CONFIG['max_retries']
        self.retry_delay = SCRAPING_CONFIG['retry_delay']
        self.user_agents = SCRAPING_CONFIG['user_agents']
        self.last_request_time = 0
        
        logger.info(f"{self.__class__.__name__} initialized")
    
    def _get_random_user_agent(self) -> str:
        """
        Get a random user agent string.
        
        Returns:
            User agent string
        """
        return random.choice(self.user_agents)
    
    def _respect_rate_limit(self):
        """Respect rate limiting by waiting between requests."""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        
        if time_since_last_request < self.rate_limit_delay:
            sleep_time = self.rate_limit_delay - time_since_last_request
            logger.debug(f"Rate limiting: sleeping for {sleep_time:.2f} seconds")
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def check_robots_txt(self, base_url: str, path: str) -> bool:
        """
        Check if scraping is allowed by robots.txt.
        
        Args:
            base_url: Base URL of the website
            path: Path to check
        
        Returns:
            True if allowed, False otherwise
        """
        try:
            rp = RobotFileParser()
            rp.set_url(f"{base_url}/robots.txt")
            rp.read()
            
            user_agent = self._get_random_user_agent()
            is_allowed = rp.can_fetch(user_agent, path)
            
            if not is_allowed:
                logger.warning(f"Scraping not allowed by robots.txt for: {path}")
            
            return is_allowed
        except Exception as e:
            logger.error(f"Error checking robots.txt: {e}")
            # Be conservative - if we can't check, assume it's not allowed
            return False
    
    def make_request(self, url: str, method: str = 'GET', **kwargs) -> Optional[requests.Response]:
        """
        Make an HTTP request with retry logic and error handling.
        
        Args:
            url: URL to request
            method: HTTP method (GET, POST, etc.)
            **kwargs: Additional arguments to pass to requests
        
        Returns:
            Response object or None if all retries failed
        """
        self._respect_rate_limit()
        
        headers = kwargs.pop('headers', {})
        headers['User-Agent'] = self._get_random_user_agent()
        
        for attempt in range(self.max_retries):
            try:
                logger.debug(f"Making {method} request to {url} (attempt {attempt + 1}/{self.max_retries})")
                
                response = self.session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    timeout=self.timeout,
                    **kwargs
                )
                
                response.raise_for_status()
                logger.debug(f"Request successful: {url}")
                return response
                
            except requests.exceptions.HTTPError as e:
                logger.error(f"HTTP error for {url}: {e}")
                if hasattr(e, 'response') and e.response is not None:
                    if e.response.status_code == 429:  # Too many requests
                        wait_time = self.retry_delay * (attempt + 1)
                        logger.warning(f"Rate limited. Waiting {wait_time} seconds...")
                        time.sleep(wait_time)
                    elif e.response.status_code >= 500:  # Server error
                        if attempt < self.max_retries - 1:
                            logger.warning(f"Server error. Retrying in {self.retry_delay} seconds...")
                            time.sleep(self.retry_delay)
                        else:
                            return None
                    else:
                        return None
                else:
                    return None
                    
            except requests.exceptions.Timeout:
                logger.error(f"Timeout for {url}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                else:
                    return None
                    
            except requests.exceptions.RequestException as e:
                logger.error(f"Request error for {url}: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                else:
                    return None
        
        return None
    
    def parse_html(self, html_content: str) -> Optional[BeautifulSoup]:
        """
        Parse HTML content using BeautifulSoup.
        
        Args:
            html_content: HTML string
        
        Returns:
            BeautifulSoup object or None if parsing fails
        """
        try:
            soup = BeautifulSoup(html_content, 'lxml')
            return soup
        except Exception as e:
            logger.error(f"Error parsing HTML: {e}")
            return None
    
    @abstractmethod
    def scrape(self, **kwargs) -> List[Dict]:
        """
        Scrape data from the target website.
        
        This method must be implemented by subclasses.
        
        Args:
            **kwargs: Parameters specific to the scraper
        
        Returns:
            List of dictionaries containing scraped data
        """
        pass
    
    def close(self):
        """Close the session and clean up resources."""
        self.session.close()
        logger.info(f"{self.__class__.__name__} closed")
