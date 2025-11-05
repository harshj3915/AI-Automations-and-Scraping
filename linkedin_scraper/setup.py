"""
Setup script to create a browser session and log in to Google/LinkedIn
Run this script first to set up your authenticated session.
"""

import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
import config

def setup_browser_session():
    """
    Opens a Chrome browser with persistent profile.
    User should log in to Google and then LinkedIn manually.
    The session will be saved for future use.
    """
    print("=" * 60)
    print("LinkedIn Scraper - Browser Setup")
    print("=" * 60)
    print("\nThis script will open a Chrome browser window.")
    print("Please follow these steps:")
    print("1. Log in to your Google account")
    print("2. Navigate to LinkedIn and log in")
    print("3. Once logged in, you can close the browser window")
    print("4. Your session will be saved for the scraper to use")
    print("\nPress Enter to continue...")
    input()

    if not os.path.exists(config.USER_DATA_DIR):
        os.makedirs(config.USER_DATA_DIR)
        print(f"\n✓ Created profile directory: {config.USER_DATA_DIR}")

    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument(f"user-data-dir={os.path.abspath(config.USER_DATA_DIR)}")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    ua = UserAgent()
    user_agent = ua.random
    chrome_options.add_argument(f'user-agent={user_agent}')
    
    # Disable webdriver detection
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    
    print("\n🌐 Opening Chrome browser...")
    print("   Installing/updating ChromeDriver...")
    
    try:
        # Initialize the Chrome driver with proper error handling
        from webdriver_manager.core.os_manager import ChromeType
        
        try:
            driver_path = ChromeDriverManager().install()
            print(f" ChromeDriver base path: {driver_path}")
            
            if not driver_path.endswith('chromedriver.exe'):
                driver_dir = os.path.dirname(driver_path)
                found = False
                for root, dirs, files in os.walk(driver_dir):
                    if 'chromedriver.exe' in files:
                        driver_path = os.path.join(root, 'chromedriver.exe')
                        print(f" Found chromedriver.exe at: {driver_path}")
                        found = True
                        break
                
                if not found:
                    parent_dir = os.path.dirname(driver_dir)
                    for root, dirs, files in os.walk(parent_dir):
                        if 'chromedriver.exe' in files:
                            driver_path = os.path.join(root, 'chromedriver.exe')
                            print(f" Found chromedriver.exe at: {driver_path}")
                            break
            
        except Exception as e:
            print(f"   Warning: ChromeDriver installation issue: {str(e)}")
            print("   Trying alternative method...")
            driver_path = ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install()
        
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Execute script to remove webdriver property
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        # Open Google
        driver.get("https://www.google.com")
        
        print("\n✓ Browser opened successfully!")
        print("\n" + "=" * 60)
        print("INSTRUCTIONS:")
        print("=" * 60)
        print("1. Log in to your Google account in the browser")
        print("2. After Google login, navigate to LinkedIn")
        print("3. Log in to LinkedIn")
        print("4. Once done, close the browser window")
        print("5. Your session data will be saved automatically")
        print("=" * 60)
        
        print("\nWaiting for you to complete login and close the browser...")
        
        while True:
            try:
                # Check if browser is still open
                _ = driver.current_url
                time.sleep(2)
            except:
                # Browser was closed
                break
        
        print("\n✓ Browser closed. Session saved!")
        print(f"✓ Profile data saved in: {os.path.abspath(config.USER_DATA_DIR)}")
        print("\nYou can now run 'python scraper.py' to scrape LinkedIn profiles.")
        
    except Exception as e:
        print(f"\nX Error during setup: {str(e)}")
        print("\nTroubleshooting tips:")
        print("- Make sure Chrome browser is installed")
        print("- Check your internet connection")
        print("- Try running the script again")
        print("\nAlternative solution:")
        print("- Try updating Chrome to the latest version")
        print("- Run: pip install --upgrade selenium webdriver-manager")
        print("- If using 32-bit Python, try 64-bit Python instead")
        
        import sys
        print(f"\nSystem info:")
        print(f"- Python: {sys.version}")
        print(f"- Architecture: {sys.maxsize > 2**32 and '64-bit' or '32-bit'}")
        
    finally:
        try:
            driver.quit()
        except:
            pass

if __name__ == "__main__":
    setup_browser_session()
