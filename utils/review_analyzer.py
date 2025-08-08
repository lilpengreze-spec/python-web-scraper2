"""
Advanced Review Filtering and Search

This module provides intelligent filtering of scraped reviews based on
keywords, sentiment, and criteria to help users find specific information.
"""

import re
import logging
from typing import List, Dict, Any, Optional, Set
from collections import Counter
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class ReviewFilter:
    """Configuration for review filtering"""
    keywords: List[str] = None
    categories: List[str] = None
    min_rating: float = 0
    max_rating: float = 5
    sentiment: str = None  # 'positive', 'negative', 'neutral'
    sort_by: str = 'relevance'  # 'relevance', 'rating', 'date', 'length'
    limit: int = 50


class ReviewAnalyzer:
    """
    Intelligent review analysis and filtering system.
    """
    
    def __init__(self):
        """Initialize the review analyzer."""
        # Common criteria categories for different product types
        self.criteria_keywords = {
            'assembly': [
                'assembly', 'assemble', 'put together', 'setup', 'installation', 
                'install', 'build', 'construction', 'instructions', 'manual',
                'easy to assemble', 'hard to assemble', 'difficult assembly'
            ],
            'quality': [
                'quality', 'build quality', 'material', 'sturdy', 'durable',
                'solid', 'cheap', 'flimsy', 'well made', 'construction',
                'materials', 'finish', 'craftsmanship'
            ],
            'value': [
                'value', 'price', 'worth', 'expensive', 'cheap', 'affordable',
                'money', 'cost', 'budget', 'overpriced', 'good deal',
                'bang for buck', 'value for money'
            ],
            'size': [
                'size', 'big', 'small', 'large', 'compact', 'spacious',
                'dimensions', 'fit', 'space', 'room', 'tiny', 'huge',
                'perfect size', 'too big', 'too small'
            ],
            'comfort': [
                'comfort', 'comfortable', 'ergonomic', 'soft', 'firm',
                'cushion', 'support', 'padding', 'cozy', 'uncomfortable'
            ],
            'delivery': [
                'delivery', 'shipping', 'arrived', 'package', 'packaging',
                'fast shipping', 'slow delivery', 'damaged', 'box',
                'delivered', 'received'
            ],
            'customer_service': [
                'customer service', 'support', 'help', 'response', 'staff',
                'representative', 'helpful', 'rude', 'friendly', 'contact'
            ],
            'durability': [
                'durability', 'durable', 'last', 'lasting', 'wear', 'tear',
                'broke', 'broken', 'sturdy', 'reliable', 'falls apart'
            ]
        }
        
        # Sentiment indicators
        self.positive_words = {
            'excellent', 'amazing', 'great', 'love', 'perfect', 'awesome',
            'fantastic', 'wonderful', 'brilliant', 'outstanding', 'superb',
            'recommend', 'happy', 'satisfied', 'pleased', 'impressed'
        }
        
        self.negative_words = {
            'terrible', 'awful', 'hate', 'horrible', 'worst', 'bad',
            'disappointed', 'poor', 'useless', 'waste', 'regret',
            'broken', 'defective', 'faulty', 'cheap', 'flimsy'
        }
    
    def analyze_sentiment(self, text: str) -> str:
        """
        Analyze sentiment of review text.
        
        Args:
            text: Review text to analyze
            
        Returns:
            Sentiment: 'positive', 'negative', or 'neutral'
        """
        if not text:
            return 'neutral'
        
        text_lower = text.lower()
        words = set(re.findall(r'\b\w+\b', text_lower))
        
        positive_count = len(words.intersection(self.positive_words))
        negative_count = len(words.intersection(self.negative_words))
        
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'
    
    def calculate_keyword_relevance(self, text: str, keywords: List[str]) -> float:
        """
        Calculate how relevant a review is to given keywords.
        
        Args:
            text: Review text
            keywords: List of keywords to match
            
        Returns:
            Relevance score (0-1)
        """
        if not text or not keywords:
            return 0.0
        
        text_lower = text.lower()
        total_matches = 0
        
        for keyword in keywords:
            keyword_lower = keyword.lower()
            # Count exact matches and partial matches
            exact_matches = len(re.findall(r'\b' + re.escape(keyword_lower) + r'\b', text_lower))
            partial_matches = text_lower.count(keyword_lower) - exact_matches
            
            # Weight exact matches higher
            total_matches += exact_matches * 2 + partial_matches
        
        # Normalize by text length and keyword count
        text_length = len(text.split())
        max_possible_score = len(keywords) * 2
        
        if text_length == 0 or max_possible_score == 0:
            return 0.0
        
        # Calculate relevance score
        relevance = min(total_matches / max_possible_score, 1.0)
        return relevance
    
    def categorize_review(self, text: str) -> List[str]:
        """
        Categorize review based on content.
        
        Args:
            text: Review text to categorize
            
        Returns:
            List of matching categories
        """
        if not text:
            return []
        
        text_lower = text.lower()
        matching_categories = []
        
        for category, keywords in self.criteria_keywords.items():
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    matching_categories.append(category)
                    break  # Found match for this category
        
        return matching_categories
    
    def filter_reviews(self, reviews: List[Dict[str, Any]], filter_config: ReviewFilter) -> List[Dict[str, Any]]:
        """
        Filter and sort reviews based on criteria.
        
        Args:
            reviews: List of review dictionaries
            filter_config: Filtering configuration
            
        Returns:
            Filtered and sorted reviews
        """
        if not reviews:
            return []
        
        filtered_reviews = []
        
        for review in reviews:
            # Skip if review doesn't meet basic criteria
            rating = float(review.get('rating', 0))
            if rating < filter_config.min_rating or rating > filter_config.max_rating:
                continue
            
            review_text = str(review.get('review_text', ''))
            
            # Sentiment filtering
            if filter_config.sentiment:
                review_sentiment = self.analyze_sentiment(review_text)
                if review_sentiment != filter_config.sentiment:
                    continue
            
            # Enhanced review data
            enhanced_review = review.copy()
            enhanced_review['sentiment'] = self.analyze_sentiment(review_text)
            enhanced_review['categories'] = self.categorize_review(review_text)
            
            # Keyword relevance
            if filter_config.keywords:
                relevance = self.calculate_keyword_relevance(review_text, filter_config.keywords)
                enhanced_review['keyword_relevance'] = relevance
                enhanced_review['relevance_percentage'] = f"{relevance * 100:.1f}%"
                
                # Only include reviews with some relevance
                if relevance > 0.1:  # 10% threshold
                    filtered_reviews.append(enhanced_review)
            else:
                enhanced_review['keyword_relevance'] = 1.0
                enhanced_review['relevance_percentage'] = "100%"
                filtered_reviews.append(enhanced_review)
            
            # Category filtering
            if filter_config.categories:
                review_categories = set(enhanced_review['categories'])
                filter_categories = set(filter_config.categories)
                if not review_categories.intersection(filter_categories):
                    continue
        
        # Sort reviews
        filtered_reviews = self._sort_reviews(filtered_reviews, filter_config.sort_by)
        
        # Limit results
        return filtered_reviews[:filter_config.limit]
    
    def _sort_reviews(self, reviews: List[Dict[str, Any]], sort_by: str) -> List[Dict[str, Any]]:
        """Sort reviews by specified criteria."""
        if sort_by == 'relevance':
            return sorted(reviews, key=lambda r: r.get('keyword_relevance', 0), reverse=True)
        elif sort_by == 'rating':
            return sorted(reviews, key=lambda r: float(r.get('rating', 0)), reverse=True)
        elif sort_by == 'date':
            return sorted(reviews, key=lambda r: r.get('date', ''), reverse=True)
        elif sort_by == 'length':
            return sorted(reviews, key=lambda r: len(str(r.get('review_text', ''))), reverse=True)
        else:
            return reviews
    
    def get_review_insights(self, reviews: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate insights from filtered reviews.
        
        Args:
            reviews: List of review dictionaries
            
        Returns:
            Insights dictionary
        """
        if not reviews:
            return {}
        
        # Category distribution
        all_categories = []
        sentiments = []
        ratings = []
        
        for review in reviews:
            all_categories.extend(review.get('categories', []))
            sentiments.append(review.get('sentiment', 'neutral'))
            ratings.append(float(review.get('rating', 0)))
        
        category_counts = Counter(all_categories)
        sentiment_counts = Counter(sentiments)
        
        return {
            'total_reviews': len(reviews),
            'average_rating': sum(ratings) / len(ratings) if ratings else 0,
            'category_breakdown': dict(category_counts.most_common()),
            'sentiment_breakdown': dict(sentiment_counts),
            'top_categories': [cat for cat, _ in category_counts.most_common(5)],
            'rating_distribution': {
                '5_star': len([r for r in ratings if r >= 4.5]),
                '4_star': len([r for r in ratings if 3.5 <= r < 4.5]),
                '3_star': len([r for r in ratings if 2.5 <= r < 3.5]),
                '2_star': len([r for r in ratings if 1.5 <= r < 2.5]),
                '1_star': len([r for r in ratings if r < 1.5])
            }
        }


def create_filter_from_params(request_args: Dict[str, Any]) -> ReviewFilter:
    """
    Create ReviewFilter from request parameters.
    
    Args:
        request_args: Request arguments dictionary
        
    Returns:
        ReviewFilter configuration
    """
    keywords = []
    if request_args.get('keywords'):
        keywords = [k.strip() for k in str(request_args['keywords']).split(',')]
    
    categories = []
    if request_args.get('categories'):
        categories = [c.strip() for c in str(request_args['categories']).split(',')]
    
    return ReviewFilter(
        keywords=keywords,
        categories=categories,
        min_rating=float(request_args.get('min_rating', 0)),
        max_rating=float(request_args.get('max_rating', 5)),
        sentiment=request_args.get('sentiment'),
        sort_by=request_args.get('sort_by', 'relevance'),
        limit=int(request_args.get('limit', 50))
    )
