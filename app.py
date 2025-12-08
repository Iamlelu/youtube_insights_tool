import streamlit as st
import pandas as pd
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")

youtube = build("youtube", "v3", developerKey=API_KEY)

def search_youtube(query, max_results=10):
    search_response = youtube.search().list(
        q=query,
        part="snippet",
        type="video",
        maxResults=max_results
    ).execute()

    video_ids = [item["id"]["videoId"] for item in search_response["items"]]

    stats_response = youtube.videos().list(
        part="statistics,snippet",
        id=",".join(video_ids)
    ).execute()

    video_data = []

    for item in stats_response["items"]:
        video_data.append({
            "video_title": item["snippet"]["title"],
            "channel_title": item["snippet"]["channelTitle"],
            "published_at": item["snippet"]["publishedAt"],
            "video_id": item["id"],
            "views": int(item["statistics"].get("viewCount", 0)),
            "likes": int(item["statistics"].get("likeCount", 0)),
            "comments": int(item["statistics"].get("commentCount", 0))
        })

    return pd.DataFrame(video_data)


# --------------------------
# STREAMLIT UI

st.title("YouTube Insights Tool")
st.write("A simple tool to fetch insights for any YouTube keyword.")

query = st.text_input("Enter a topic to search:", "technology news")
max_results = st.slider("Number of videos:", 5, 50, 10)

if st.button("Search"):
    with st.spinner("Fetching data..."):
        df = search_youtube(query, max_results)
        st.success("Done!")
        st.dataframe(df)

        st.subheader("Top Videos by Views")
        st.bar_chart(df.set_index("video_title")["views"])