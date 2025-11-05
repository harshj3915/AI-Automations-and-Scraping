"""
LinkedIn Profile Scraper
Uses saved browser session to scrape LinkedIn profiles
"""

import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
import config

class LinkedInScraper:
    def __init__(self):
        """Initialize the scraper with saved browser profile"""
        self.driver = None
        self.profiles_data = []
        
    def setup_driver(self):
        """Setup Chrome driver with saved profile"""
        print("\n🔧 Setting up Chrome driver with saved profile...")
        
        if not os.path.exists(config.USER_DATA_DIR):
            raise Exception(
                f"Profile directory not found: {config.USER_DATA_DIR}\n"
                "Please run 'python setup.py' first to set up your browser session."
            )
        
        chrome_options = Options()
        chrome_options.add_argument(f"user-data-dir={os.path.abspath(config.USER_DATA_DIR)}")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        if config.HEADLESS:
            chrome_options.add_argument("--headless")
        
        ua = UserAgent()
        user_agent = ua.random
        chrome_options.add_argument(f'user-agent={user_agent}')
        
        try:
            from webdriver_manager.core.os_manager import ChromeType
            
            print("   Installing/updating ChromeDriver...")
            try:
                driver_path = ChromeDriverManager().install()
                
                if not driver_path.endswith('chromedriver.exe'):
                    driver_dir = os.path.dirname(driver_path)
                    found = False
                    for root, dirs, files in os.walk(driver_dir):
                        if 'chromedriver.exe' in files:
                            driver_path = os.path.join(root, 'chromedriver.exe')
                            found = True
                            break
                    
                    if not found:
                        parent_dir = os.path.dirname(driver_dir)
                        for root, dirs, files in os.walk(parent_dir):
                            if 'chromedriver.exe' in files:
                                driver_path = os.path.join(root, 'chromedriver.exe')
                                break
                
            except Exception as e:
                print(f"   Warning: {str(e)}")
                print("   Trying alternative method...")
                driver_path = ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install()
            
            service = Service(driver_path)
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
        except Exception as e:
            raise Exception(f"Failed to initialize Chrome driver: {str(e)}")
        
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print(" Chrome driver ready!")
        
    def scroll_page(self):
        """Scroll the page to load all dynamic content"""
        try:
            time.sleep(2)
            
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            
            for i in range(3):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(config.SCROLL_PAUSE_TIME)
                
                # Wait for lazy-loaded content
                try:
                    WebDriverWait(self.driver, 5).until(
                        lambda driver: driver.execute_script("return document.readyState") == "complete"
                    )
                except TimeoutException:
                    pass
                
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
            
            time.sleep(1)
                
        except Exception as e:
            print(f"   Warning: Error while scrolling: {str(e)}")
    
    def extract_text_safe(self, by, selector, default="N/A"):
        """Safely extract text from an element"""
        try:
            element = self.driver.find_element(by, selector)
            text = element.text.strip() if element.text else default
            if text != default:
                text = ' '.join(text.split())
            return text
        except NoSuchElementException:
            return default
        except Exception:
            return default
    
    def clean_text(self, text):
        """Clean and normalize text by removing extra whitespace, newlines, and duplicates"""
        if not text or text == "N/A":
            return "N/A"
        
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        cleaned_lines = []
        prev_line = None
        for line in lines:
            if line != prev_line:
                cleaned_lines.append(line)
                prev_line = line
        
        text = ' '.join(cleaned_lines)
        text = ' '.join(text.split())
        
        return text
    
    def extract_profile_data(self, url):
        """Extract data from a LinkedIn profile"""
        print(f"\n📄 Scraping: {url}")
        
        try:
           

            # Navigate to the profile URL
            self.driver.get(url)
            
            # Wait for profile page to load - check for multiple elements
            try:
                WebDriverWait(self.driver, 20).until(
                    lambda driver: driver.execute_script("return document.readyState") == "complete"
                )
                WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.TAG_NAME, "main"))
                )
                print("    Profile page loaded")
            except TimeoutException:
                print("    Timeout waiting for profile page")
            
            time.sleep(config.WAIT_TIME)
            
            # Scroll to load all content
            self.scroll_page()
            
            # Check if we're still logged in
            if "authwall" in self.driver.current_url or "login" in self.driver.current_url:
                print("    Not logged in! Please run setup.py again.")
                return None
            
            # Extract profile data
            profile_data = {
                'url': url,
                'name': 'N/A',
                'headline': 'N/A',
                'location': 'N/A',
                'about': 'N/A',
                'followers': 'N/A',
                'connections': 'N/A',
                'experience': 'N/A',
                'education': 'N/A',
            }
            
            name_selectors = [
                "h1.text-heading-xlarge",
                "h1.inline.t-24.v-align-middle.break-words",
                "h1.top-card-layout__title"
            ]
            for selector in name_selectors:
                name = self.extract_text_safe(By.CSS_SELECTOR, selector)
                if name != "N/A":
                    profile_data['name'] = name
                    break
            
            headline_selectors = [
                "div.text-body-medium.break-words",
                "h2.mt1.t-18.t-black.t-normal",
                "div.top-card-layout__headline"
            ]
            for selector in headline_selectors:
                headline = self.extract_text_safe(By.CSS_SELECTOR, selector)
                if headline != "N/A":
                    profile_data['headline'] = headline
                    break
            
            location_selectors = [
                "span.text-body-small.inline.t-black--light.break-words",
                "span.top-card-layout__location"
            ]
            for selector in location_selectors:
                location = self.extract_text_safe(By.CSS_SELECTOR, selector)
                if location != "N/A":
                    profile_data['location'] = location
                    break
            
            try:
                # Try multiple selectors for about section
                about_selectors = [
                    "div.display-flex.ph5.pv3",
                    "div.pv-shared-text-with-see-more",
                    "div.inline-show-more-text",
                    "section[data-section='summary'] div.pv-shared-text-with-see-more"
                ]
                for selector in about_selectors:
                    try:
                        about_elem = self.driver.find_element(By.CSS_SELECTOR, selector)
                        about_text = about_elem.text.strip()
                        if about_text:
                            profile_data['about'] = self.clean_text(about_text)
                            break
                    except:
                        continue
            except Exception as e:
                pass
            
            # Extract followers/connections - Try multiple approaches
            try:
                # Look for connection count
                connection_selectors = [
                    "span.t-bold",  # Common selector for connections like "500+"
                    "span.t-black--light span.t-bold",
                    "li.pv-top-card--list-bullet span.t-bold",
                    "span.link-without-visited-state span"
                ]
                
                for selector in connection_selectors:
                    try:
                        conn_elems = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        for conn_elem in conn_elems:
                            conn_text = conn_elem.text.strip()
                            # Check if it contains numbers and connection-related text
                            if conn_text and any(char.isdigit() for char in conn_text):
                                profile_data['connections'] = self.clean_text(conn_text)
                                break
                        if profile_data['connections'] != "N/A":
                            break
                    except:
                        continue
            except:
                pass
            
            # Extract followers - Try multiple approaches
            try:
                # Look for follower count
                follower_selectors = [
                    "span.pvs-entity__caption-wrapper",
                    "span.follower-count",
                    "div.pv-top-card--list-bullet span",
                    "span[aria-label*='follower']"
                ]
                
                for selector in follower_selectors:
                    try:
                        follower_elems = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        for follower_elem in follower_elems:
                            follower_text = follower_elem.text.strip()
                            # Check if it contains "follower" keyword and numbers
                            if follower_text and 'follower' in follower_text.lower() and any(char.isdigit() for char in follower_text):
                                # Extract just the number and "followers" part
                                profile_data['followers'] = self.clean_text(follower_text)
                                break
                        if profile_data['followers'] != "N/A":
                            break
                    except:
                        continue
            except:
                pass
            
            # Extract experience (first position only, cleaned)
            try:
                experience_section = self.driver.find_element(By.ID, "experience")
                exp_parent = experience_section.find_element(By.XPATH, "..")
                exp_items = exp_parent.find_elements(By.CSS_SELECTOR, "li.artdeco-list__item")
                
                if exp_items:
                    first_exp_elem = exp_items[0]
                    
                    try:
                        title = first_exp_elem.find_element(By.CSS_SELECTOR, "div[aria-hidden='true'] span[aria-hidden='true']").text.strip()
                        company = ""
                        duration = ""
                        
                        try:
                            company_elem = first_exp_elem.find_element(By.CSS_SELECTOR, "span.t-14.t-normal span[aria-hidden='true']")
                            company = company_elem.text.strip()
                        except:
                            pass
                        
                        try:
                            duration_elem = first_exp_elem.find_element(By.CSS_SELECTOR, "span.t-14.t-normal.t-black--light span[aria-hidden='true']")
                            duration = duration_elem.text.strip()
                        except:
                            pass
                        
                        exp_parts = [p for p in [title, company, duration] if p]
                        if exp_parts:
                            profile_data['experience'] = " | ".join(exp_parts)
                        else:
                            full_text = first_exp_elem.text.strip()
                            profile_data['experience'] = self.clean_text(full_text[:200])
                    except:
                        # Fallback to full text
                        full_text = first_exp_elem.text.strip()
                        profile_data['experience'] = self.clean_text(full_text[:200])
            except:
                pass
            
            # Extract education (first item only, cleaned)
            try:
                education_section = self.driver.find_element(By.ID, "education")
                edu_parent = education_section.find_element(By.XPATH, "..")
                edu_items = edu_parent.find_elements(By.CSS_SELECTOR, "li.artdeco-list__item")
                
                if edu_items:
                    first_edu_elem = edu_items[0]
                    
                    try:
                        school = first_edu_elem.find_element(By.CSS_SELECTOR, "div[aria-hidden='true'] span[aria-hidden='true']").text.strip()
                        degree = ""
                        years = ""
                        
                        try:
                            degree_elem = first_edu_elem.find_element(By.CSS_SELECTOR, "span.t-14.t-normal span[aria-hidden='true']")
                            degree = degree_elem.text.strip()
                        except:
                            pass
                        
                        try:
                            years_elem = first_edu_elem.find_element(By.CSS_SELECTOR, "span.t-14.t-normal.t-black--light span[aria-hidden='true']")
                            years = years_elem.text.strip()
                        except:
                            pass
                        
                        edu_parts = [p for p in [school, degree, years] if p]
                        if edu_parts:
                            profile_data['education'] = " | ".join(edu_parts)
                        else:
                            full_text = first_edu_elem.text.strip()
                            profile_data['education'] = self.clean_text(full_text[:200])
                    except:
                        full_text = first_edu_elem.text.strip()
                        profile_data['education'] = self.clean_text(full_text[:200])
            except:
                pass
            
            print(f"    Scraped: {profile_data['name']}")
            return profile_data
            
        except Exception as e:
            print(f"   ❌ Error scraping profile: {str(e)}")
            return None
    
    def scrape_profiles(self, urls):
        """Scrape multiple LinkedIn profiles"""
        print("\n" + "=" * 60)
        print("LinkedIn Profile Scraper")
        print("=" * 60)
        print(f"\nTotal profiles to scrape: {len(urls)}")
        
        self.setup_driver()
        
        # Navigate to LinkedIn homepage first
        self.driver.get("https://www.linkedin.com/feed/")
        
        # Wait for LinkedIn homepage to load (wait for navigation bar)
        try:
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            print("    LinkedIn homepage loaded")
        except TimeoutException:
            print("    Timeout waiting for LinkedIn homepage")
        
        time.sleep(10)

        for i, url in enumerate(urls, 1):
            print(f"\n[{i}/{len(urls)}]", end=" ")
            
            profile_data = self.extract_profile_data(url)
            
            if profile_data:
                self.profiles_data.append(profile_data)
            
            # Add delay between requests to avoid rate limiting
            if i < len(urls):
                wait_time = config.WAIT_TIME
                print(f"   ⏳ Waiting {wait_time} seconds before next profile...")
                time.sleep(wait_time)
        
        self.save_to_csv()
        
    def save_to_csv(self):
        """Save scraped data to CSV file"""
        if not self.profiles_data:
            print("\n No data to save!")
            return
        
        try:
            df = pd.DataFrame(self.profiles_data)
            df.to_csv(config.OUTPUT_CSV, index=False, encoding='utf-8-sig')
            
            print("\n" + "=" * 60)
            print("✅ Scraping completed!")
            print("=" * 60)
            print(f"Total profiles scraped: {len(self.profiles_data)}")
            print(f"Data saved to: {os.path.abspath(config.OUTPUT_CSV)}")
            print("\nColumns in CSV:")
            for col in df.columns:
                print(f"  - {col}")
            
        except Exception as e:
            print(f"\n❌ Error saving to CSV: {str(e)}")
    
    def close(self):
        """Close the browser"""
        if self.driver:
            try:
                self.driver.quit()
                print("\n Browser closed")
            except:
                pass

def main():
    """Main function to run the scraper"""
    scraper = LinkedInScraper()
    
    try:
        scraper.scrape_profiles(config.PROFILE_URLS)
    except KeyboardInterrupt:
        print("\n\n Scraping interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
    finally:
        scraper.close()

if __name__ == "__main__":
    main()
