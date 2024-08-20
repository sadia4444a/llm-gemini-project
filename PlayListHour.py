import streamlit as st
import re
from datetime import timedelta
from googleapiclient.discovery import build


with st.sidebar:
    "[View the source code](https://github.com/sadia4444a/llm-gemini-project/blob/master/PlayListHour.py)"
   
    
# UI Components
st.subheader('Hello 😎, I am here to help you.')
st.markdown("### Find Total Duration Of a Playlist")
st.divider()

# Input for the playlist link
link = st.text_input('Enter Playlist Link 👇')

# Function to extract playlist ID from the link
def extract_playlist_id(url):
    match = re.search(r'list=([^&]+)', url)
    return match.group(1) if match else None

# Extract playlist ID
playlist_id = extract_playlist_id(link)

if 'playlist_history' not in st.session_state:
    st.session_state['playlist_history'] = []

# Button to trigger the duration calculation
if st.button('Calculate Duration'):
    if playlist_id:
        try:
            # YouTube API setup
            api_key = st.secrets["YOUTUBE_API_KEY"]
            youtube = build('youtube', 'v3', developerKey=api_key)

            # Regex patterns for extracting time
            hours_pattern = re.compile(r'(\d+)H')
            minutes_pattern = re.compile(r'(\d+)M')
            seconds_pattern = re.compile(r'(\d+)S')

            total_seconds = 0
            nextPageToken = None

            while True:
                # Request playlist items
                pl_request = youtube.playlistItems().list(
                    part='contentDetails',
                    playlistId=playlist_id,
                    maxResults=50,
                    pageToken=nextPageToken
                )
                pl_response = pl_request.execute()

                # Collect video IDs
                vid_ids = [item['contentDetails']['videoId'] for item in pl_response['items']]

                # Request video details
                vid_request = youtube.videos().list(
                    part='contentDetails',
                    id=','.join(vid_ids)
                )
                vid_response = vid_request.execute()

                # Calculate total duration
                for item in vid_response['items']:
                    duration = item['contentDetails']['duration']

                    hours = int(hours_pattern.search(duration).group(1)) if hours_pattern.search(duration) else 0
                    minutes = int(minutes_pattern.search(duration).group(1)) if minutes_pattern.search(duration) else 0
                    seconds = int(seconds_pattern.search(duration).group(1)) if seconds_pattern.search(duration) else 0

                    video_seconds = timedelta(hours=hours, minutes=minutes, seconds=seconds).total_seconds()
                    total_seconds += video_seconds

                nextPageToken = pl_response.get('nextPageToken')
                if not nextPageToken:
                    break

            # Convert total seconds to hours, minutes, and seconds
            total_seconds = int(total_seconds)
            minutes, seconds = divmod(total_seconds, 60)
            hours, minutes = divmod(minutes, 60)
            st.write(f'This playlist takes a total time of :red[**{hours} Hour(s), {minutes} Minute(s), and {seconds} Second(s)**.]')

            st.session_state['playlist_history'].append({
            'playlist_link':link ,
            'time':f'This playlist takes a total time of :red[**{hours} Hour(s), {minutes} Minute(s), and {seconds} Second(s)**.]'})
            
        except Exception as e:
            st.write("Oops! Something went wrong. Please check the playlist link and try again.")
    else:
        st.write("Invalid playlist link. Please enter a valid YouTube playlist URL.")

st.header(":red[History]" , divider='violet' )

if st.session_state['playlist_history']:
    for idx, entry in enumerate(st.session_state['playlist_history'], 1):
        st.subheader(f":red[Playlist Duration  {idx}]")
        st.write(f"**Playlist Link:** {entry['playlist_link']}")
        st.write(entry['time'])
        st.divider()
        