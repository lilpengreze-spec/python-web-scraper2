# Universal Review Scraper

🚀 **Production-ready Python web scraper** that collects real-time reviews from **10+ major platforms** including Yelp, Amazon, Walmart, Target, and more!

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/XXXXXX)

## ✨ Features

- **🌍 Universal Scraping**: Supports 10+ major retail/review platforms
- **🔄 Real-time Data**: Immediate scraping with live review comments and ratings
- **🔗 Direct Links**: Each review includes clickable links back to the original source
- **⭐ Star Ratings**: Visual star displays (⭐⭐⭐⭐⭐) with numerical ratings
- **🔀 API Fallbacks**: Uses official APIs where available, web scraping as fallback
- **⚡ Flask API**: RESTful endpoints with JSON responses
- **🛡️ Production Ready**: Comprehensive error handling, rate limiting, and logging
- **☁️ Multi-Platform Deploy**: Railway, Replit, and local deployment support
- **📊 Rich Data**: Reviewer names, ratings, comments, dates, and source links

## 🏪 Supported Platforms

| Platform | Domain | Review Types |
|----------|--------|-------------|
| **Yelp** | yelp.com | Restaurant & business reviews |
| **Amazon** | amazon.com | Product reviews |
| **Walmart** | walmart.com | Product reviews |
| **Target** | target.com | Product reviews |
| **Best Buy** | bestbuy.com | Electronics reviews |
| **Home Depot** | homedepot.com | Tool & hardware reviews |
| **Lowe's** | lowes.com | Home improvement reviews |
| **Costco** | costco.com | Bulk product reviews |
| **eBay** | ebay.com | Seller & product reviews |
| **Etsy** | etsy.com | Handmade product reviews |

## 🏗️ Architecture

```
├── app.py                     # Main Flask application
├── scrapers/
│   ├── yelp_scraper.py       # Yelp API + scraping
│   ├── amazon_scraper.py     # Amazon scraping
│   ├── walmart_scraper.py    # Walmart scraping
│   └── universal_scraper.py  # Universal multi-platform scraper
├── utils/
│   ├── validators.py         # Input validation
│   └── helpers.py           # Formatting & utilities
├── requirements.txt          # Python dependencies
├── Procfile                 # Railway deployment
├── railway.json             # Railway configuration
└── .replit                  # Replit configuration
```

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd review-scraper
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables** (optional)
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Test the API**
   ```bash
   curl http://localhost:5000/health
   ```

### Railway Deployment

1. **Connect to Railway**
   - Click the "Deploy on Railway" button above
   - Or manually connect your GitHub repository

2. **Set Environment Variables** (optional)
   ```
   YELP_API_KEY=your_yelp_api_key
   AMAZON_ACCESS_KEY=your_amazon_access_key
   AMAZON_SECRET_KEY=your_amazon_secret_key
   AMAZON_PARTNER_TAG=your_amazon_partner_tag
   ```

3. **Deploy**
   - Railway will automatically detect the configuration and deploy

## 📡 API Endpoints

### Health Check
```http
GET /health
```

### Start Scraping
```http
POST /scrape
Content-Type: application/json

{
  "yelp_business_id": "garaje-san-francisco",
  "amazon_asin": "B08N5WRWNW",
  "refresh_interval": 300
}
```

### Get Latest Data
```http
GET /latest
```

### Stop Background Scraping
```http
POST /stop
```

## 📊 Response Format

```json
{
  "timestamp": "2025-08-08T12:00:00Z",
  "status": "success",
  "yelp_reviews": [
    {
      "reviewer_name": "John D.",
      "rating": 5,
      "review_text": "Amazing food and great service!",
      "date": "2025-08-01",
      "review_url": "https://www.yelp.com/biz/garaje-san-francisco",
      "source": "yelp_scraping"
    }
  ],
  "amazon_reviews": [
    {
      "reviewer_name": "TechLover123",
      "rating": 4.0,
      "review_text": "Great sound quality for the price.",
      "date": "August 3, 2025",
      "review_url": "https://www.amazon.com/dp/B08N5WRWNW",
      "helpful_votes": "15 people found this helpful",
      "source": "amazon_scraping"
    }
  ],
  "statistics": {
    "total_reviews": 2,
    "yelp_review_count": 1,
    "amazon_review_count": 1,
    "has_errors": false
  }
}
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `YELP_API_KEY` | Yelp Fusion API key | No (falls back to scraping) |
| `AMAZON_ACCESS_KEY` | Amazon Product Advertising API access key | No (uses scraping only) |
| `AMAZON_SECRET_KEY` | Amazon Product Advertising API secret key | No |
| `AMAZON_PARTNER_TAG` | Amazon associate partner tag | No |
| `FLASK_ENV` | Flask environment (development/production) | No |
| `LOG_LEVEL` | Logging level (DEBUG/INFO/WARNING/ERROR) | No |

### Input Examples

**Yelp:**
- Business ID: `garaje-san-francisco`
- URL: `https://www.yelp.com/biz/garaje-san-francisco`

**Amazon:**
- ASIN: `B08N5WRWNW`
- URL: `https://www.amazon.com/dp/B08N5WRWNW`

## 🛡️ Error Handling

The scraper includes comprehensive error handling for:
- ❌ Invalid URLs or IDs
- 🚫 Rate limiting and anti-bot measures
- 🌐 Network timeouts and connection errors
- 🔑 Missing or invalid API credentials
- 📄 HTML parsing failures
- ⚠️ Partial data extraction

## 🧪 Testing

Run the test suite:
```bash
python test_scraper.py
```

Run the demo:
```bash
python demo.py
```

## 📋 Requirements

- Python 3.11+
- Flask 3.0+
- requests 2.31+
- BeautifulSoup4 4.12+
- See `requirements.txt` for full dependencies

## ⚠️ Important Notes

1. **Anti-bot Measures**: Both Yelp and Amazon have sophisticated anti-bot protections. Real scraping may be limited.

2. **API Limitations**: 
   - Amazon's Product Advertising API doesn't provide review data
   - Yelp's API has rate limits and requires approval

3. **Legal Compliance**: Ensure compliance with terms of service and robots.txt files

4. **Rate Limiting**: Built-in delays and retry logic to respect server resources

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- 📧 Issues: [GitHub Issues](../../issues)
- 📖 Documentation: This README
- 🚀 Deployment: [Railway Documentation](https://docs.railway.app)

---

**⭐ Star this repository if you find it useful!**
