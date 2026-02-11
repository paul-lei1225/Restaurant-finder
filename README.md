# 🍽️ Restaurant Finder & Reservation Suggester

A comprehensive Python application that helps you discover restaurants and find the best reservation times based on your preferences.

## 📋 Project Description

Restaurant Finder is an interactive command-line application that allows users to:
- Search and filter restaurants by cuisine, rating, price range, and distance
- Get personalized restaurant recommendations
- View suggested reservation times based on availability
- Manage a local database of restaurant information

**Note:** This application is designed for educational purposes and demonstrates web scraping concepts, database management, and recommendation algorithms. For production use, please utilize official APIs from Yelp, Google Places, OpenTable, and other services.

## ✨ Features

- **🔍 Smart Restaurant Search**: Filter by cuisine type, rating, price range, and distance
- **🎯 Personalized Recommendations**: Get tailored suggestions based on your preferences
- **⏰ Availability Suggestions**: View optimal reservation times
- **💾 Local Database**: SQLite database for storing restaurant data
- **📊 Cuisine Statistics**: See available restaurant types at a glance
- **🎨 Beautiful CLI Interface**: User-friendly command-line interface with emoji icons
- **📝 Sample Data**: Pre-loaded with 15 sample restaurants for immediate testing

## 🚀 Installation Instructions

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/paul-lei1225/Restaurant-finder.git
   cd Restaurant-finder
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```

That's it! The application will automatically initialize the database and load sample data on first run.

## 📖 Usage Guide

When you run the application, you'll see a menu with the following options:

### 1. Scrape Restaurants in a Location
**Note:** This is a mock implementation. For real data, use official APIs.
- Educational demonstration of web scraping concepts
- Shows legal and ethical considerations
- Recommends using Yelp Fusion API or Google Places API

### 2. Update Availability Data
- Updates available reservation times for restaurants
- Currently uses mock/estimated data
- For production, integrate with OpenTable, Resy, or other reservation APIs

### 3. Get Restaurant Recommendations ⭐
This is the main feature! Enter your preferences:
- **Location**: Your current location (e.g., "San Francisco, CA")
- **Cuisine**: Preferred cuisine type or "any"
- **Minimum Rating**: Filter by rating (1-5 stars)
- **Price Range**: $, $$, $$$, or $$$$
- **Max Distance**: How far you're willing to travel (in miles)

The app will display ranked recommendations with:
- Restaurant name, rating, and price range
- Address and distance from you
- Phone number and hours
- Suggested reservation times

### 4. Search by Cuisine Type
- Browse restaurants by specific cuisine
- See all available cuisine types with counts
- View detailed information for each restaurant

### 5. View All Saved Restaurants
- See the complete list of restaurants in your database
- View full details including contact info and hours

### 6. Clear Database
- Remove all restaurant and availability data
- Useful for starting fresh

### 7. Exit
- Safely exit the application

## 🎯 Example Usage

```
==============================
Restaurant Finder & Reservation Suggester
==============================
Enter your choice (1-7): 3

=== Get Restaurant Recommendations ===
Enter your location: San Francisco, CA
Enter preferred cuisine (or 'any'): Italian
Enter minimum rating (1-5): 4.0
Enter price range ($ - $$$$): $$
Enter max distance in miles: 5

🔍 Searching for restaurants...

✓ Found 2 recommendations:

1. ⭐ Trattoria Romana - 4.5★ - $$
   📍 123 North Beach, San Francisco, CA 94133
   📏 1.2 mi away
   🍽️  Italian
   📞 (415) 555-0123
   
   Suggested Times (Today):
   • 6:00 PM ✓ Available (Less busy)
   • 6:30 PM ✓ Available (Less busy)
   • 8:00 PM ✓ Available

2. ⭐ Pasta Milano - 4.3★ - $$
   📍 456 Mission St, San Francisco, CA 94105
   📏 2.3 mi away
   🍽️  Italian
   📞 (415) 555-0456
   
   Suggested Times (Today):
   • 6:30 PM ✓ Available (Less busy)
   • 7:00 PM ✓ Available
   • 8:30 PM ✓ Available
```

## ⚙️ Configuration

Configuration settings are located in `config/settings.py`:

- **Database Settings**: SQLite database location
- **Scraping Settings**: Rate limits, timeouts, user agents
- **Default Preferences**: Default cuisine types, ratings, distances
- **Sample Data**: Pre-configured restaurant data for testing

You can modify these settings to customize the application behavior.

## 🏗️ Project Structure

```
restaurant-finder/
├── README.md
├── requirements.txt
├── .gitignore
├── config/
│   └── settings.py          # Configuration settings
├── src/
│   ├── __init__.py
│   ├── scrapers/
│   │   ├── __init__.py
│   │   ├── base_scraper.py      # Abstract base scraper class
│   │   ├── yelp_scraper.py      # Yelp scraper (mock)
│   │   └── google_maps_scraper.py  # Google Maps scraper (mock)
│   ├── database/
│   │   ├── __init__.py
│   │   ├── models.py            # SQLAlchemy database models
│   │   └── db_manager.py        # Database operations
│   ├── recommender/
│   │   ├── __init__.py
│   │   └── suggestion_engine.py # Recommendation algorithms
│   └── utils/
│       ├── __init__.py
│       └── helpers.py           # Utility functions
├── main.py                     # Main CLI application
└── tests/
    ├── __init__.py
    ├── test_helpers.py         # Tests for utility functions
    └── test_database.py        # Tests for database operations
```

## 🧪 Testing

Run the test suite:

```bash
python -m unittest discover tests
```

Run specific test files:

```bash
python -m unittest tests.test_helpers
python -m unittest tests.test_database
```

## ⚖️ Legal Disclaimer

**⚠️ IMPORTANT - PLEASE READ:**

This application is intended for **educational and personal use only**. Please be aware of the following:

### Web Scraping
- **Check Terms of Service**: Always review and comply with a website's Terms of Service before scraping
- **Use Official APIs**: Whenever possible, use official APIs instead of scraping:
  - [Yelp Fusion API](https://www.yelp.com/developers)
  - [Google Places API](https://developers.google.com/maps/documentation/places/web-service)
- **Respect robots.txt**: The application checks robots.txt files before scraping
- **Rate Limiting**: Implements delays between requests to avoid overloading servers
- **Not for Commercial Use**: Do not use scraped data for commercial purposes without permission

### Data Usage
- Mock implementations are used by default to demonstrate concepts
- Real data collection requires proper API keys and agreements
- Store and handle user data responsibly and in compliance with privacy laws

### Reservation Systems
- Integration with reservation systems (OpenTable, Resy, etc.) requires official API access
- Do not attempt to automate reservations without authorization
- Respect reservation system terms of service

**By using this application, you agree to use it responsibly and in compliance with all applicable laws and terms of service.**

## 🔮 Future Improvements

Potential enhancements for the project:

### Integration & APIs
- [ ] Integration with real reservation APIs (OpenTable, Resy)
- [ ] Yelp Fusion API implementation for live restaurant data
- [ ] Google Places API for location and business information
- [ ] Real-time availability checking

### Features
- [ ] Web interface using Flask or Django
- [ ] User accounts and saved preferences
- [ ] Favorite restaurants list
- [ ] Reservation history tracking
- [ ] Email notifications for availability
- [ ] SMS alerts for reservation confirmations
- [ ] Calendar integration

### Filters & Search
- [ ] Dietary filters (vegetarian, vegan, gluten-free, kosher, halal)
- [ ] Atmosphere/ambiance filters (romantic, family-friendly, quiet)
- [ ] Parking availability
- [ ] Accessibility information
- [ ] Review sentiment analysis
- [ ] Photo galleries

### Data & Analytics
- [ ] Restaurant comparison tool
- [ ] Price trends over time
- [ ] Popular times analysis
- [ ] Peak vs. off-peak pricing
- [ ] Wait time predictions

### Technical Enhancements
- [ ] PostgreSQL database support for production
- [ ] Redis caching for improved performance
- [ ] Async/await for concurrent operations
- [ ] Docker containerization
- [ ] CI/CD pipeline
- [ ] Mobile app (iOS/Android)

## 🤝 Contributing

This is an educational project. If you'd like to contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

Please ensure your code follows the existing style and includes appropriate documentation.

## 📄 License

This project is provided for educational purposes. Please respect all applicable licenses and terms of service when using or extending this code.

## 🙏 Acknowledgments

- Thanks to the Python community for excellent libraries (SQLAlchemy, BeautifulSoup, requests)
- Yelp and Google for inspiration on restaurant discovery features
- OpenTable and Resy for reservation system concepts

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Review existing documentation
- Check configuration settings

---

**Remember:** Always use official APIs for production applications and respect website terms of service. This project is for learning and demonstration purposes only.

Enjoy finding your next great meal! 🍕🍜🍔🍱