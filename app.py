import streamlit as st
import pandas as pd
from scraper.remoteok_scraper import scrape_remoteok
from analysis import analyzer
import plotly.express as px

st.set_page_config(
    page_title="📡 Job Radar",
    page_icon="🛰️",
    layout="wide",
)

st.markdown("""
    <style>
    .stApp {
        background-color: #1e1e2f;
        color: #f0f0f0;
        font-family: 'Segoe UI', sans-serif;
    }
    h1, h2, h3 {
        color: #58a6ff;
    }
    .block-container {
        padding-top: 2rem;
    }
    .custom-hr {
        border: none;
        height: 1px;
        background: #3e3e55;
        margin: 30px 0;
    }
    .stTextInput > div > div > input {
        background-color: #2c2c3e;
        color: white;
    }
    .stButton > button {
        background-color: #58a6ff;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("## 🛰️ Job Radar – Real-Time Market Analysis")
st.markdown("Discover emerging job trends and insights directly from **RemoteOK** listings.")
st.markdown('<hr class="custom-hr">', unsafe_allow_html=True)

with st.expander("🔍 Search Job Listings", expanded=True):
    col1, col2 = st.columns([4, 1])
    keyword = col1.text_input("Enter a job keyword:", placeholder="e.g., data scientist, front-end developer")
    fetch_clicked = col2.button("Fetch Live Data")

df = pd.DataFrame()

if fetch_clicked:
    with st.spinner("Fetching fresh job data..."):
        df = scrape_remoteok(keyword)
        st.success(f"{len(df)} listings found.")
else:
    df = analyzer.load_data()
    if not df.empty:
        st.info("Displaying previously saved job data.")
    else:
        st.warning("No data found. Please fetch live job listings.")

if not df.empty:
    st.markdown('<hr class="custom-hr">', unsafe_allow_html=True)
    st.subheader("📊 Key Insights")

    tab1, tab2, tab3 = st.tabs(["💼 Job Titles", "🌍 Locations", "🧠 Skills"])

    with tab1:
        st.dataframe(analyzer.get_top_job_titles(df), height=250)

    with tab2:
        st.dataframe(analyzer.get_top_locations(df), height=250)

    with tab3:
        top_skills = analyzer.get_top_skills(df)
        if top_skills:
            skill_df = pd.DataFrame(top_skills, columns=["Skill", "Frequency"])
            st.dataframe(skill_df, height=250)
        else:
            st.info("No skill data extracted from current listings.")

    st.markdown('<hr class="custom-hr">', unsafe_allow_html=True)
    st.subheader("📈 Trend Over Time")

    trend_data = analyzer.get_posting_trends(df)
    if not trend_data.empty:
        fig = px.bar(
            trend_data,
            title="📅 Job Postings by Date",
            labels={'index': 'Date', 'value': 'Number of Jobs'},
            color_discrete_sequence=["#00c2ff"]
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Insufficient posting date data to visualize trends.")

else:
    st.markdown("🚀 Enter a keyword and hit **Fetch Live Data** to begin exploring real-time job insights.")
