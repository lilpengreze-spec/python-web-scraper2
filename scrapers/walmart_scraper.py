"""
Walmart Reviews Scraper

This module handles scraping reviews from Walmart products.
"""

import os
import re
import logging
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict, Optional, Any
from urllib.parse import urlparse, parse_qs

logger = logging.getLogger(__name__)


class WalmartScraper:
    """
    Scraper for Walmart product reviews.
    """
    
    def __init__(self):
        """Initialize the Walmart scraper."""
        # Setup session for web requests
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
    
    def extract_product_id(self, input_str: str) -> str:
        """
        Extract product ID from Walmart URL or return the input if it's already an ID.
        
        Args:
            input_str: Walmart product ID or URL
            
        Returns:
            Product ID string
        """
        if not input_str:
            return ""
        
        # If it's already a product ID (no URL structure), return as is
        if not input_str.startswith('http'):
            return input_str
        
        try:
            # Parse URL to extract product ID
            parsed_url = urlparse(input_str)
            
            # Extract from path (e.g., /ip/product-name/123456 -> 123456)
            if '/ip/' in parsed_url.path:
                parts = parsed_url.path.split('/')
                if len(parts) > 2:
                    product_id = parts[-1].split('?')[0]
                    return product_id
            
            return ""
            
        except Exception as e:
            logger.error(f"Error extracting product ID from Walmart URL: {str(e)}")
            return ""
    
    def get_reviews(self, input_str: str) -> List[Dict[str, Any]]:
        """
        Get reviews from Walmart product pages.
        
        Args:
            input_str: Walmart product ID or URL
            
        Returns:
            List of review dictionaries
        """
        if not input_str:
            return []
        
        # Extract product ID from input
        product_id = self.extract_product_id(input_str)
        if not product_id:
            raise Exception("Invalid Walmart product ID or URL")
        
        try:
            # Construct Walmart URL
            url = f"https://www.walmart.com/ip/{product_id}"
            
            # Make request
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            reviews = []
            
            # Find review containers (Walmart's structure)
            review_containers = soup.find_all('div', {'data-testid': 'reviews-section'}) or \
                               soup.find_all('div', class_=re.compile(r'review.*item')) or \
                               soup.find_all('div', class_=re.compile(r'customer.*review'))
            
            for container in review_containers[:10]:  # Limit to 10 reviews
                try:
                    # Extract reviewer name
                    name_elem = container.find('span', class_=re.compile(r'reviewer.*name')) or \
                               container.find('div', class_=re.compile(r'customer.*name'))
                    
                    reviewer_name = 'Anonymous'
                    if name_elem:
                        reviewer_name = name_elem.get_text(strip=True)
                    
                    # Extract rating
                    rating_elem = container.find('div', {'aria-label': re.compile(r'\d+ star')}) or \
                                 container.find('span', class_=re.compile(r'star.*rating'))
                    
                    rating = 0
                    if rating_elem:
                        rating_text = rating_elem.get('aria-label', '') or rating_elem.get_text()
                        rating_match = re.search(r'(\d+)', rating_text)
                        if rating_match:
                            rating = int(rating_match.group(1))
                    
                    # Extract review text
                    text_elem = container.find('div', class_=re.compile(r'review.*text')) or \
                               container.find('span', class_=re.compile(r'review.*content'))
                    
                    review_text = ''
                    if text_elem:
                        review_text = text_elem.get_text(strip=True)
                    
                    # Extract date
                    date_elem = container.find('span', class_=re.compile(r'review.*date')) or \
                               container.find('time')
                    
                    date = ''
                    if date_elem:
                        date = date_elem.get_text(strip=True) or date_elem.get('datetime', '')
                    
                    # Skip if no meaningful content
                    if not review_text and rating == 0:
                        continue
                    
                    review_data = {
                        'reviewer_name': reviewer_name,
                        'rating': rating,
                        'review_text': review_text,
                        'date': date,
                        'review_url': url,
                        'source': 'walmart_scraping'
                    }
                    reviews.append(review_data)
                    
                except Exception as e:
                    logger.warning(f"Error parsing individual Walmart review: {str(e)}")
                    continue
            
            logger.info(f"Retrieved {len(reviews)} reviews from Walmart")
            return reviews
            
        except requests.RequestException as e:
            logger.error(f"Network error during Walmart scraping: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Walmart scraping error: {str(e)}")
            raise
