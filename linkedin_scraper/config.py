"""
Configuration file for LinkedIn scraper
"""

# List of LinkedIn profile URLs to scrape
PROFILE_URLS = [
    "https://www.linkedin.com/in/satyanadella/",
    "https://www.linkedin.com/in/pushkar-g-b837131aa/",
    # "https://www.linkedin.com/in/williamhgates/",
    # "https://www.linkedin.com/in/jeffweiner08/",
    # "https://www.linkedin.com/in/reid-hoffman-460b3b/",
    # "https://www.linkedin.com/in/arividh/",
    # "https://www.linkedin.com/in/sundarpichai/",
    # "https://www.linkedin.com/in/timcook/",
    # "https://www.linkedin.com/in/sherylsandberg/",
    # "https://www.linkedin.com/in/marissameyer/",
    # "https://www.linkedin.com/in/stevewozniak/",
    # "https://www.linkedin.com/in/ericschmidt/",
    # "https://www.linkedin.com/in/jackmaa/",
    # "https://www.linkedin.com/in/elonmusk/",
    # "https://www.linkedin.com/in/markzuckerberg/",
    # "https://www.linkedin.com/in/larrypage/",
    # "https://www.linkedin.com/in/ginni-rometty/",
    # "https://www.linkedin.com/in/travis-kalanick/",
    # "https://www.linkedin.com/in/melinda-gates/",
    # "https://www.linkedin.com/in/anne-wojcicki/",
    # "https://www.linkedin.com/in/brian-chesky/",
]

# Browser settings
USER_DATA_DIR = "./chrome_profile"
HEADLESS = False  # Set to True to run browser in background
WAIT_TIME = 5 
SCROLL_PAUSE_TIME = 2 

# Output settings
OUTPUT_CSV = "linkedin_profiles.csv"
