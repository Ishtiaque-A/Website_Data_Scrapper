# scraper/utils.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
import time

def scrape_title(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        time.sleep(2)  # Wait for the page to load; adjust as needed
        title = driver.title
        driver.quit()
        return title
    except WebDriverException as e:
        print(f"Error scraping {url}: {e}")
        return None
