from flask import Flask, render_template, request, redirect, url_for
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import socket
import random

app = Flask(__name__)

# Function to set up Selenium WebDriver
def setup_driver():
    driver = webdriver.Chrome()
    return driver

def get_random_proxy():
    f = open('proxies.txt', 'r')
    lines = f.readlines()
    f.close()
    return random.choice(lines).strip()

# Function to fetch trending topics using Selenium
def fetch_trending_topics():
    driver = setup_driver()
    result_dict = {}
    try:
        driver.get("https://x.com/login")

        # Login process (replace with actual credentials)
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='text']"))
        ).send_keys("upenderlakhwan")
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']"))
        ).click()
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='password']"))
        ).send_keys("Upender9@")
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Log in']"))
        ).click()

        # Wait for homepage load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid='primaryColumn']"))
        )
        driver.get("https://x.com/explore/tabs/trending")

        # Wait for trending section and extract spans
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid='cellInnerDiv']"))
        )
        spans = driver.find_elements(By.TAG_NAME, "span")

        # Filter data
        unwanted_keywords = ["What's happening", "Trending in India", "·", "show more"]
        filtered_spans = [span.text for span in spans if not any(keyword in span.text.lower() for keyword in unwanted_keywords)]
        filtered_data = [item for item in filtered_spans if item]
        entertainment_index = filtered_data.index('Entertainment')
        filtered_data = filtered_data[entertainment_index + 1:]

        i = 1
        temp = []
        for item in filtered_data[:20]:
            if item.isdigit() and temp:
                result_dict[i] = temp
                temp = []
                i += 1
            temp.append(item)

        if temp:
            result_dict[i] = temp

    finally:
        driver.quit()

    return result_dict

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run-script')
def run_script():
    trending_topics = fetch_trending_topics()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ip_address = get_random_proxy()

    # Prepare data for display
    # trend_names = [details[1] for details in trending_topics.values()[:5]]
    trend_names = [details for details in list(trending_topics.values())[:5]]
    
    print(trend_names)
    return render_template(
        'result.html',
        datetime=now,
        ip=ip_address,
        trends=trend_names
    )

if __name__ == '__main__':
    app.run(debug=True)
