# scraper/remoteok_scraper.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import time
import os

def scrape_remoteok(keyword="python"):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)

    jobs = []
    formatted_keyword = keyword.replace(" ", "+")
    url = f"https://remoteok.com/remote-{formatted_keyword}-jobs"
    print(f"🔍 Scraping: {url}")
    driver.get(url)
    time.sleep(5)  # allow JS to load

    rows = driver.find_elements(By.CSS_SELECTOR, "tr.job")

    for row in rows:
        try:
            title = row.find_element(By.TAG_NAME, "h2").text.strip()
            company = row.find_element(By.TAG_NAME, "h3").text.strip()
            location = row.find_element(By.CLASS_NAME, "location").text.strip()
            date_posted = row.find_element(By.TAG_NAME, "time").get_attribute("datetime")
            tag_elements = row.find_elements(By.CLASS_NAME, "tag")
            skills = ", ".join(tag.text.strip() for tag in tag_elements if tag.text.strip())

            jobs.append({
                "title": title,
                "company": company,
                "location": location,
                "date_posted": date_posted or "N/A",
                "skills": skills
            })
        except Exception as e:
            continue

    driver.quit()

    df = pd.DataFrame(jobs)
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/jobs.csv", index=False)
    print(f"📁 Saved {len(df)} jobs to data/jobs.csv")
    return df
