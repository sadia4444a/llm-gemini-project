import streamlit as st
from googleapiclient.discovery import build
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
import re



#API KEY------------------

# Configure Google Gemini API key
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
# YouTube API configuration
YOUTUBE_API_KEY = st.secrets["YOUTUBE_API_KEY"]
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)


#Function-------------------
# Function to extract video ID from various YouTube link formats
def extract_video_id(youtube_video_url):
    video_id = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", youtube_video_url)
    return video_id.group(1) if video_id else None

# Function to extract video details using YouTube Data API
def get_video_details(video_id):
    request = youtube.videos().list(part="snippet", id=video_id)
    response = request.execute()
    video_details = response['items'][0]['snippet']
    return video_details['title'], video_details['channelTitle']

# Function to extract transcript
def extract_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([item['text'] for item in transcript_list])
        return transcript
    except Exception as e:
        st.error(f"An error occurred while extracting the transcript: {e}")
        return None

# Function to generate LinkedIn post using Google Gemini
def generate_linkedin_post(video_title, video_link, transcript_text):
    prompt = f"""
    You are a social media content creator. Your task is to write a LinkedIn-style post that feels personal and engaging. 
    You've just watched a YouTube video and found it very interesting. Your post should include the following:

    1. A brief introduction about how you found the video interesting and worth sharing.
    2. The video title and a direct link to it.
    3. The main theme of the video and key takeaways or learnings from it point by point more details.
    4. An engaging call-to-action, encouraging others to watch the video and share their thoughts.
    5. Use a conversational tone and include emojis to make the post more relatable and fun.
    6. use video link in post

    Here’s the video transcript and details:

    Video Title: {video_title}
    Video Link: {video_link}
    Transcript: {transcript_text}

    Write a LinkedIn post based on this information that feels personal, engaging, easy to read and understand and uses appropriate emojis.
    """
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text





# Streamlit UI---------------------

with st.sidebar:
    "[View the source code](https://github.com/sadia4444a/llm-gemini-yt-tools/blob/main/CreatePost.py)"
   
st.title("YouTube to LinkedIn Post Generator")

youtube_link = st.text_input("Enter YouTube Video Link:")

if 'post_history' not in st.session_state:
    st.session_state['post_history'] = []

if st.button("Generate LinkedIn Post"):
    video_id = extract_video_id(youtube_link)
    if video_id:
        video_title, channel_name = get_video_details(video_id)
        transcript_text = extract_transcript(video_id)
        
        if transcript_text:
            linkedin_post = generate_linkedin_post(video_title, youtube_link, transcript_text)
            st.markdown("### LinkedIn-Style Post")
            st.write(linkedin_post)
            st.session_state['post_history'].append({
        'video_link': youtube_link,
        'response': linkedin_post
    })
            
st.header(":red[History]" , divider='violet' )

if st.session_state['post_history']:
    for idx, entry in enumerate(st.session_state['post_history'], 1):
        st.subheader(f":red[Analysis for Video {idx}]")
        st.write(f"**:green[Video Link]:** {entry['video_link']}")
        st.write(entry['response'])
        st.divider()