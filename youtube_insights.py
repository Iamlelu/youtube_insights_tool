## api project 


from platform import python_version

print(python_version())



from googleapiclient.discovery import build
import pandas as pd



import os

from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")


youtube = build("youtube", "v3", developerKey=API_KEY)


def search_youtube(query, max_results=5):
    search_response = youtube.search().list(
        q=query,
        part="snippet",
        type="video",
        maxResults=max_results
    ).execute()

    video_ids = [item["id"]["videoId"] for item in search_response["items"]]

    # Fetch video statistics
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
            "views": item["statistics"].get("viewCount", 0),
            "likes": item["statistics"].get("likeCount", 0),
            "comments": item["statistics"].get("commentCount", 0)
        })

    return pd.DataFrame(video_data)


if __name__ == "__main__":
    df = search_youtube("Education", max_results=5)
    print(df)
