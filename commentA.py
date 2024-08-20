

import streamlit as st
from googleapiclient.discovery import build
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
import re
import os




#API KEY------------------

# Configure Google Gemini API key
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
# YouTube API configuration
YOUTUBE_API_KEY = st.secrets["YOUTUBE_API_KEY"]
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)





#Function -----------------


# Function to extract video ID from various YouTube link formats
def extract_video_id(youtube_video_url):
    video_id = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", youtube_video_url)
    return video_id.group(1) if video_id else None


# Function to get comments from a YouTube video
def get_youtube_comments(video_link):
    video_id = extract_video_id(video_link)
    comments = []
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=100  # Adjust as needed
    )
    response = request.execute()

    for item in response['items']:
        comments.append(item['snippet']['topLevelComment']['snippet']['textOriginal'])

    return comments


# Function to analyze comments using a prompt with Gemini Pro
def analyze_comments_with_prompt(comments):
    prompt = f"""
    Please analyze the following comments from a YouTube video. 
    Provide insights into the overall sentiment, common themes, and any specific issues mentioned. 
    Summarize the key takeaways for someone considering watching the video.

    Comments:
    {comments}

    Your analysis should include:
    - Overall sentiment (positive, negative, neutral) and show it as percentage and text aslo
    - Common themes or topics discussed
    - Any specific praises or criticisms
    - Summary of what viewers think about the video
    """
    response = genai.GenerativeModel('gemini-pro').generate_content(prompt)
    return response.text




# Streamlit app -----------------
with st.sidebar:
    "[View the source code](https://github.com/sadia4444a/llm-gemini-yt-tools/blob/main/commentA.py)"
   

st.title('YouTube Comment Analysis')
video_link = st.text_input('Enter YouTube Video Link:')
submit = st.button('Analyze Comments')

if 'analysis_history' not in st.session_state:
    st.session_state['analysis_history'] = []

if submit and video_link:
    comments = get_youtube_comments(video_link)
    analysis = analyze_comments_with_prompt(comments)
    st.write(analysis)
    st.session_state['analysis_history'].append({
        'video_link': video_link,
        'analysis': analysis
    })


st.header(":red[History]" , divider='violet' )

if st.session_state['analysis_history']:
    for idx, entry in enumerate(st.session_state['analysis_history'], 1):
        st.subheader(f":red[Analysis for Video {idx}]")
        st.write(f"**Video Link:** {entry['video_link']}")
        st.write(entry['analysis'])
        st.divider()