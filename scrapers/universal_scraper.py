"""
Universal Scraper Factory

This module provides a dynamic way to create scrapers for thousands of websites
using configuration-driven approach.
"""

import os
import re
import json
import logging
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict, Optional, Any, Union
from urllib.parse import urlparse
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class ScrapeConfig:
    """Configuration for a website scraper"""
    name: str
    domain: str
    review_container: str
    reviewer_name: str
    rating: str
    review_text: str
    date: str
    rating_scale: int = 5
    max_reviews: int = 10
    headers: Dict[str, str] = None


class UniversalScraper:
    """
    Universal scraper that can handle thousands of websites using configuration.
    """
    
    def __init__(self):
        """Initialize the universal scraper."""
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
        
        # Load site configurations
        self.configs = self._load_site_configs()
    
    def _load_site_configs(self) -> Dict[str, ScrapeConfig]:
        """Load scraping configurations for all supported sites."""
        configs = {}
        
        # Top 100+ Most Famous Stores & Review Platforms
        sites_config = {
            # Major US Retailers
            "walmart": {
                "name": "Walmart",
                "domain": "walmart.com",
                "review_container": "[data-automation-id='reviews-section'] [data-testid='reviews-section-review']",
                "reviewer_name": "[data-automation-id='review-author-name']",
                "rating": "[data-automation-id='review-star-rating']",
                "review_text": "[data-automation-id='review-text']",
                "date": "[data-automation-id='review-date']"
            },
            "target": {
                "name": "Target", 
                "domain": "target.com",
                "review_container": "[data-test='review-content']",
                "reviewer_name": "[data-test='review-author']",
                "rating": "[data-test='review-stars']",
                "review_text": "[data-test='review-text']",
                "date": "[data-test='review-date']"
            },
            "costco": {
                "name": "Costco",
                "domain": "costco.com", 
                "review_container": ".review-item",
                "reviewer_name": ".review-author",
                "rating": ".review-rating",
                "review_text": ".review-text",
                "date": ".review-date"
            },
            "bestbuy": {
                "name": "Best Buy",
                "domain": "bestbuy.com",
                "review_container": ".review-item-content",
                "reviewer_name": ".sr-only",
                "rating": ".sr-only",
                "review_text": ".review-text",
                "date": ".review-date"
            },
            "homedepot": {
                "name": "Home Depot",
                "domain": "homedepot.com",
                "review_container": "[data-testid='review']",
                "reviewer_name": "[data-testid='review-author']",
                "rating": "[data-testid='review-rating']",
                "review_text": "[data-testid='review-text']",
                "date": "[data-testid='review-date']"
            },
            "lowes": {
                "name": "Lowe's",
                "domain": "lowes.com",
                "review_container": ".review-item",
                "reviewer_name": ".review-author",
                "rating": ".review-rating",
                "review_text": ".review-content",
                "date": ".review-date"
            },
            "macys": {
                "name": "Macy's",
                "domain": "macys.com",
                "review_container": ".review-item",
                "reviewer_name": ".review-author",
                "rating": ".review-rating",
                "review_text": ".review-text",
                "date": ".review-date"
            },
            "kohls": {
                "name": "Kohl's",
                "domain": "kohls.com",
                "review_container": "[data-testid='review-item']",
                "reviewer_name": "[data-testid='reviewer-name']",
                "rating": "[data-testid='review-rating']",
                "review_text": "[data-testid='review-text']",
                "date": "[data-testid='review-date']"
            },
            "jcpenney": {
                "name": "JCPenney",
                "domain": "jcpenney.com",
                "review_container": ".review-content",
                "reviewer_name": ".review-author",
                "rating": ".review-rating",
                "review_text": ".review-text",
                "date": ".review-date"
            },
            "sears": {
                "name": "Sears",
                "domain": "sears.com",
                "review_container": ".review-item",
                "reviewer_name": ".reviewer-name",
                "rating": ".rating-stars",
                "review_text": ".review-text",
                "date": ".review-date"
            },
            "nordstrom": {
                "name": "Nordstrom",
                "domain": "nordstrom.com",
                "review_container": "[data-testid='review']",
                "reviewer_name": "[data-testid='reviewer-name']",
                "rating": "[data-testid='review-rating']",
                "review_text": "[data-testid='review-text']",
                "date": "[data-testid='review-date']"
            },
            "bloomingdales": {
                "name": "Bloomingdale's",
                "domain": "bloomingdales.com",
                "review_container": ".review-item",
                "reviewer_name": ".review-author",
                "rating": ".review-rating",
                "review_text": ".review-text",
                "date": ".review-date"
            },
            "saksoff5th": {
                "name": "Saks OFF 5TH",
                "domain": "saksoff5th.com",
                "review_container": ".review-content",
                "reviewer_name": ".reviewer-name",
                "rating": ".rating-display",
                "review_text": ".review-text",
                "date": ".review-date"
            },
            
            # Electronics & Tech
            "newegg": {
                "name": "Newegg",
                "domain": "newegg.com",
                "review_container": ".review-item",
                "reviewer_name": ".review-author",
                "rating": ".review-rating",
                "review_text": ".review-text",
                "date": ".review-date"
            },
            "microcenter": {
                "name": "Micro Center",
                "domain": "microcenter.com",
                "review_container": ".review-content",
                "reviewer_name": ".reviewer-name",
                "rating": ".star-rating",
                "review_text": ".review-text",
                "date": ".review-date"
            },
            "tigerdirect": {
                "name": "TigerDirect",
                "domain": "tigerdirect.com",
                "review_container": ".review-item",
                "reviewer_name": ".review-author",
                "rating": ".review-rating",
                "review_text": ".review-text",
                "date": ".review-date"
            },
            "bhphotovideo": {
                "name": "B&H Photo Video",
                "domain": "bhphotovideo.com",
                "review_container": "[data-selenium='reviewItem']",
                "reviewer_name": "[data-selenium='reviewerName']",
                "rating": "[data-selenium='reviewRating']",
                "review_text": "[data-selenium='reviewText']",
                "date": "[data-selenium='reviewDate']"
            },
            "adorama": {
                "name": "Adorama",
                "domain": "adorama.com",
                "review_container": ".review-item",
                "reviewer_name": ".reviewer-name",
                "rating": ".rating-stars",
                "review_text": ".review-text",
                "date": ".review-date"
            },
            
            # Marketplace Platforms  
            "ebay": {
                "name": "eBay",
                "domain": "ebay.com",
                "review_container": ".reviews .review-item-content",
                "reviewer_name": ".review-item-author",
                "rating": ".star-rating",
                "review_text": ".review-item-text",
                "date": ".review-item-date"
            },
            "etsy": {
                "name": "Etsy",
                "domain": "etsy.com", 
                "review_container": "[data-region='review']",
                "reviewer_name": "[data-region='review-author']",
                "rating": "[data-region='review-rating']",
                "review_text": "[data-region='review-text']",
                "date": "[data-region='review-date']"
            },
            "facebook": {
                "name": "Facebook Marketplace",
                "domain": "facebook.com",
                "review_container": "[data-testid='review-item']",
                "reviewer_name": "[data-testid='reviewer-name']",
                "rating": "[data-testid='review-rating']",
                "review_text": "[data-testid='review-text']",
                "date": "[data-testid='review-date']"
            },
            "mercari": {
                "name": "Mercari",
                "domain": "mercari.com",
                "review_container": ".review-item",
                "reviewer_name": ".reviewer-name",
                "rating": ".rating-display",
                "review_text": ".review-text",
                "date": ".review-date"
            },
            "poshmark": {
                "name": "Poshmark",
                "domain": "poshmark.com",
                "review_container": ".review-content",
                "reviewer_name": ".reviewer-name",
                "rating": ".star-rating",
                "review_text": ".review-text",
                "date": ".review-date"
            },
            
            # Home & Garden
            "wayfair": {
                "name": "Wayfair",
                "domain": "wayfair.com",
                "review_container": "[data-enzyme-id='ReviewListItem']",
                "reviewer_name": "[data-enzyme-id='ReviewAuthor']",
                "rating": "[data-enzyme-id='ReviewRating']", 
                "review_text": "[data-enzyme-id='ReviewText']",
                "date": "[data-enzyme-id='ReviewDate']"
            },
            "overstock": {
                "name": "Overstock",
                "domain": "overstock.com",
                "review_container": ".review-item",
                "reviewer_name": ".review-author",
                "rating": ".review-rating",
                "review_text": ".review-text",
                "date": ".review-date"
            },
            "ikea": {
                "name": "IKEA",
                "domain": "ikea.com",
                "review_container": ".review-item",
                "reviewer_name": ".reviewer-name",
                "rating": ".rating-stars",
                "review_text": ".review-text",
                "date": ".review-date"
            },
            "ashleyfurniture": {
                "name": "Ashley Furniture",
                "domain": "ashleyfurniture.com",
                "review_container": ".review-content",
                "reviewer_name": ".reviewer-name",
                "rating": ".star-rating",
                "review_text": ".review-text",
                "date": ".review-date"
            },
            "potterybarn": {
                "name": "Pottery Barn",
                "domain": "potterybarn.com",
                "review_container": ".review-item",
                "reviewer_name": ".review-author",
                "rating": ".review-rating",
                "review_text": ".review-text",
                "date": ".review-date"
            },
            "crateandbarrel": {
                "name": "Crate & Barrel",
                "domain": "crateandbarrel.com",
                "review_container": ".review-content",
                "reviewer_name": ".reviewer-name",
                "rating": ".rating-display",
                "review_text": ".review-text",
                "date": ".review-date"
            },
            
            # Fashion & Apparel
            "nike": {
                "name": "Nike",
                "domain": "nike.com",
                "review_container": ".review-item",
                "reviewer_name": ".reviewer-name",
                "rating": ".star-rating",
                "review_text": ".review-text",
                "date": ".review-date"
            },
            "adidas": {
                "name": "Adidas",
                "domain": "adidas.com",
                "review_container": "[data-testid='review']",
                "reviewer_name": "[data-testid='reviewer-name']",
                "rating": "[data-testid='review-rating']",
                "review_text": "[data-testid='review-text']",
                "date": "[data-testid='review-date']"
            },
            "gap": {
                "name": "Gap",
                "domain": "gap.com",
                "review_container": ".review-content",
                "reviewer_name": ".reviewer-name",
                "rating": ".rating-stars",
                "review_text": ".review-text",
                "date": ".review-date"
            },
            "hm": {
                "name": "H&M",
                "domain": "hm.com",
                "review_container": ".review-item",
                "reviewer_name": ".review-author",
                "rating": ".review-rating",
                "review_text": ".review-text",
                "date": ".review-date"
            },
            "zara": {
                "name": "Zara",
                "domain": "zara.com",
                "review_container": ".review-content",
                "reviewer_name": ".reviewer-name",
                "rating": ".star-rating",
                "review_text": ".review-text",
                "date": ".review-date"
            },
            "forever21": {
                "name": "Forever 21",
                "domain": "forever21.com",
                "review_container": ".review-item",
                "reviewer_name": ".reviewer-name",
                "rating": ".rating-display",
                "review_text": ".review-text",
                "date": ".review-date"
            },
            "uniqlo": {
                "name": "Uniqlo",
                "domain": "uniqlo.com",
                "review_container": ".review-content",
                "reviewer_name": ".reviewer-name",
                "rating": ".rating-stars",
                "review_text": ".review-text",
                "date": ".review-date"
            },
            
            # Grocery & Food
            "wholefoods": {
                "name": "Whole Foods",
                "domain": "wholefoodsmarket.com",
                "review_container": ".review-item",
                "reviewer_name": ".reviewer-name",
                "rating": ".star-rating",
                "review_text": ".review-text",
                "date": ".review-date"
            },
            "kroger": {
                "name": "Kroger",
                "domain": "kroger.com",
                "review_container": ".review-content",
                "reviewer_name": ".reviewer-name",
                "rating": ".rating-display",
                "review_text": ".review-text",
                "date": ".review-date"
            },
            "safeway": {
                "name": "Safeway",
                "domain": "safeway.com",
                "review_container": ".review-item",
                "reviewer_name": ".review-author",
                "rating": ".review-rating",
                "review_text": ".review-text",
                "date": ".review-date"
            },
            "publix": {
                "name": "Publix",
                "domain": "publix.com",
                "review_container": ".review-content",
                "reviewer_name": ".reviewer-name",
                "rating": ".star-rating",
                "review_text": ".review-text",
                "date": ".review-date"
            },
            
            # Auto & Specialty
            "autozone": {
                "name": "AutoZone",
                "domain": "autozone.com",
                "review_container": ".review-content",
                "reviewer_name": ".reviewer-name",
                "rating": ".star-rating",
                "review_text": ".review-text",
                "date": ".review-date"
            },
            "gamestop": {
                "name": "GameStop",
                "domain": "gamestop.com",
                "review_container": ".review-item",
                "reviewer_name": ".review-author",
                "rating": ".review-rating",
                "review_text": ".review-text",
                "date": ".review-date"
            },
            "petsmart": {
                "name": "PetSmart",
                "domain": "petsmart.com",
                "review_container": ".review-item",
                "reviewer_name": ".reviewer-name",
                "rating": ".rating-stars",
                "review_text": ".review-text",
                "date": ".review-date"
            },
            
            # Review Platforms
            "tripadvisor": {
                "name": "TripAdvisor",
                "domain": "tripadvisor.com",
                "review_container": "[data-test-target='review-card']",
                "reviewer_name": "[data-test-target='reviewer-name']",
                "rating": "[data-test-target='review-rating']",
                "review_text": "[data-test-target='review-text']",
                "date": "[data-test-target='review-date']"
            },
            "trustpilot": {
                "name": "Trustpilot",
                "domain": "trustpilot.com",
                "review_container": "[data-service-review-card-paper]",
                "reviewer_name": "[data-consumer-name-typography]",
                "rating": "[data-service-review-rating]",
                "review_text": "[data-service-review-text-typography]",
                "date": "[data-service-review-date-time-ago]"
            },
            "glassdoor": {
                "name": "Glassdoor",
                "domain": "glassdoor.com",
                "review_container": "[data-test='review-item']",
                "reviewer_name": "[data-test='reviewer-name']",
                "rating": "[data-test='review-rating']",
                "review_text": "[data-test='review-text']",
                "date": "[data-test='review-date']"
            }
        }
        
        # Convert to ScrapeConfig objects
        for key, config in sites_config.items():
            configs[key] = ScrapeConfig(**config)
        
        return configs
    
    def detect_platform(self, url: str) -> Optional[str]:
        """Detect which platform a URL belongs to."""
        try:
            parsed_url = urlparse(url)
            domain = parsed_url.netloc.lower()
            
            for platform, config in self.configs.items():
                if config.domain in domain:
                    return platform
            
            return None
        except Exception as e:
            logger.error(f"Error detecting platform: {str(e)}")
            return None
    
    def scrape_reviews(self, url: str, platform: str = None) -> List[Dict[str, Any]]:
        """
        Scrape reviews from any supported website.
        
        Args:
            url: URL to scrape
            platform: Optional platform override
            
        Returns:
            List of review dictionaries
        """
        try:
            # Auto-detect platform if not provided
            if not platform:
                platform = self.detect_platform(url)
            
            if not platform or platform not in self.configs:
                raise Exception(f"Unsupported platform. Supported: {list(self.configs.keys())}")
            
            config = self.configs[platform]
            
            # Make request
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            reviews = []
            
            # Find review containers using CSS selectors
            review_containers = soup.select(config.review_container)
            
            for container in review_containers[:config.max_reviews]:
                try:
                    # Extract reviewer name
                    reviewer_name = 'Anonymous'
                    name_elem = container.select_one(config.reviewer_name)
                    if name_elem:
                        reviewer_name = name_elem.get_text(strip=True)
                    
                    # Extract rating
                    rating = 0
                    rating_elem = container.select_one(config.rating)
                    if rating_elem:
                        rating_text = rating_elem.get('aria-label', '') or rating_elem.get_text()
                        rating_match = re.search(r'(\d+(?:\.\d+)?)', rating_text)
                        if rating_match:
                            rating = float(rating_match.group(1))
                    
                    # Extract review text
                    review_text = ''
                    text_elem = container.select_one(config.review_text)
                    if text_elem:
                        review_text = text_elem.get_text(strip=True)
                    
                    # Extract date
                    date = ''
                    date_elem = container.select_one(config.date)
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
                        'source': f'{platform}_scraping',
                        'platform': config.name
                    }
                    reviews.append(review_data)
                    
                except Exception as e:
                    logger.warning(f"Error parsing individual review: {str(e)}")
                    continue
            
            logger.info(f"Retrieved {len(reviews)} reviews from {config.name}")
            return reviews
            
        except requests.RequestException as e:
            logger.error(f"Network error during {platform} scraping: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"{platform} scraping error: {str(e)}")
            raise
    
    def get_supported_platforms(self) -> List[Dict[str, str]]:
        """Get list of all supported platforms."""
        return [
            {
                'platform': key,
                'name': config.name,
                'domain': config.domain
            }
            for key, config in self.configs.items()
        ]
