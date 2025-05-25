# scraper/remoteok_scraper.py

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def scrape_remoteok(keyword="python"):
    formatted_keyword = keyword.replace(" ", "-").lower()
    url = f"https://remoteok.com/remote-{formatted_keyword}-jobs"
    print(f"🔍 Scraping: {url}")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve page, status code: {response.status_code}")
        return pd.DataFrame()

    soup = BeautifulSoup(response.text, "html.parser")
    jobs = []

    # RemoteOK wraps job listings in <tr class="job">
    rows = soup.find_all("tr", class_="job")

    for row in rows:
        try:
            title_elem = row.find("h2", {"itemprop": "title"})
            company_elem = row.find("h3", {"itemprop": "name"})
            location_elem = row.find("div", class_="location")
            date_elem = row.find("time")
            tags = row.find_all("div", class_="tag")

            title = title_elem.text.strip() if title_elem else "N/A"
            company = company_elem.text.strip() if company_elem else "N/A"
            location = location_elem.text.strip() if location_elem else "Worldwide"
            date_posted = date_elem["datetime"] if date_elem and date_elem.has_attr("datetime") else "N/A"
            skills = ", ".join(tag.text.strip() for tag in tags if tag.text.strip())

            jobs.append({
                "title": title,
                "company": company,
                "location": location,
                "date_posted": date_posted,
                "skills": skills
            })
        except Exception:
            continue

    df = pd.DataFrame(jobs)
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/jobs.csv", index=False)
    print(f"📁 Saved {len(df)} jobs to data/jobs.csv")
    return df
