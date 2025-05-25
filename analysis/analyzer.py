# analysis/analyzer.py

import pandas as pd
from collections import Counter

def load_data(filepath='data/jobs.csv'):
    try:
        return pd.read_csv(filepath)
    except FileNotFoundError:
        return pd.DataFrame()

def get_top_job_titles(df, n=5):
    return df['title'].value_counts().head(n)

def get_top_locations(df, n=5):
    return df['location'].value_counts().head(n)

def get_posting_trends(df):
    if 'date_posted' in df.columns:
        return df['date_posted'].value_counts().sort_index()
    return pd.Series(dtype="int")

def get_top_skills(df, n=5):
    if 'skills' not in df.columns:
        return []

    all_skills = []
    for entry in df['skills'].dropna():
        skills = [s.strip().lower() for s in entry.split(",") if s.strip()]
        all_skills.extend(skills)

    skill_counts = Counter(all_skills)
    return skill_counts.most_common(n)
