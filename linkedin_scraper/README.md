# LinkedIn Profile Scraper

A robust LinkedIn profile scraper that uses Selenium with persistent browser sessions to scrape profile data while avoiding detection.

## Features

- **Persistent Browser Session**: Login once, use the saved session for all scraping
- **Anti-Detection**: Uses various techniques to avoid LinkedIn's bot detection
- **Random User Agents**: Rotates user agents to appear as different browsers
- **Comprehensive Data Extraction**: Scrapes name, headline, location, about, experience, education, and more
- **CSV Export**: Automatically saves all scraped data to a CSV file
- **Error Handling**: Robust error handling with detailed logging
- **Rate Limiting**: Built-in delays to avoid triggering LinkedIn's rate limits

## Prerequisites

- Python 3.7 or higher
- Google Chrome browser installed
- A LinkedIn account (for login)

## Installation

1. **Navigate to the project directory:**
   ```bash
   cd linkedin_scraper
   ```

2. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Step 1: Setup Browser Session (One-time setup)

Run the setup script to create a persistent browser session:

```bash
python setup.py
```

**What happens:**
1. A Chrome browser window will open
2. Log in to your Google account
3. Navigate to LinkedIn and log in
4. Close the browser window
5. Your session will be saved in the `chrome_profile` folder

**Important:** You only need to do this once. The session will be reused for all future scraping.

### Step 2: Run the Scraper

After setting up your browser session, run the scraper:

```bash
python scraper.py
```

The scraper will:
- Use your saved session to access LinkedIn
- Scrape all profiles listed in `config.py`
- Save the data to `linkedin_profiles.csv`

## Configuration

Edit `config.py` to customize the scraper:

### Profile URLs
Add or modify LinkedIn profile URLs to scrape:
```python
PROFILE_URLS = [
    "https://www.linkedin.com/in/username1/",
    "https://www.linkedin.com/in/username2/",
    # Add more URLs...
]
```

### Scraper Settings
```python
HEADLESS = False          # Set to True to run browser in background
WAIT_TIME = 5            # Seconds to wait between profiles
SCROLL_PAUSE_TIME = 2    # Seconds to pause while scrolling
OUTPUT_CSV = "linkedin_profiles.csv"  # Output filename
```

## Output

The scraper generates a CSV file with the following columns:

| Column | Description |
|--------|-------------|
| url | LinkedIn profile URL |
| name | Person's full name |
| headline | Professional headline |
| location | Current location |
| about | About/summary section |
| followers | Number of followers (if visible) |
| connections | Connection information |
| experience | Most recent work experience |
| education | Most recent education |

## Project Structure

```
linkedin_scraper/
├── setup.py              # One-time setup script for browser session
├── scraper.py            # Main scraping script
├── config.py             # Configuration file
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── .gitignore           # Git ignore file
├── chrome_profile/      # Browser session data (created after setup)
└── linkedin_profiles.csv # Output data (created after scraping)
```

## How It Works

### 1. Session Persistence
- Chrome's user data directory is used to save cookies, cache, and login state
- This allows the scraper to reuse your login session without logging in every time
- Session data is stored in the `chrome_profile` folder

### 2. Anti-Detection Measures
- **Random User Agents**: Each session uses a different browser fingerprint
- **Webdriver Flag Removal**: Removes automation detection flags
- **Human-like Behavior**: Includes scrolling and realistic wait times
- **Session Reuse**: Appears as a normal logged-in user, not a bot

### 3. Data Extraction
- Uses multiple CSS selectors for reliability (LinkedIn often changes their HTML)
- Scrolls the page to load dynamic content
- Safely handles missing elements with default values
- Extracts comprehensive profile information

### 4. Rate Limiting
- Built-in delays between profile requests
- Configurable wait times to avoid triggering LinkedIn's anti-bot systems
- Graceful handling of rate limit responses

## Troubleshooting

### "Profile directory not found" Error
**Solution:** Run `python setup.py` first to create the browser session.

### Login Required / Auth Wall
**Solution:** 
1. Delete the `chrome_profile` folder
2. Run `python setup.py` again
3. Log in to LinkedIn again

### Chrome Driver Issues
**Solution:** The script automatically downloads the correct ChromeDriver. Ensure Chrome browser is installed and up to date.

### No Data Scraped
**Possible causes:**
- Not logged in (run setup.py again)
- LinkedIn changed their HTML structure (may need to update selectors)
- Rate limited by LinkedIn (increase WAIT_TIME in config.py)

### Profile Access Denied
**Solution:** Some profiles require connections or Premium. Try profiles that are publicly visible or profiles you're connected with.

## Best Practices

1. **Respect Rate Limits**: Don't scrape too many profiles too quickly
2. **Use Delays**: Keep WAIT_TIME at least 5 seconds
3. **Session Management**: Re-run setup.py if you encounter login issues
4. **Data Privacy**: Only scrape public profile data and respect LinkedIn's ToS
5. **Account Safety**: Use a test account if possible to avoid risking your main account

## Legal Disclaimer

This tool is for educational purposes only. Web scraping may violate LinkedIn's Terms of Service. Use at your own risk. Always:
- Respect robots.txt
- Don't overload servers
- Only scrape publicly available data
- Follow LinkedIn's Terms of Service
- Be aware of legal implications in your jurisdiction

## Tips for Success

1. **Test Account**: Consider using a test LinkedIn account
2. **Start Small**: Test with 2-3 profiles first
3. **Monitor Sessions**: If you get logged out, run setup.py again
4. **Increase Delays**: If rate limited, increase WAIT_TIME
5. **Public Profiles**: Scrape profiles that are fully public for best results
6. **Connection Requests**: Consider connecting with profiles you want to scrape

## Limitations

- LinkedIn actively works to prevent scraping
- Some profile data may require LinkedIn Premium
- Private profiles have limited visible information
- LinkedIn may rate limit or temporarily ban accounts that scrape excessively
- HTML structure changes may require selector updates

## Support

If you encounter issues:
1. Check the console output for specific error messages
2. Ensure Chrome browser is up to date
3. Verify you're logged in by running setup.py again
4. Try increasing WAIT_TIME in config.py
5. Check if LinkedIn has changed their HTML structure

## Future Enhancements

Potential improvements:
- Proxy rotation support
- More comprehensive data extraction
- Resume parsing
- Skills extraction
- Recommendations scraping
- Company page scraping
- Connection graph analysis

---

**Remember**: Always use this tool responsibly and in compliance with LinkedIn's Terms of Service and applicable laws.
