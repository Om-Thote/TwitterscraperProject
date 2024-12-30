from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from pymongo import MongoClient
import uuid
import datetime

# Your ProxyMesh URL
proxy = "http://Aishwaryacdry:Aish2008@proxy.proxymesh.com:31280"  
chrome_options = Options()
chrome_options.add_argument(f'--proxy-server={proxy}')

# Setup WebDriver
chromedriver_path = r"C:\path_to_chromedriver\chromedriver.exe"  
service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open Twitter and log in
driver.get("https://twitter.com/login")
time.sleep(2)

username = driver.find_element(By.NAME, "text")
username.send_keys("Aishwaryacdry")  
username.send_keys(Keys.RETURN)
time.sleep(2)

password = driver.find_element(By.NAME, "password")
password.send_keys("Aish2008")  
password.send_keys(Keys.RETURN)
time.sleep(5)

# Navigate to "Trending" section
driver.get("https://twitter.com/explore/tabs/trending")
time.sleep(3)

# Scrape top 5 trending topics
trends = driver.find_elements(By.XPATH, '//div[@data-testid="trend"]')
trend_list = [trend.text for trend in trends[:5]]

# Close the driver
driver.quit()

# Store data in MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client["twitter_data"]
collection = db["trends"]

trend_data = {
    "_id": str(uuid.uuid4()),  # Unique ID for each entry
    "trend1": trend_list[0],
    "trend2": trend_list[1],
    "trend3": trend_list[2],
    "trend4": trend_list[3],
    "trend5": trend_list[4],
    "timestamp": datetime.datetime.now(),
    "ip_address": proxy
}
collection.insert_one(trend_data)
