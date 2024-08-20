import streamlit as st
import re
from googleapiclient.discovery import build



with st.sidebar:
    "[View the source code](https://github.com/sadia4444a/llm-gemini-yt-tools/blob/main/PopularVideo.py)"
    

st.markdown("### Find Most Popular video in a Playlist")
st.divider()

link = st.text_input('Enter Playlist link 👇')


# Function to extract playlist ID from the link
def extract_playlist_id(url):
    match = re.search(r'list=([^&]+)', url)
    return match.group(1) if match else None

# Extract playlist ID
playlist_id = extract_playlist_id(link)


if 'populer_history' not in st.session_state:
    st.session_state['populer_history'] = []


# Button to trigger the duration calculation
if  st.button('Find Most Popular Video'):
    if playlist_id:
        try:
            api_key = st.secrets["YOUTUBE_API_KEY"]
            youtube = build('youtube', 'v3', developerKey=api_key)

            nextPageToken = None
            video_details = []

            while True:
                pl_request = youtube.playlistItems().list(
                    part='contentDetails',
                    playlistId=playlist_id,
                    maxResults=50,
                    pageToken=nextPageToken
                )

                pl_response = pl_request.execute()

                vid_ids = [item['contentDetails']['videoId'] for item in pl_response['items']]

                vid_request = youtube.videos().list(
                    part='statistics,snippet',
                    id=','.join(vid_ids)
                )

                vid_response = vid_request.execute()

                for item in vid_response['items']:
                    video_details.append({
                        'title': item['snippet']['title'],
                        'video_id': item['id'],
                        'view_count': int(item['statistics'].get('viewCount', 0))
                    })

                nextPageToken = pl_response.get('nextPageToken')

                if not nextPageToken:
                    break

            # Find the video with the highest view count
            most_popular_video = max(video_details, key=lambda x: x['view_count'])

            st.write(f"The most popular video title is: :red[**{most_popular_video['title']}**]")
            video_url = f"https://www.youtube.com/watch?v={most_popular_video['video_id']}"
            st.write(f"Watch it here: [Watch Video]({video_url})")
            st.image(f"http://img.youtube.com/vi/{most_popular_video['video_id']}/0.jpg", use_column_width=True)
            
            st.session_state['populer_history'].append({
            'video_link': video_url,
            'image': f"http://img.youtube.com/vi/{most_popular_video['video_id']}/0.jpg",
            'playlist_link': link
            })

            
        except Exception as e:
            st.write("Oops! Something went wrong. Please check the playlist link and try again.")
    else:
        st.write("Invalid playlist link. Please enter a valid YouTube playlist URL.")


st.header(":red[History]" , divider='violet' )

if st.session_state['populer_history']:
    for idx, entry in enumerate(st.session_state['populer_history'], 1):
        st.subheader(f":red[Populer Video {idx}]")
        st.write(f"**Video Link:** {entry['video_link']}")
        st.write(f"**Playlist link:** {entry['playlist_link']}")
        st.image(entry['image'], use_column_width=True)
        st.divider()
        